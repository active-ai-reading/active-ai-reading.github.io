---
layout: page
title: schedule
permalink: /schedule/
nav: true
nav_order: 5
description: What we read each week, and who is doing what.
---

Who does what each week lives in {% include course/signup_link.liquid text="the shared sign-up sheet" %}: add one row per week (week, your GitHub username, task) and change it whenever you like. Its *Week check* tab shows, per week, which major tasks still need people and which are over their limit. If your change would break a rule, switch with someone instead.

<div class="reading-status" id="reading-status" hidden>
  <div><span class="label">Read</span> <span data-slot="read"></span></div>
  <div><span class="label">Upcoming meeting</span> <span data-slot="current"></span></div>
  <div><span class="label">After that</span> <span data-slot="next"></span></div>
  <div><span class="label">Planned later</span> <span data-slot="planned"></span></div>
</div>

The papers come from `_data/schedule.yml`, the only place to change them. The sign-up sheet's *Papers* tab reads the same list from [schedule.csv]({{ '/schedule.csv' | relative_url }}).

{% for w in site.data.schedule %}
{%- assign paper = site.papers | where: 'slug', w.paper | first -%}

<div class="schedule-week" data-week="{{ w.week }}"{% if paper %} data-paper-title="{{ paper.short | default: paper.title | escape }}" data-paper-url="{{ paper.url | relative_url }}"{% endif %}>
  <div class="week-head">
    <span>Week {{ w.week }}: {% if paper %}<a href="{{ paper.url | relative_url }}">{{ paper.title }}</a>{% else %}{{ w.topic }}{% endif %}</span>
    <span class="week-date">{{ w.date }}</span>
  </div>
  {% if paper and w.topic %}<div class="muted">{{ w.topic }}</div>{% endif %}
  {% if w.notes %}<div>{{ w.notes }}</div>{% endif %}
  {% include course/week_roles.liquid week=w.week %}
</div>
{% endfor %}

<script>
  // Mark the upcoming meeting (like the "now" line in a calendar), from course_start and class_day in _config.yml.
  // A week counts as read once its class day has passed; the upcoming meeting is the first one today or later.
  (function () {
    var start = new Date("{{ site.course_start | date: '%Y-%m-%d' }}T00:00:00");
    var first = {{ site.first_week_number | default: 0 }};
    var classDay = {{ site.class_day | default: 0 }};
    var now = new Date(), today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    var days = Math.round((today - start) / (24 * 3600 * 1000));
    var current = first + Math.max(0, Math.ceil((days - classDay) / 7));
    var weeks = document.querySelectorAll(".schedule-week[data-week]");
    var last = weeks.length ? +weeks[weeks.length - 1].dataset.week : first;
    current = Math.min(current, last);
    weeks.forEach(function (el) {
      var w = +el.dataset.week;
      if (w < current) el.classList.add("is-past");
      if (w === current) {
        el.classList.add("is-current");
        var head = el.querySelector(".week-head span");
        if (head) head.insertAdjacentHTML("afterbegin", '<span class="now-badge">Upcoming meeting</span> ');
      }
    });

    // The status box at the top: read / upcoming meeting / after that / planned later.
    var box = document.getElementById("reading-status");
    var slots = { read: [], current: [], next: [], planned: [] };
    weeks.forEach(function (el) {
      if (!el.dataset.paperTitle) return;
      var w = +el.dataset.week;
      var slot = w < current ? "read" : w === current ? "current" : w === current + 1 ? "next" : "planned";
      slots[slot].push(el);
    });
    Object.keys(slots).forEach(function (k) {
      var target = box.querySelector('[data-slot="' + k + '"]');
      if (!slots[k].length) {
        target.innerHTML = '<span class="muted">not chosen yet</span>';
        return;
      }
      slots[k].forEach(function (el, i) {
        if (i) target.appendChild(document.createTextNode(" · "));
        var a = document.createElement("a");
        a.href = el.dataset.paperUrl;
        a.textContent = el.dataset.paperTitle;
        target.appendChild(a);
        target.appendChild(document.createTextNode(" (week " + el.dataset.week + ")"));
      });
    });
    box.hidden = false;
  })();
</script>
