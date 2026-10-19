---
layout: page
title: people
permalink: /people/
nav: true
nav_order: 6
description: Everyone writing for Active AI Reading.
---

{%- assign people = site.people | sort: 'name' -%}

<div class="people-grid">
  {% for p in people %}
    {%- assign n = site.posts | where_exp: 'post', 'post.by contains p.slug' | size -%}
    <a class="person-card" href="{{ p.url | relative_url }}">
      <img src="{% if p.photo %}{{ p.photo | relative_url }}{% else %}https://github.com/{{ p.slug }}.png?size=144{% endif %}" alt="" loading="lazy">
      <span class="person-card-name">{{ p.name | default: p.slug }}</span>
      <span class="person-card-sub">{% if p.role_in_course %}{{ p.role_in_course }} · {% endif %}{{ n }} post{% if n != 1 %}s{% endif %}</span>
    </a>
  {% endfor %}
</div>

<p>Not here yet? <a class="profile-link" href="https://github.com/{{ site.github_repo }}/blob/main/templates/person.md">Add yourself →</a> (rename the file to your GitHub username)</p>
