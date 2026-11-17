---
layout: page
title: papers
permalink: /papers/
nav: true
nav_order: 1
description: Every paper the course reads, latest week first, with everything the class wrote about it.
---

{% include course/paper_grid.liquid %}

<p class="muted">Adding a paper: <code>python bin/add_paper.py &lt;arXiv id&gt; --week &lt;n&gt;</code> writes <code>_papers/&lt;short-id&gt;.md</code> from arXiv and puts it on the schedule. Or copy <code>templates/paper.md</code> by hand. See the <a href="{{ '/guide/' | relative_url }}">guide</a>.</p>
