---
layout: project-summary
classes: wide
title: "四卡 vLLM：一次异步调度自旋的排查与修复"
permalink: /notes/projects/vllm-async-scheduler/
author_profile: false
toc: false
excerpt: "从 GPU 闲等和主线程忙碌查到异步调度自旋，完成最小复现、补丁与真实 GPU 前后验证。"
private_url: https://github.com/pegasas/pegasas-notes-v2/blob/main/notes/projects/vllm-async-scheduler.md
---

四张 GPU 执行一个短输出请求时，设备大量闲等，主线程却持续忙碌。我从容量诊断转向异步调度源码，构造最小复现，再用相同参数和负载验证显式启用的修复。前后 greedy 输出 token 完全一致。

## 参数与资源

| 项目 | 本次配置或实测用量 |
|---|---|
| 模型与精度 | Qwen2.5-14B-Instruct，FP16；vLLM 0.6.1.post1 |
| GPU 数量与并行方式 | 4 张 GPU；TP=1，PP=4 |
| 本次对照已测请求并发 | 1；输入 4096 token，输出 16 token |
| 上下文与调度上限 | `max-model-len=8192`，`max-num-seqs=1`，`max-num-batched-tokens=8192` |
| 执行参数 | eager；关闭 chunked prefill 和前缀缓存；CPU offload=0，swap=0 |
| 其他参数 | `gpu-memory-utilization=0.9`；seed=31925 |
| 设备显存采样峰值 | 两次运行均为每卡 13944–14048 MiB |
| 本次两阶段资源占用 | 完整对照阶段墙钟合计 **435.59 秒**；4 卡折算 **0.4840 GPU·时** |

资源折算包含这两个阶段的加载与暖机，不是 GPU 内核忙时，也没有把其他探索阶段计入。单请求上限为 1；四卡流水并行不等于四请求同时执行。

## 修复前后结果

| 指标 | 原版 | 活动任务等待修复 |
|---|---:|---:|
| 正式请求测量秒 | 318.266584 | 6.687034 |
| TTFT 秒 | 33.624885 | 4.891925 |
| 输出 token/s | 0.050272 | 2.392690 |
| 完成 / 到达请求 | 1 / 1 | 1 / 1 |
| 完整阶段墙钟秒 | 399.541134 | 36.053323 |
| 阶段占用折算 GPU·时 | 0.44393 | 0.04006 |

正式请求计时排除了加载和暖机，完整阶段墙钟则保留这些成本。CPU 最小复现与 GPU 前后记录分别保存；这次改动针对调度等待行为，没有用调度模拟替代模型测速。

本次对照最高观测输出速度为 **2.392690 token/s**。每种配置只有一次正式测量，尚不能外推为多并发服务收益、硬件最高速度或长期稳定性。补丁、唤醒语义检查和完整排障记录保留在这一篇对应的私有全文中。
