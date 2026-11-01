---
layout: project-summary
classes: wide
title: "vLLM 突发流量调优：3600 次请求的排队与延迟对照"
permalink: /notes/projects/vllm-burst-serving/
author_profile: false
toc: false
excerpt: "四轮独立服务对照中，首 token 延迟 p95 从约 1234 ms 降到 366 ms，同时记录逐 token 延迟和显存的代价。"
private_url: https://github.com/pegasas/pegasas-notes-v2/blob/main/notes/projects/vllm-burst-serving.md
---

在单张 L40S 上，我围绕突发到达后的请求积压做了一轮 vLLM 调优：固定同一段流量，启动四轮独立服务，保存 3600 次请求的流式时间戳，并与服务端排队指标核对。

首 token 延迟 p95 按两次独立运行汇总，从约 **1234 ms 降到 366 ms**；满足联合延迟要求的吞吐从约 **29.2 提高到 43.7 req/s**。两组候选运行都改善了排队，逐 token 延迟和设备显存占用也同时增加。

这些结果对应短时间、固定长度的突发负载。它反映的是服务合格率改善，不能据此推断长期 SLA 或模型计算吞吐同比增长。

完整笔记保留四轮对照、计时口径、请求校验和资源成本。
