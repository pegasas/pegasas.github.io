---
layout: single
classes: wide
title: "参考 Strata 构建自己的本地推理产品：设计要点、趋势信号与路线"
permalink: /notes/projects/strata-build-roadmap/
author_profile: false
breadcrumbs: true
toc: true
toc_sticky: true
---

> 依据：对 [niko1221/strata](https://github.com/niko1221/strata)（引擎 0.1.55、应用 0.2.9）的 README、`AGENTS.md`、`docs/HOW_IT_WORKS.md`、`docs/DETAILS.md` 目录和源码规模的阅读；CUDA 内核未逐行阅读。趋势数据取自 2026-11-01 当天 Hugging Face 趋势榜（`sort=trendingScore`）的一次快照，会很快变化。路线是判断，不是实测结论。

## 1. Strata 是什么

- 本地大模型推理引擎，目标是把大型 MoE 模型放进 12–24 GB 显存的家用电脑。后端为 C++/CUDA，另有 HIP（AMD）、SYCL（Intel）、Metal（Mac）；模型格式为 GGUF，底层复用 llama.cpp / ggml。
- 外围分三块：桌面应用（Tauri 外壳加 Node 主机与网页界面）、命令行（`strata launch / connect`）、服务端（OpenAI 与 Anthropic 兼容接口，另有 MCP 服务端）。
- 源码规模：`src/` 下 core、kernels、prefill、dsv41 各约 2.4–3.2 万行；`setup.py` 单文件约 1.05 万行。

## 2. 值得参考的设计

| 设计 | 做法 | 可借鉴点 |
|---|---|---|
| 分层放置 | 显卡放注意力层、路由和最常用的专家；内存放全部专家并由 CPU 并行计算；SSD 放 n-gram 查找表 | 显存放不下就按访问频率分层，而不是整体卸载 |
| 自适应专家缓存 | 显存剩余部分缓存最常用的专家，随对话变化；双小显卡时去重（实测约 1900–2000 个重复槽位） | 缓存策略比单个内核更影响吞吐 |
| 先猜后验 | 模型自带 MTP 层一次猜最多 3 个词，整层验证；重复内容用 prompt lookup；输出与不猜时相同 | 投机解码正在成为标配 |
| 先预览再执行 | `strata launch --plan` 只打印计划，不下载、不改动 | 对用户和 AI 助手都友好 |
| 应用连接检查 | `strata connect <app> --check` 用该应用的方式发一次提示和一次工具调用 | 把"能不能接上"变成可验证的 |
| AI 可操作 | MCP 服务端把安装、启动、状态做成工具 | 让助手自己完成安装与排障 |
| 统一基准协议 | 短提示、4K、16K、并发、预填充；数字注明测量环境 | 可复现、可对比 |

局限：每个模型家族都要手写适配（目前只有 3 个家族）；硬件矩阵（NVIDIA、AMD、Intel、Mac）维护成本高；安装配置逻辑集中在一个超大文件里。

## 3. 趋势榜上的信号（2026-11-01 快照）

- **大型 MoE 加 GGUF 量化**：DeepSeek-V4.1-Flash-1017（榜单第 2）、ISTA-DASLab 的 GSQ-RCO GGUF（下载约 229 万）、Qwen3.8-Flash-Next 的 GGUF 变体（下载约 342 万）、Mistral-Large-4-1T-A52B、Clover-35B-A3B。
- **端侧小模型**：LiquidAI LFM3 全系（1.7B，以及 2B 的视觉、音频、全模态）、Nemotron-3.5-Bolt-E4B-4GB、Qwen3.5-4B、Spark-X2.6-4B。
- **语音与文档类模型**：Nemotron-3.5-Transcribe（识别）、Baidu Unlimited-OCR-2、MiniCPM-OCR-1.0、Audio8-TTS。
- **带 MTP 的微调版本**已进入普通用户视野（榜上有名称含 `MTP` 的 Qwen3.8-27B GGUF）。
- **图像与视频生成最热**（LTX-2.5、flux、Qwen-Image-2.1、Wan），但与推理引擎是两条线。

## 4. 可选方向

1. **多模态本地网关**（推荐）：用 llama.cpp 或 transformers 做底层，复用 Strata 的"先预览、再启动、再验证应用"流程，把端侧小模型、OCR、语音识别与合成串成一条流水线，对外是统一的 OpenAI 兼容接口。Strata 目前只覆盖文本与图片输入的 3 个大模型家族，这一块是空白。难度中，风险低，不碰 GPU 内核。
2. **硬件到模型的推荐与预览工具**：输入显卡、显存、内存、SSD，输出能跑哪些趋势榜模型、哪个量化版本、预期速度和启动命令。可接 Hugging Face 趋势接口和自己的基准数据。难度低到中。
3. **跨引擎基准平台**：同一模型在 llama.cpp、Strata、vLLM、MLX 上对比速度和质量，随趋势榜新模型周期更新。价值在数据和持续更新，不在代码量。难度中。
4. **端侧小模型专用引擎**：专攻 4B 以下模型加长上下文：KV 缓存量化、投机解码、手机或边缘设备部署。会直接与 llama.cpp、MLX 竞争，难度高。
5. **专攻一个系统优化点**：如 MoE 专家缓存与换页、投机解码、长上下文 KV。超大 MoE 增多使其更重要，但需要懂 CUDA，难度很高。

## 5. 建议顺序

先做 1 或 2：可以很快做出可用的东西，同时积累对硬件与模型格式的认识；3 作为持续产出的数据；4、5 在有明确瓶颈后再投入。

## 6. 一个提醒：单个内核优化的收益有限

对 Strata 的 `gr_down_staged` 内核做过一次 `NW=4`（每个 block 的 warp 数从 8 降到 4，block 数 41→81）的对照：输出逐位一致，但无追踪测速在单请求解码上只多约 2%，4 并发和 16K 上下文解码反而在 1% 内略慢；该内核在追踪中只占总时间的 11%–12%。单项内核优化的上限由它占的时间决定，系统层面的调度与缓存通常更值得先做。

## 7. 需要核实

- 哪些部分是 Strata 自研、哪些复用 llama.cpp：见其 `docs/DETAILS.md` 的"Credits and licenses"。
- 许可证：README 标注 MIT，但模型文件各有各的许可证；直接复制代码需保留声明。
- 趋势榜是一次快照；决定方向前应重新查看，并区分"下载量大"和"上升快"。
