---
layout: page
title: schedule
permalink: /schedule/
nav: true
nav_order: 4
description: What we read each week, and who is doing what.
---

To claim a task, [edit the schedule](https://github.com/{{ site.github_repo }}/edit/main/_data/schedule.yml) and add a line under that week's `claims`:

```yaml
- who: your-github-username
  role: research # a role id from the roles page
  task: critique # a task id from the roles page
```

{% for w in site.data.schedule %}
{%- assign paper = site.papers | where: 'slug', w.paper | first -%}

<div class="schedule-week">
  <div class="week-head">
    <span>Week {{ w.week }}: {% if paper %}<a href="{{ paper.url | relative_url }}">{{ paper.title }}</a>{% else %}{{ w.topic }}{% endif %}</span>
    <span class="week-date">{{ w.date }}</span>
  </div>
  {% if paper and w.topic %}<div class="muted">{{ w.topic }}</div>{% endif %}
  {% if w.notes %}<div>{{ w.notes }}</div>{% endif %}
  {% if w.claims and w.claims.size > 0 %}
    <ul class="claims">
      {% for c in w.claims %}
        {%- assign who = c.who | split: '|' -%}
        <li>{% include course/people_inline.liquid people=who %} {% include course/role_badge.liquid role=c.role task=c.task %}</li>
      {% endfor %}
    </ul>
  {% else %}
    <div class="muted">No tasks claimed yet.</div>
  {% endif %}
</div>
{% endfor %}
