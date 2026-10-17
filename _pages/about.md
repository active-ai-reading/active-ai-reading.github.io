---
layout: default
title: home
permalink: /
description: A course where students read AI papers actively, and publish summaries, critiques, better figures, reimplementations and posts for everyone.
---

{%- assign recent_posts = site.posts | slice: 0, 6 -%}

<div class="post">
  <section class="home-hero">
    <h1>Active <span class="accent">AI</span> Reading</h1>
    <p class="home-lede">
      We read AI papers the way researchers do: we rewrite them, criticize them, redraw their figures, rerun their code, trace their ideas
      and tell the world about them. Everything here is written by the students, in the open.
    </p>
    <div class="home-cta">
      <a class="primary" href="{{ '/papers/' | relative_url }}">Browse papers</a>
      <a href="{{ '/roles/' | relative_url }}">How the course works</a>
      <a href="{{ '/guide/' | relative_url }}">Write a post</a>
    </div>
    <div class="role-strip">
      {% for r in site.data.roles %}
        {% include course/role_badge.liquid role=r.id %}
      {% endfor %}
    </div>
  </section>

  <h2 class="section-title">Papers</h2>
  {% include course/paper_grid.liquid limit=6 %}

  {% if recent_posts.size > 0 %}
    <h2 class="section-title">Latest posts</h2>
    <div class="post-grid">
      {% for p in recent_posts %}
        {% include course/post_card.liquid post=p show_paper=true %}
      {% endfor %}
    </div>
    <p><a href="{{ '/posts/' | relative_url }}">All posts →</a></p>
  {% endif %}

  <h2 class="section-title">About the course</h2>
  <div class="post-content">
    <p>
      Every week we read one paper. Before class, each participant picks a <a href="{{ '/roles/' | relative_url }}">task</a>: rewrite the
      abstract, critique the paper, redo a graph, reimplement an experiment, write the social media thread, find the papers it builds on,
      and more. Then we write it up here, so the work is useful to everyone who reads the paper after us.
    </p>
    <p>
      You are welcome to experiment. Do the default thing, or try a new way that might fail. We encourage failure: learning only happens
      when you are exposed to the unknown.
    </p>
    <p>
      Want to join? See the <a href="{{ '/guide/' | relative_url }}">guide</a>. Reading along from outside the class? Comments, corrections
      and follow-ups are welcome on <a href="https://github.com/{{ site.github_repo }}/discussions">GitHub Discussions</a>.
    </p>
  </div>
</div>
