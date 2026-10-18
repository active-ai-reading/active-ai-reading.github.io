---
layout: page
title: guides
permalink: /guides/
nav: true
nav_order: 4
description: One living guide per role, written and passed on by the people who held it.
---

Each role has a guide, written by the students who held it and handed on from week to week (and from year to year). Before you take a role, read its guide and the latest [handoffs](https://github.com/{{ site.github_repo }}/tree/main/handoffs). After, fold in what you learned, including what didn't work.

<div class="post-grid">
  {% for r in site.data.roles %}
    {%- assign g = site.guides | where: 'role', r.id | first -%}
    {%- if g -%}
      {%- assign n_words = g.content | strip_html | number_of_words -%}
      <a class="post-card" href="{{ g.url | relative_url }}" style="--role-color: {{ r.color }}">
        <div class="post-card-top">
          <span class="post-card-role">{{ r.icon }} {{ r.name }}</span>
          <span class="post-card-date">{{ r.tasks | size }} task{% if r.tasks.size != 1 %}s{% endif %}</span>
        </div>
        <div class="post-card-title">{{ g.title }}</div>
        <div class="post-card-desc">{{ r.summary }}</div>
        <div class="post-card-paper">{% if n_words < 120 %}just started, help write it{% else %}{{ n_words }} words{% endif %}</div>
      </a>
    {%- endif -%}
  {% endfor %}
</div>

