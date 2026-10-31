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
{%- capture ts %}{% include course/class_date.liquid week=w.week %}{% endcapture -%}

<div class="schedule-week" data-week="{{ w.week }}" data-date="{{ ts | date: '%Y-%m-%d' }}"{% if paper %} data-paper-title="{{ paper.short | default: paper.title | escape }}" data-paper-url="{{ paper.url | relative_url }}"{% endif %}>
  <div class="week-head">
    <span>Week {{ w.week }}: {% if paper %}<a href="{{ paper.url | relative_url }}">{{ paper.title }}</a>{% else %}{{ w.topic | default: "To be decided" }}{% endif %}</span>
    <span class="week-date">{{ ts | date: "%a %-d %b %Y" }}</span>
  </div>
  {% if paper and w.topic %}<div class="muted">{{ w.topic }}</div>{% endif %}
  {% if w.notes %}<div>{{ w.notes }}</div>{% endif %}
  {% include course/week_roles.liquid week=w.week %}
</div>
{% endfor %}

<script>
  // Mark the upcoming meeting: the first class today or later (dates come from _config.yml, see
  // _includes/course/class_date.liquid). A meeting counts as read once its day has passed.
  (function () {
    var now = new Date();
    var today = now.getFullYear() + "-" + String(now.getMonth() + 1).padStart(2, "0") + "-" + String(now.getDate()).padStart(2, "0");
    var weeks = document.querySelectorAll(".schedule-week[data-week]");
    var current = weeks.length ? +weeks[weeks.length - 1].dataset.week : 0;
    for (var i = 0; i < weeks.length; i++) {
      if (weeks[i].dataset.date >= today) { current = +weeks[i].dataset.week; break; }
    }
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
