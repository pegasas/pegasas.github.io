---
layout: project-summary
classes: wide
title: "Qwen3-8B 偏好微调：训练、上线与评分口径复核"
permalink: /notes/projects/qwen3-dpo-evaluation/
author_profile: false
toc: false
excerpt: "完成 QLoRA-DPO 和动态 LoRA 服务后，逐 token 复核偏好分数，修正对单一评测数字的解释。"
private_url: https://github.com/pegasas/pegasas-notes-v2/blob/main/notes/projects/qwen3-dpo-evaluation.md
---

我使用 1 张 GPU 完成 Qwen3-8B 的 QLoRA-DPO，保存 adapter，并接入 vLLM 动态 LoRA 服务。随后扩充偏好评测，保存逐 token 分数，重新检查评分范围。

## 训练参数与资源

| 项目 | 实际配置或记录 |
|---|---|
| GPU | 1 张 GPU；训练、评测与服务实验分阶段执行 |
| 训练与服务基座 | Qwen3-8B 4-bit 训练基座；Qwen3-8B-AWQ 服务基座 |
| 数据 | 36 对训练样本；初始 12 对留出，扩展后共 48 对评测 |
| LoRA | rank=16，alpha=16，dropout=0；attention 与 MLP 投影 |
| batch 与累积 | 每卡 batch=1，梯度累积=4，有效 batch=4 |
| 序列上限 | 总长度 512 token，prompt 长度 256 token |
| 优化参数 | BF16，8-bit AdamW；学习率 5e-6，DPO beta=0.1 |
| 调度与重复性 | cosine，warmup ratio=0.1，seed=3407；选中 adapter 实际训练 10 epochs |
| 训练器 runtime | 212.0203 秒；1 卡折算约 **0.0589 GPU·小时** |
| 训练器吞吐 | 1.698 samples/s；0.424 steps/s |
| 保存产物 | adapter 约 167 MiB |

GPU 小时仅按选中训练段的运行时间折算，不包含环境准备、模型加载、其他训练尝试或后续评测和服务，也不是完整项目计费。该训练段没有可独立核实的峰值显存汇总，不用设备容量代替消耗。

## 关键质量结果

| 评测数据与口径 | Base | LoRA |
|---|---:|---:|
| 初始 12 对，训练基座离线评分，完整 assistant turn | 7/12 | 11/12 |
| 扩展合并 48 对，AWQ 服务评分，完整 assistant turn | 36/48 | 44/48 |
| 同一 48 对，仅比较答案内容 | 37/48 | 41/48 |

完整 turn 包含模板结束符与末尾换行。改成只比较答案内容后，改进方向仍为正，但配对检验的名义 p 值从约 0.0078 变成 0.125，原先对单一 91.7% 分数的解释需要收窄。

## 动态 LoRA 的服务成本

另做三组相同到达轨迹的 base / LoRA 配对：每组 120 个请求，其中 108 个输入为 128 token、12 个为 4096 token，均输出 256 token；活动序列上限 32，长 prefill 阈值 512，关闭前缀缓存，temperature=0。两侧都启用同一 LoRA runtime，只改变请求选择的模型。

| 指标 | LoRA 相对 Base 的三组平均变化 |
|---|---:|
| 短请求平均 TPOT | +5.09 ms（+14.2%） |
| 符合延迟要求的 goodput | −13.5% |
| 总输出吞吐 | −1.08% |
| 设备显存采样峰值 | 六个服务窗口均为 19606 MiB |

合格条件为每请求 TTFT≤1000 ms 且平均 TPOT≤50 ms。服务窗口显存属于服务对照，不能替代训练峰值。质量数据是小型自编合成集，扩展评测受先前结果影响；这些分数不能作为通用能力或真实用户偏好的证明，训练与服务基座的量化数值差异也需分别看待。

完整笔记保留训练配置、上线过程、逐题复核与服务对照。
