---
layout: page
title: feature showcase
permalink: /showcase/
nav: false
sitemap: false
description: Everything a post on this site can do, with copyable source.
---

Each page below demonstrates one feature of the site's theme ([al-folio](https://github.com/alshedivat/al-folio)). Open a page to see it, then open its source in [`_showcase/`](https://github.com/{{ site.github_repo }}/tree/main/_showcase) and copy what you need into your post.

<ul>
{% assign items = site.showcase | sort: 'title' %}
{% for s in items %}
  <li><a href="{{ s.url | relative_url }}">{{ s.title | remove: 'a post with ' | capitalize }}</a> <span class="muted">({{ s.path | remove: '_showcase/' }})</span></li>
{% endfor %}
</ul>
