---
layout: single
classes: wide
title: "Strata 推理引擎：GPU 基准与 kernel 级剖析"
permalink: /notes/projects/strata-h100-benchmark/
author_profile: false
breadcrumbs: true
toc: true
toc_sticky: true
---

> 目标：[niko1221/strata](https://github.com/niko1221/strata) 发布版引擎 0.1.55（源码 checkout `c62d5e3a`），模型 Qwen3.8-Flash-Next。
> 硬件：1× NVIDIA GPU（94 GB 显存，约 835 TFLOPS BF16 dense），40 vCPU，314 GB RAM，驱动 580.126.20。由自动化脚本采集，**未修改任何引擎代码**。

## 结论速览

- **Decode 136–172 tok/s（IQ3_XXS），随上下文下降**：短 prompt 172 → 4K 155 → 16K 136，16K 时约 −21%。
- **Prefill 4.4–5.7K tok/s（IQ3_XXS）、6.2–7.2K tok/s（Q2_0）**：TTFT 4K 为 0.94 s，16K 为 2.9 s，32K 为 5.5 s。
- **4 路并发只有 202–207 tok/s 总吞吐，仅为单路（171）的 1.2×**，每路降到约 51 tok/s。
- **GPU 并未跑满**：decode 忙时显存控制器利用率约 15%，功耗约 244 W（峰值 361 W）。
- **量化类型对速度的影响超过体积差**：16K 时 Q2_0 decode 170 tok/s，比 IQ3_XXS（136）快 25%，而体积只小约 20%。
- **质量无差异**：三种量化、五次运行，sanity 套件均为 12/12。

## 测试边界

- 主机没有 `nvcc` / `cmake` / `nsys` / `ncu`，**没有 per-kernel profile**。关于"为什么慢"的判断都来自系统级遥测，标注为 *未证实*。
- 只测发布版引擎，没有源码重编，因此没有验证任何引擎改动。
- 标准协议仍是草案：IQ3_XXS 跑 3 次（decode 跨次波动 0.1 tok/s，重复性很好）；Q2_0、IQ3_S 各 1 次有效记录（表中为 3 轮取中位数）。
- parallel-overload 套件未运行（需要设置 `max_queue` / `queue_timeout`，默认未设置）。

## 数据

### 标准协议（track=default，视觉关闭，ctx 128K，MTP 开，KV int8）

| 量化 | 用例 | prompt tok/s | decode tok/s | decode 跨次范围 | TTFT (s) |
|---|---|---:|---:|---|---:|
| IQ3_XXS | short | 383 | 171.6 | 171.6–171.8 | 0.213 |
| IQ3_XXS | 4K | 4437 | 155.2 | 155.1–155.3 | 0.936 |
| IQ3_XXS | 16K | 5727 | 136.0 | 136.0–136.1 | 2.882 |
| Q2_0 | short | 313 | 181.2 | 180.3–181.3 | 0.257 |
| Q2_0 | 4K | 6195 | 150.0 | 149.9–150.0 | 0.674 |
| Q2_0 | 16K | 7213 | 170.1 | 170.0–170.1 | 2.292 |
| IQ3_S | short | 373 | 164.1 | 164.0–164.3 | 0.218 |
| IQ3_S | 4K | 4304 | 144.6 | 144.6–144.8 | 0.965 |
| IQ3_S | 16K | 5715 | 139.1 | 139.0–139.1 | 2.888 |

### 并发（4 个短请求同时放出，容量 4）

三种量化的聚合输出吞吐分别在 201–207（IQ3_XXS）、211–219（Q2_0）、208–210（IQ3_S）tok/s。

### 实验：`--parallel 8`（同模型、同机器）

| 客户端 | slots | p95 TTFT | p95 延迟 | 输出 tok/s |
|---|---|---|---|---|
| 8 | 4（默认） | 1.70–2.22 s | 2.99–3.04 s | 168.1, 170.9 |
| 8 | 8 | 0.70–0.86 s | 2.64–2.86 s | 178.6–193.7（6 次） |
| 4 | 4（默认） | 0.34–0.72 s | 1.62–2.05 s | 124.8, 157.6 |
| 4 | 8 | 0.31–0.71 s | 1.61–2.05 s | 124.9–159.2（6 次） |

8 slots 把 8 客户端下的 p95 TTFT 降低约 2.5×，吞吐提升 5–15%；4 客户端无变化。这是单机 A/B，**不代表其他硬件上的默认行为**。

### GPU 遥测（IQ3_XXS，500 ms 采样）

| 指标 | 均值 | GPU 忙时均值 | 最大 |
|---|---:|---:|---:|
| GPU 利用率 % | 47.2 | 86.3 | 100 |
| 显存控制器利用率 % | 8.1 | 14.9 | 26 |
| 功耗 W | 173.8 | 244.0 | 361 |
| SM 时钟 MHz | 1570.5 | 1784.1 | 1785 |

## Kernel 级剖析（Nsight Systems）

同一块 GPU，引擎 0.1.55，IQ3_XXS，`--parallel 4`，MTP `--spec 4`。每个负载单独一个采集窗口；trace 本身有开销，窗口间对比有意义，绝对 tok/s 约低 20%。

| 窗口 | 负载 | decode tok/s | GPU 忙碌 | kernel 数 / 输出 token | kernel 中位耗时 |
|---|---|---:|---:|---:|---:|
| d1 | 单路，短 prompt，512 输出 | 135.4 | 83.3% | 810 | 4.4 µs |
| d4 | 4 路并发 | 195.3（合计） | 84.4% | 521 | 4.1 µs |
| c16k | 16K prompt，512 输出 | 122.2 | 84.8% | 880 | 4.6 µs |
| p16k | 16K 冷 prefill | 5.5K prompt tok/s | 74.1% | — | 18.5 µs |

- **并发扩展差**：单 token 的 GPU 时间只从 6.15 ms 降到 4.32 ms（4 路）。专家 GEMV 类 kernel 在 4 路时仍保留 60–76% 的单 token 开销，因为各序列选中的专家不同，权重读取无法共享。
- **host 同步不是主因**：两种窗口 GPU 忙碌都约 83–84%，空洞中位 0.4 µs。
- **kernel 非常碎**：每 token 约 810 次 launch，四分之三短于 10 µs；部分热点 kernel 只有 11–41 个 block，远少于 SM 数。
- **Prefill**：16,258 token 用 2.92 s，GPU 空闲 26%；GPU 时间中量化矩阵乘 `mul_mat_q` 占 45.7%，prompt attention 占 11.6%。
- **长上下文 decode**：16K 时单 token GPU 时间 +13%（6.15 → 6.94 ms）。attention 每 token +29%，且同样 512 个 token 多跑了 7.6% 的 graph step，提示 MTP 接受率在长 prompt 下降低。
- **未完成**：Nsight Compute 在引擎的 CUDA graph 内回放 kernel 时进程中止，没有 per-kernel 的 SOL / 显存吞吐数据。

