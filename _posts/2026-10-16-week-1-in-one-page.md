---
title: "Week 0 in one page: tokens keep knowledge apart"
description: The paper, what we learned, and everything the class wrote about it, in a five-minute read.
paper: cross-lingual-knowledge-pretraining
role: communication
task: compile
by: [course-team]
example: true
og_image: https://active-ai-reading.github.io/assets/img/papers/cross-lingual-knowledge-pretraining/figure1.png
---

{% include figure.liquid path="assets/img/papers/cross-lingual-knowledge-pretraining/figure1.png" class="img-fluid rounded z-depth-1" caption="Figure 1 of the paper (CC BY 4.0). Left: knowledge transfer (CLeq) for English–Arabic models under different methods. Right: English perplexity." %}

## The paper in three sentences

LLMs that learn a fact in one language mostly don't know it in another, and Gaber et al. show this starts during pretraining {% cite gaber2026crosslingual %}. Their cleanest experiment trains on two identical copies of English that differ only in token IDs, and finds the copies share essentially no knowledge. Mapping Arabic word by word into English tokens raises transfer 14×, but only when the mapping preserves meaning.

## What we wrote

**✍️ Writing.** The abstract buries its best result in sentence six; [our rewrite]({{ '/posts/2026/rewriting-the-abstract/' | relative_url }}) leads with it and puts numbers up front. [Three things to remember]({{ '/posts/2026/three-things-to-remember/' | relative_url }}) checks whether the abstract, Figure 1 and the intro actually deliver the main points (the most original one, clone languages, is missing from Figure 1).

**🧠 Learning.** [Fictive facts]({{ '/posts/2026/fictive-facts/' | relative_url }}) explains the trick that makes the whole paper possible: invent facts so you know exactly how often the model saw them.

**📊 Visualization.** [A better Figure 2]({{ '/posts/2026/a-better-figure-2/' | relative_url }}) plots the appendix's soft-mapping sweep as curves, revealing that natural languages need far more embedding sharing than clones before knowledge flows. [The core idea in one picture]({{ '/posts/2026/the-core-idea-in-one-picture/' | relative_url }}) draws the three setups token by token.

**🔬 Research.** The [critique]({{ '/posts/2026/critique/' | relative_url }}): accept, with a clean diagnosis but framing stronger than the evidence. The [literature map]({{ '/posts/2026/literature-map/' | relative_url }}) places it among cloned-language studies, fictive-fact injection, and the vocabulary-overlap debate. [Five follow-ups]({{ '/posts/2026/follow-ups-worth-doing/' | relative_url }}) range from a weekend simulation to a thesis chapter.

**💻 Coding.** [Reimplementing CLeq]({{ '/posts/2026/reimplementing-cleq/' | relative_url }}) simulates the metric with a known answer: exact at 0% and 100%, generous in between, about ±2 points of noise per run.

**📣 Communication.** [The paper in four feeds]({{ '/posts/2026/the-paper-in-four-feeds/' | relative_url }}): ready-to-post versions for X, Bluesky, Mastodon and LinkedIn.

## What we argued about in class

*(Fill in after class: the disagreements are the most interesting part.)*

- Is "disjoint tokens are sufficient" the same as "disjoint tokens are the cause"?
- Should Figure 1 show the diagnosis or the fix?
- How literally should we read a CLeq of 12.6%?
