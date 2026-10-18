---
layout: page
title: schedule
permalink: /schedule/
nav: true
nav_order: 5
description: What we read each week, and who is doing what.
---

Who does what each week lives in one spreadsheet-like file: [`_data/weekly_roles.csv`](https://github.com/{{ site.github_repo }}/edit/main/_data/weekly_roles.csv). To take a role, add one line:

```text
week,github_username,role,task,notes
3,your-github-username,visualization,redo-graph,trying a small-multiples version
```

`role` and `task` are the ids shown in grey on the [roles page]({{ '/roles/' | relative_url }}). Several people can take the same task; `notes` is optional. Changed your mind? Edit or delete your line.

{% for w in site.data.schedule %}
{%- assign paper = site.papers | where: 'slug', w.paper | first -%}

<div class="schedule-week">
  <div class="week-head">
    <span>Week {{ w.week }}: {% if paper %}<a href="{{ paper.url | relative_url }}">{{ paper.title }}</a>{% else %}{{ w.topic }}{% endif %}</span>
    <span class="week-date">{{ w.date }}</span>
  </div>
  {% if paper and w.topic %}<div class="muted">{{ w.topic }}</div>{% endif %}
  {% if w.notes %}<div>{{ w.notes }}</div>{% endif %}
  {% include course/week_roles.liquid week=w.week %}
</div>
{% endfor %}
