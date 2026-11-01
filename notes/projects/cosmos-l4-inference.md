---
layout: project-summary
classes: wide
title: "单张 L4 跑 Cosmos：从基础样例到视频分辨率边界"
permalink: /notes/projects/cosmos-l4-inference/
author_profile: false
toc: false
excerpt: "从图像和视频实际输出出发，逐档验证单卡可运行边界，并保留显存采样和模型加载排障记录。"
private_url: https://github.com/pegasas/pegasas-notes-v2/blob/main/notes/projects/cosmos-l4-inference.md
---

在单张 L4 上，我逐项运行 Cosmos 3 Edge 的文生图、图片理解和文生视频，再提高输出档位；每项同时检查退出状态与实际产物。

已完成 **768 档位的图片和 25 帧视频**。扩展轮设备显存采样峰值为 **22562 MiB**，说明这组样例已接近本卡可用容量。分辨率参数的档位名称与实际文件尺寸分别记录。

这些是特定输入与配置下完成的样例，没有据此承诺更长视频、并发容量或训练可行性。

完整笔记保留样例结果位置、各轮配置、设备采样和未完成环节的排障记录。
