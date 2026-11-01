---
layout: project-summary
classes: wide
title: "LoRA、QLoRA 与全量微调：同一模型的显存、训练与恢复实测"
permalink: /notes/projects/lora-qlora-full-finetuning/
author_profile: false
toc: false
excerpt: "固定模型、数据与监督 token，实际测量三种微调方式的训练、显存、checkpoint 和新进程恢复成本。"
private_url: https://github.com/pegasas/pegasas-notes-v2/blob/main/notes/projects/lora-qlora-full-finetuning.md
---

我对同一模型分别执行 LoRA、QLoRA 和全量 BF16 微调，固定数据顺序与监督 token 数，再实际保存 checkpoint、在新进程中恢复模型和优化器。QLoRA 减少了部分显存，却没有在这组配置下缩短训练时间。

## 参数与资源用量

| 项目 | 三组共同配置 |
|---|---|
| 计算资源与并行方式 | 1 张 L40S；三组顺序执行，每组单卡训练 |
| 模型与任务 | Qwen2.5-1.5B-Instruct；GSM8K completion-only SFT |
| 固定训练量 | 每组 160 个样本、20 步、34566 个非 padding token、20178 个监督目标 token |
| 批量 | microbatch=2，梯度累积=4，有效 batch=8；无 gradient checkpointing |
| 优化器 | AdamW，学习率 2e-4，weight decay=0 |
| Adapter | LoRA / QLoRA 均为 rank=16、alpha=32，作用于 Q/K/V/O 和 MLP 投影 |
| 精度 | LoRA 与全量组为 BF16；QLoRA 使用 NF4、double quantization 和 BF16 compute |
| 评测量 | 同一 64 条 dev 数据、8004 个目标 token，按目标 token 加权计算 loss |

三组纯训练窗口共 **39.088 秒**，按单卡折算 **39.088 GPU·秒，约 0.01086 GPU·小时**；这是训练段用量，不含加载、dev 评测、保存、恢复或首次环境失败。完整进程墙钟另外列出，不与纯训练时间混算。

## 训练与显存结果

| 指标 | BF16 LoRA | NF4 QLoRA | 全量 BF16 |
|---|---:|---:|---:|
| 可训练参数 | 18.46 M | 18.46 M | 1543.71 M |
| 纯训练时间 秒 | 12.421 | 18.090 | 8.577 |
| 训练段 GPU·秒 | 12.421 | 18.090 | 8.577 |
| 非 padding token/s | 2783 | 1911 | 4030 |
| 峰值 allocated / reserved GiB | 8.52 / 9.06 | 8.21 / 9.04 | 15.86 / 18.28 |
| dev loss 前 → 后 | 0.683 → 0.344 | 0.692 → 0.375 | 0.683 → 0.890 |

本轮三组对照中，最高纯训练吞吐为全量 BF16 的 **4030 非 padding token/s**，同时要看它的 dev loss 和完整进程成本。QLoRA 相比 LoRA 的峰值 allocated 节省约 **0.32 GiB、3.7%**，训练段则更慢。表中显存保留两位小数，差值按原始精度计算。

## 保存与恢复结果

| 指标 | BF16 LoRA | NF4 QLoRA | 全量 BF16 |
|---|---:|---:|---:|
| checkpoint | 222 MB | 222 MB | 9.26 GB |
| 其中优化器状态 | 148 MB | 148 MB | 6.18 GB |
| 保存时间 秒 | 0.34 | 0.33 | 9.44 |
| 新进程内部 ready 时间 秒 | 3.13 | 4.52 | 4.93 |
| 完整训练进程墙钟 秒 | 24.78 | 34.44 | 94.61 |
| 完整恢复进程墙钟 秒 | 7.38 | 8.88 | 9.06 |

三组恢复都加载了模型或 adapter 与优化器，并把相同首批数据放上 GPU；恢复检查没有额外更新。完整进程时间包含启动等非训练工作，不能解释为 GPU 活跃计算时间。

共用学习率下全量组 dev loss 恶化，但本轮没有分别调参或训练到收敛。这是小模型、短训练量下的系统比较，不能据此给三种方法的最佳质量排序。完整笔记保留环境排障、逐步日志和恢复检查。
