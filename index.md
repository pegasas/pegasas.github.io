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
    <div class="pg-intro">
      <span class="pg-eyebrow">John Huang / pegasas</span>
      <h1><span>From <em>Systems</em></span> <span>to <em>Algorithms</em></span> <span>to <em>AI</em></span></h1>
      <p class="pg-lead">I’m John Huang. 目前专注于 Agentic AI、AI Infra 与 Physical AI，并以分布式系统、数据库与云原生为底座，把实践与学习沉淀为一份结构化的技术知识库。</p>
      <div class="pg-btns">
        <a class="pg-btn primary" href="{{ '/notes/' | relative_url }}">浏览 Notes &rarr;</a>
        <a class="pg-btn ghost" href="https://github.com/pegasas">GitHub 主页</a>
      </div>
    </div>
    <aside class="pg-focus" aria-label="当前关注的技术方向">
      <div class="pg-focus-heading"><span>FIELD NOTES</span><span class="pg-focus-status">研究与实践</span></div>
      <div class="pg-focus-identity"><img src="{{ '/assets/images/logo.svg?v=5' | relative_url }}" alt="" width="88" height="88"><div><b>Systems. Data. AI.</b><span>从底层机制，到工程实践。</span></div></div>
      <nav class="pg-focus-links" aria-label="按技术方向浏览">
        <a href="{{ '/notes/topics/agent/' | relative_url }}"><span class="pg-focus-number">01</span><span><b>Agentic AI</b><small>工具调用、记忆与评估闭环</small></span>{% include pg-icon.html name="arrow" %}</a>
        <a href="{{ '/notes/topics/ai-infra/' | relative_url }}"><span class="pg-focus-number">02</span><span><b>AI Infra</b><small>KV Cache 与推理 Serving</small></span>{% include pg-icon.html name="arrow" %}</a>
        <a href="{{ '/notes/topics/ai-models/#s3' | relative_url }}"><span class="pg-focus-number">03</span><span><b>Physical AI</b><small>感知、仿真与闭环控制</small></span>{% include pg-icon.html name="arrow" %}</a>
      </nav>
    </aside>
  </div>
</section>

<section class="pg-section pg-projects" id="projects">
  <div class="pg-wrap">
    <div class="pg-head"><span class="pg-eyebrow">Field Notes</span><h2>项目笔记</h2><p>每篇独立记录实战结果、实验参数和资源用量，完整过程保存在对应的私有笔记中。</p></div>
    {% include project-notes.html %}
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
      <div><span class="pg-ico">{% include pg-icon.html name="ai-infra" %}</span><h3>Working on</h3><p>I’m currently working on <b>LLM / AI Infra / Agentic AI / Physical AI / AI Factory</b>.</p></div>
      <div><span class="pg-ico">{% include pg-icon.html name="learning" %}</span><h3>Learning</h3><p>I’m currently learning <b>LLM, AI Infra, distributed system, db, cloud native</b>, etc.</p></div>
      <div><span class="pg-ico">{% include pg-icon.html name="collaborate" %}</span><h3>Collaborate</h3><p>I’m looking to collaborate on <b>C/C++, Java, Golang, Python, Rust</b>.</p></div>
    </div>
  </div>
</section>

<section class="pg-contact" id="contact">
  <div class="pg-wrap">
    <div>
      <span class="pg-eyebrow">Keep exploring</span>
      <h2>Let’s talk.</h2>
      <p>How to reach me: Email me or try to figure out my WeChat number.</p>
      <p class="pg-contact-meta">Pronouns: He</p>
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
