---
layout: splash
title:
---

<!--
**pegasas/pegasas** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I’m currently working on ...
- 🌱 I’m currently learning ...
- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->

<div class="pg">

<section class="pg-hero">
  <div class="pg-wrap">
    <div>
      <span class="pg-eyebrow">Hi 👋 Coders</span>
      <h1><span>From <em>Systems</em></span> <span>to <em>Algorithms</em></span> <span>to <em>AI</em></span></h1>
      <p class="pg-lead">I’m John Huang. 目前专注于 Agentic AI、AI Infra 与 Physical AI，并以分布式系统、数据库与云原生为底座，把实践与学习沉淀为一份结构化的技术知识库。</p>
      <div class="pg-btns">
        <a class="pg-btn primary" href="{{ '/notes/' | relative_url }}">浏览 Notes &rarr;</a>
        <a class="pg-btn ghost" href="https://github.com/pegasas">GitHub 主页</a>
      </div>
      <div class="pg-links">
        <a href="{{ '/notes/projects/strata-gpu-benchmark/' | relative_url }}"><small>Latest · 项目笔记</small><b>Strata 推理引擎：GPU 基准与 kernel 级剖析</b><span>decode / prefill / 并发实测，以及 8 个按优先级排序的改进点 &rarr;</span></a>
        <a href="{{ '/notes/projects/strata-build-roadmap/' | relative_url }}"><small>Roadmap · 项目笔记</small><b>参考 Strata 构建自己的本地推理产品</b><span>设计要点、趋势榜信号与 5 个可选方向 &rarr;</span></a>
      </div>
    </div>
    <div class="pg-visual" aria-hidden="true">
      <div class="pg-float a"><small>01 · Agentic AI</small><strong>工具调用、记忆与评估闭环</strong><i style="width:92%"></i><i style="width:64%"></i></div>
      <div class="pg-float b"><small>02 · AI Infra</small><strong>KV Cache 与推理 Serving</strong><i style="width:84%"></i><i style="width:48%"></i></div>
      <div class="pg-float c"><small>03 · Physical AI</small><strong>感知、仿真与闭环控制</strong><span class="pg-chip">Simulation</span><span class="pg-chip">Control</span></div>
    </div>
  </div>
</section>

<section class="pg-section soft" id="notes">
  <div class="pg-wrap">
    <div class="pg-head"><span class="pg-eyebrow">Notes</span><h2>技术知识库</h2><p>分两段组织：AI 是当前方向，计算机基础是底座。点分组进入子类，点子类标签直达对应位置。</p></div>
{% include notes-overview.html %}
  </div>
</section>

<section class="pg-section" id="about">
  <div class="pg-wrap">
    <div class="pg-head"><span class="pg-eyebrow">About</span><h2>我在做什么</h2></div>
    <div class="pg-feat">
      <div><span class="pg-ico">🔭</span><h3>Working on</h3><p>I’m currently working on <b>LLM / AI Infra / Agentic AI / Physical AI / AI Factory</b>.</p></div>
      <div><span class="pg-ico">🌱</span><h3>Learning</h3><p>I’m currently learning <b>LLM, AI Infra, distributed system, db, cloud native</b>, etc.</p></div>
      <div><span class="pg-ico">👯</span><h3>Collaborate</h3><p>I’m looking to collaborate on <b>C/C++, Java, Golang, Python, Rust</b>.</p></div>
    </div>
  </div>
</section>

<section class="pg-contact" id="contact">
  <div class="pg-wrap">
    <div>
      <h2>Let’s talk.</h2>
      <p>📫 How to reach me: Email me or try to figure out my WeChat number.</p>
      <p>😄 Pronouns: He</p>
    </div>
    <div class="pg-btns">
      <a class="pg-btn primary" href="{{ '/notes/' | relative_url }}">Browse Notes</a>
      <a class="pg-btn ghost" href="https://github.com/pegasas">GitHub</a>
    </div>
  </div>
</section>

<section class="pg-section">
  <div class="pg-wrap">
    <div class="pg-head"><span class="pg-eyebrow">Activity</span><h2>GitHub Analytics</h2></div>
    <div class="pg-analytics">
      <img width="48%" src="{{ '/assets/images/profile/github-stats.svg' | relative_url }}" alt="GitHub stats"/>
      <img width="48%" src="{{ '/assets/images/profile/top-langs.svg' | relative_url }}" alt="Most used languages"/>
    </div>
    <img class="pg-badge" src="https://visitor-badge.laobi.icu/badge?page_id=pegasas.pegasas" alt="visitors">
  </div>
</section>

</div>
