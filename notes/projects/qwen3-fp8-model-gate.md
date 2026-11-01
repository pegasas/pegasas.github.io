---
layout: project-summary
classes: wide
title: "把 FP8 接进 Qwen3：矩阵乘更快，整模型为什么更慢"
permalink: /notes/projects/qwen3-fp8-model-gate/
author_profile: false
toc: false
excerpt: "用真实权重完成 FP8 投影和整模型替换，记录局部算子收益被在线转换成本抵消的负结果。"
private_url: https://github.com/pegasas/pegasas-notes-v2/blob/main/notes/projects/qwen3-fp8-model-gate.md
---

在单张 L40S 上，我从 Qwen3 真实权重的投影实验开始，把同一套 FP8 实现接回完整模型，同时比较局部算子时间、完整执行时间和输出数值。

预先量化输入后，矩阵乘约有 **1.5–1.8 倍**的局部优势；计入在线转换并接回模型后，decode 反而慢约 **21%**，而且没有通过预设的完整模型数值检查。

这是一项保留完整记录的失败优化，局部算子结果不能作为模型加速或质量等价替换的证明。

完整笔记保留实现、独立重复、整模型对照和逐层误差定位。
