---
layout: project-summary
classes: wide
title: "Strata 推理引擎：GPU 基准与 kernel 级剖析"
permalink: /notes/projects/strata-gpu-benchmark/
author_profile: false
toc: false
excerpt: "围绕量化、上下文和并发建立基准，结合系统遥测与 kernel 剖析复核端到端收益。"
private_url: https://github.com/pegasas/pegasas-notes-v2/blob/main/notes/projects/strata-gpu-benchmark.md
---

我围绕 Strata 推理引擎建立了一组量化、上下文长度和多请求对照，把首 token 时间、prefill、decode 与输出检查分开记录，再结合系统遥测和 kernel trace 排查性能变化。

实测中，并发请求增加后的收益受到工作负载限制；一次内核改动的端到端差异也没有稳定超过跨次运行波动。局部热点、单次速度和整体服务收益需要分别验证。

这份项目记录保留了有效结果与负结果，没有把一次局部尝试直接写成稳定加速结论。

完整笔记保留原有结果表、剖析过程、对照实验及后续计划。
