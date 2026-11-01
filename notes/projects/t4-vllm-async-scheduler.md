---
layout: project-summary
classes: wide
title: "四张 T4 跑 vLLM：一次异步调度自旋的排查与修复"
permalink: /notes/projects/t4-vllm-async-scheduler/
author_profile: false
toc: false
excerpt: "从 GPU 闲等和主线程忙碌查到异步调度自旋，完成最小复现、补丁与真实 GPU 前后验证。"
private_url: https://github.com/pegasas/pegasas-notes-v2/blob/main/notes/projects/t4-vllm-async-scheduler.md
---

四张 T4 执行一个短输出请求时，GPU 大量闲等，主线程却持续忙碌。我从容量诊断转向异步调度源码，构造最小复现，再用同一负载验证显式启用的修复。

这次单请求前后诊断中，正式请求时间由 **318.27 秒降到 6.69 秒**，greedy 输出 token 完全一致。CPU 复现与真实 GPU 记录分别保存，没有把调度模拟当成模型测速。

每种配置只有一次正式测量，这个结果还不能外推为多并发服务收益或长期稳定性结论。

完整笔记保留定位过程、修复实现、唤醒语义和验证记录。
