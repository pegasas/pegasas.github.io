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

在单张 L4 上，我完成 Qwen3-8B 的 QLoRA-DPO，保存 adapter，并接入 vLLM 动态 LoRA 服务。随后扩充偏好评测，保存逐 token 分数，重新检查评分范围。

在 **48 对**合成偏好样本上，包含模板结束符时 adapter 得分为 **44/48**，仅比较答案内容时为 **41/48**。改进方向仍为正，但幅度和统计强度依赖评分口径，原先对单一分数的解释需要收窄。

这组小样本自编数据的结果不能作为通用能力或真实用户偏好的证明。服务可运行与模型质量、延迟成本也分别验证。

完整笔记保留训练配置、上线过程、逐题复核与服务对照。
