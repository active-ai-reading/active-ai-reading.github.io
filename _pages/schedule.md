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
  <div><span class="label">This week</span> <span data-slot="current"></span></div>
  <div><span class="label">Next</span> <span data-slot="next"></span></div>
  <div><span class="label">Planned after</span> <span data-slot="planned"></span></div>
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
  // Highlight the current week (like the "now" line in a calendar), from course_start in _config.yml.
  (function () {
    var start = new Date("{{ site.course_start | date: '%Y-%m-%d' }}T00:00:00");
    var first = {{ site.first_week_number | default: 0 }};
    var now = new Date(), day = 24 * 3600 * 1000;
    var current = first + Math.floor((now - start) / (7 * day));
    var weeks = document.querySelectorAll(".schedule-week[data-week]");
    var last = weeks.length ? +weeks[weeks.length - 1].dataset.week : first;
    current = Math.max(first, Math.min(current, last));
    weeks.forEach(function (el) {
      var w = +el.dataset.week;
      if (w < current) el.classList.add("is-past");
      if (w === current) {
        el.classList.add("is-current");
        var head = el.querySelector(".week-head span");
        if (head) head.insertAdjacentHTML("afterbegin", '<span class="now-badge">This week</span> ');
        if (!location.hash) el.scrollIntoView({ block: "center" });
      }
    });

    // The status box: read / this week / next / planned after, from the same weeks.
    var box = document.getElementById("reading-status");
    function link(el) {
      if (!el.dataset.paperTitle) return null;
      return '<a href="' + el.dataset.paperUrl + '">' + el.dataset.paperTitle + "</a> (week " + el.dataset.week + ")";
    }
    var slots = { read: [], current: [], next: [], planned: [] };
    weeks.forEach(function (el) {
      var w = +el.dataset.week, a = link(el);
      if (!a) return;
      if (w < current) slots.read.push(a);
      else if (w === current) slots.current.push(a);
      else if (w === current + 1) slots.next.push(a);
      else slots.planned.push(a);
    });
    Object.keys(slots).forEach(function (k) {
      box.querySelector('[data-slot="' + k + '"]').innerHTML = slots[k].join(" · ") || '<span class="muted">not chosen yet</span>';
    });
    box.hidden = false;
  })();
</script>
