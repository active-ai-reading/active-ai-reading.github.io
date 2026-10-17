---
layout: page
title: papers
permalink: /papers/
nav: true
nav_order: 1
description: Every paper the course has read, with everything the class wrote about it.
---

{%- assign papers = site.papers | sort: 'year' | reverse -%}

<div class="paper-grid">
  {% for paper in papers %}
    {% include course/paper_card.liquid paper=paper %}
  {% endfor %}
</div>

<p class="muted">Adding a paper: copy <code>templates/paper.md</code> to <code>_papers/&lt;short-id&gt;.md</code> and fill it in. See the <a href="{{ '/guide/' | relative_url }}">guide</a>.</p>
