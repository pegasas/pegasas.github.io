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
      <h1>Notes on <em>systems, data</em> &amp; AI infra.</h1>
      <p class="pg-lead">I’m John Huang. 专注 LLM、AI Infra、Agentic AI 与 Physical AI，持续学习分布式系统、数据库与云原生，并把学到的东西整理成一份结构化的技术知识库。</p>
      <div class="pg-btns">
        <a class="pg-btn primary" href="{{ '/notes/' | relative_url }}">浏览 Notes &rarr;</a>
        <a class="pg-btn ghost" href="https://github.com/pegasas">GitHub 主页</a>
      </div>
      <div class="pg-stats">
        <div><b>16</b><span>知识域</span></div>
        <div><b>5</b><span>语言：C/C++ · Java · Go · Python · Rust</span></div>
        <div><b>Open</b><span>持续更新，源码在 GitHub</span></div>
      </div>
    </div>
    <div class="pg-visual" aria-hidden="true">
      <div class="pg-float a"><small>Distributed</small><strong>Raft 共识与日志复制</strong><i style="width:92%"></i><i style="width:64%"></i></div>
      <div class="pg-float b"><small>AI Infra</small><strong>KV Cache 与推理 Serving</strong><i style="width:84%"></i><i style="width:48%"></i></div>
      <div class="pg-float c"><small>Data Systems</small><strong>LSM-tree 存储引擎</strong><span class="pg-chip">Database</span><span class="pg-chip">Storage</span></div>
    </div>
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

<section class="pg-section soft" id="notes">
  <div class="pg-wrap">
    <div class="pg-head"><span class="pg-eyebrow">Notes</span><h2>技术知识库</h2><p>按知识域组织。从任意领域入口开始，沿基础与机制读到项目实现。</p></div>
    <div class="pg-grid">
{% for d in site.data.notes_domains %}
{% capture site_url %}/notes/{{ d.path }}/{% endcapture %}
{% assign synced = site.pages | where: "url", site_url | first %}
{% if synced %}{% assign href = site_url | relative_url %}{% else %}{% capture href %}https://github.com/pegasas/pegasas-notes-v2/tree/main/knowledge/{{ d.path }}{% endcapture %}{% endif %}
<a class="pg-card" href="{{ href }}"><span class="pg-ico">{{ d.icon }}</span><b>{{ d.title }}</b><span>{{ d.desc }}</span><em>进入 &rarr;</em></a>
{% endfor %}
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
      <img height="180em" width="48%" src="https://github-readme-stats.vercel.app/api/?username=pegasas&bg_color=30,000000,000000&title_color=6762A9&text_color=6c14a6&show_icons=true&include_all_commits=true&count_private=true"/>
      <img height="180em" width="48%" src="https://github-readme-stats.vercel.app/api/top-langs/?username=pegasas&layout=compact&langs_count=8&bg_color=30,000000,000000&title_color=6762A9&text_color=6762A9&show_icons=true&count_private=true"/>
    </div>
    <img class="pg-badge" src="https://visitor-badge.laobi.icu/badge?page_id=pegasas.pegasas" alt="visitors">
  </div>
</section>

</div>
