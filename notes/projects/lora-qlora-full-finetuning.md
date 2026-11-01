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

在单张 L40S 上，我对同一小模型分别执行 LoRA、QLoRA 和全量 BF16 微调，固定数据顺序与监督 token 数，并实际保存 checkpoint、在新进程中加载模型和优化器状态。

这组配置下，QLoRA 相比 LoRA，峰值分配显存从 **8.52 降到 8.21 GiB**，纯训练段时间却从 **12.42 增加到 18.09 秒**。全量微调则呈现出训练段和完整进程成本的另一种取舍。

这是固定小模型、短训练量与共用学习率下的系统比较，不能用来给三种方法的最佳质量或大模型成本排序。

完整笔记保留三组指标、环境排障、保存与恢复检查。
