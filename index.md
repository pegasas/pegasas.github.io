---
layout: single
classes: wide
title:
author_profile: true
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

<style>
.hp{--hp-accent:#5b4fc7;--hp-border:rgba(127,127,127,.28);--hp-soft:rgba(91,79,199,.07)}
.hp h2{margin:2.2em 0 .6em;padding:0;border:0;font-size:1.25em;letter-spacing:.01em}
.hp-hero{padding:2.2em 1.6em;border-radius:16px;background:linear-gradient(135deg,#5b4fc7 0%,#8a5cf6 55%,#c06cf0 100%);color:#fff}
.hp-hero h1{margin:0 0 .15em;color:#fff;font-size:2.1em;line-height:1.15}
.hp-hero p{margin:0;color:rgba(255,255,255,.9);font-size:1.02em}
.hp-btns{margin-top:1.3em;display:flex;flex-wrap:wrap;gap:.6em}
.hp-btns a{display:inline-block;padding:.5em 1.1em;border-radius:999px;font-weight:700;font-size:.9em;text-decoration:none;border:1.5px solid rgba(255,255,255,.85);color:#fff}
.hp-btns a.primary{background:#fff;color:#4b3fb5}
.hp-btns a:hover{opacity:.88}
.hp-grid{display:grid;gap:.9em;grid-template-columns:repeat(auto-fill,minmax(220px,1fr))}
.hp-card{display:block;padding:1em 1.1em;border:1px solid var(--hp-border);border-radius:12px;text-decoration:none;color:inherit;background:var(--hp-soft);transition:transform .15s,box-shadow .15s,border-color .15s}
.hp-card:hover{transform:translateY(-2px);box-shadow:0 6px 18px rgba(0,0,0,.1);border-color:var(--hp-accent)}
.hp-card b{display:block;font-size:1em;margin-bottom:.25em}
.hp-card span{display:block;font-size:.82em;opacity:.75;line-height:1.45}
.hp-about{list-style:none;margin:0;padding:0}
.hp-about li{margin:0;padding:.55em 0;border-bottom:1px solid var(--hp-border)}
.hp-about li:last-child{border:0}
.hp-more{margin-top:1em;font-size:.9em}
</style>

<div class="hp">

<div class="hp-hero">
  <h1>Hi 👋 Coders</h1>
  <p>Ads · LLM · Distributed Systems · Databases · Cloud Native</p>
  <div class="hp-btns">
    <a class="primary" href="{{ '/notes/' | relative_url }}">📚 Browse Notes</a>
    <a href="https://github.com/pegasas/pegasas-notes-v2">GitHub</a>
    <a href="https://scholar.google.com.hk/citations?user=g79gAJEAAAAJ&hl=zh-CN&oi=sra">Scholar</a>
  </div>
</div>

<h2>About</h2>

<ul class="hp-about">
  <li>🔭 I’m currently working on <b>ads domain</b>.</li>
  <li>🌱 I’m currently learning <b>LLM, distributed system, db, cloud native</b>, etc.</li>
  <li>👯 I’m looking to collaborate on <b>C/C++, Java, Golang, Python, Rust</b>.</li>
  <li>📫 How to reach me: Email me or try to figure out my WeChat number.</li>
  <li>😄 Pronouns: He</li>
</ul>

<img src="https://visitor-badge.laobi.icu/badge?page_id=pegasas.pegasas" style="max-width:100%;margin-top:.8em;">

<h2>📚 Notes</h2>

<p>技术知识库，按知识域组织，同步自 <a href="https://github.com/pegasas/pegasas-notes-v2">pegasas-notes-v2</a>。</p>

<div class="hp-grid">
{% for d in site.data.notes_domains %}
  {% capture site_url %}/notes/{{ d.path }}/{% endcapture %}
  {% assign synced = site.pages | where: "url", site_url | first %}
  {% if synced %}{% assign href = site_url | relative_url %}{% else %}{% capture href %}https://github.com/pegasas/pegasas-notes-v2/tree/main/knowledge/{{ d.path }}{% endcapture %}{% endif %}
  <a class="hp-card" href="{{ href }}"><b>{{ d.icon }} {{ d.title }}</b><span>{{ d.desc }}</span></a>
{% endfor %}
</div>

<p class="hp-more"><a href="{{ '/notes/' | relative_url }}">查看全部 Notes &rarr;</a></p>

<h2>GitHub Analytics</h2>

</div>

<div align="center">
  <img height="180em" width="48%" src="https://github-readme-stats.vercel.app/api/?username=pegasas&bg_color=30,000000,000000&title_color=6762A9&text_color=6c14a6&show_icons=true&include_all_commits=true&count_private=true"/>
  <img height="180em" width="48%" src="https://github-readme-stats.vercel.app/api/top-langs/?username=pegasas&layout=compact&langs_count=8&bg_color=30,000000,000000&title_color=6762A9&text_color=6762A9&show_icons=true&count_private=true"/>
</div>
