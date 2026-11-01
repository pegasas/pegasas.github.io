---
layout: single
classes: wide
title: "Strata on H100 NVL：基准测试与优化方向"
permalink: /notes/projects/strata-h100-benchmark/
author_profile: false
breadcrumbs: true
toc: true
toc_sticky: true
---

> 2026-11-01 · 目标：[niko1221/strata](https://github.com/niko1221/strata) 发布版引擎 0.1.55（源码 checkout `c62d5e3a`），模型 Qwen3.8-Flash-Next。
> 硬件：1× NVIDIA H100 NVL 94 GB，40 vCPU，314 GB RAM，驱动 580.126.20。由自动化脚本采集，**未修改任何引擎代码**。

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

### 实验：`--parallel 8`（同模型、同机器、同一天）

| 客户端 | slots | p95 TTFT | p95 延迟 | 输出 tok/s |
|---|---|---|---|---|
| 8 | 4（默认） | 1.70–2.22 s | 2.99–3.04 s | 168.1, 170.9 |
| 8 | 8 | 0.70–0.86 s | 2.64–2.86 s | 178.6–193.7（6 次） |
| 4 | 4（默认） | 0.34–0.72 s | 1.62–2.05 s | 124.8, 157.6 |
| 4 | 8 | 0.31–0.71 s | 1.61–2.05 s | 124.9–159.2（6 次） |

8 slots 把 8 客户端下的 p95 TTFT 降低约 2.5×，吞吐提升 5–15%；4 客户端无变化。这是单机同日 A/B，**不代表其他硬件上的默认行为**。

### GPU 遥测（IQ3_XXS，500 ms 采样）

| 指标 | 均值 | GPU 忙时均值 | 最大 |
|---|---:|---:|---:|
| GPU 利用率 % | 47.2 | 86.3 | 100 |
| 显存控制器利用率 % | 8.1 | 14.9 | 26 |
| 功耗 W | 173.8 | 244.0 | 361 |
| SM 时钟 MHz | 1570.5 | 1784.1 | 1785 |

## 改进方向（按优先级）

1. **A. Decode 批处理效率（最大，成因未证实）**：4 路只有单路 1.2×，显存控制器仅 15% 忙，更像 launch / 同步 / 延迟受限或串行化路径，而非带宽受限。待 Nsight 验证三个假设：每 token host/device 同步；小粒度 per-expert GEMV kernel 不随 batch 扩展；verify 窗口固定 6 token。
2. **B. IQ3 反量化成本**：Q2_0 比 IQ3_XXS 在 16K decode 快 25%、prefill 快 26%，超过约 20% 的体积优势，而显存流量很低，提示限制因素是 IQ3 查表反量化而非访存。
3. **C. Prefill 远低于 H100 能力**：对激活参数很小的模型只有 5–7K tok/s。可测更大 chunk、专用 prefill expert 布局，以及 16K–32K 是否受 expert-cache gather 限制。
4. **D. 长上下文 decode 衰减（16K −21%）**：16K 时 KV 全部驻留（`--kv-resident 32768`，int8），不是流式换入问题，应是 attention / KV 读取成本。
5. **E. 默认容量（已测，易改）**：显存充裕时提高默认 `--parallel`——引擎启动时已知有 85 GB 空闲。本卡上 8 slots 对 8 客户端更好、对 4 客户端持平。
6. **F. 宿主机告警**：`vm.nr_hugepages=0`；THP 开启但 expert arena 没请求 `MADV_HUGEPAGE`。本场景 expert 全在显存，影响小；部分卸载场景可能有影响（未测）。
7. **G. 可靠性与可观测性**：quick bench 有 1 个 agent 请求无 token 返回；overload 套件缺 `max_queue` 时报错信息不够直接。
8. **H. 基准工具**：`tools/strata_bench.py` 明确不是标准协议；标准 runner 需要 `launch-<preset>` 配置名，该约定未与 `--save-preset` 一起写明。

## 下一步测量（本次未做）

- 用 Nsight Systems / Compute 对 A–D 做 kernel 级 trace（需要带 CUDA toolkit 的主机）。
- Q2_0、IQ3_S 跑满 3 次标准协议，给出置信区间。
- 1K–128K 上下文扫描（decode 与 prefill）。
- 设置 `max_queue` 后的 overload 套件。
- 源码构建 `-DCMAKE_CUDA_ARCHITECTURES=90` 与发布版对比。
