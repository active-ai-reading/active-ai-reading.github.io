---
layout: page
title: roles
permalink: /roles/
nav: true
nav_order: 3
description: The tasks you can take on for each paper. Pick one every week.
---

Each week, everyone takes a task for that week's paper and writes a short piece for the site. You can do the default version, or try something new that might fail. Both are good. Several people can do the same task; comparing versions is half the fun.

**Before every class, read the paper:** at least the main part, and whatever your task needs.

To take a task, sign up in {% include course/signup_link.liquid %} (one row per week). Each role has a [guide]({{ '/guides/' | relative_url }}) written by the people who held it before you. To write it up, copy the template named after the role from the [`templates/`](https://github.com/{{ site.github_repo }}/tree/main/templates) folder. The role and task ids below (in grey) are what you put in your post's header.

{% for r in site.data.roles %}

<section class="role-section" id="{{ r.id }}" style="--role-color: {{ r.color }}">
  <h2>{{ r.icon }} {{ r.name }} <span class="task-id">role: {{ r.id }}</span></h2>
  <p class="muted">{{ r.summary }} <a href="{{ '/guides/' | append: r.id | append: '/' | relative_url }}">Read the {{ r.name | downcase }} guide →</a></p>
  {% for t in r.tasks %}
    <div class="task">
      <div><span class="task-name">{{ t.name }}</span> <span class="task-id">task: {{ t.id }}</span></div>
      <div>{{ t.prompt }}</div>
    </div>
  {% endfor %}
</section>
{% endfor %}

<p class="muted">The roles and tasks are set by the course. Have an idea for a change? Raise it in class or in <a href="https://github.com/{{ site.github_repo }}/discussions">Discussions</a>.</p>
