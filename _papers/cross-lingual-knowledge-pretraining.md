---
title: Why Pretraining Fails to Share Cross-Lingual Knowledge
short: Cross-lingual knowledge in pretraining
authors: Adam Gaber, Uriel Dolev, Elisabeth Fittschen, Bobby Cheng, Yuval Marton, Leshem Choshen
year: 2026
arxiv: "2609.19291"
code: https://github.com/AdamJaber03/torchtitan-mulitlingual
license: CC BY 4.0
image: /assets/img/papers/cross-lingual-knowledge-pretraining/figure1.png
og_image: https://active-ai-reading.github.io/assets/img/papers/cross-lingual-knowledge-pretraining/figure1.png # preview image when the page is shared
tldr: >
  Bilingual LLMs learn the same fact twice, once per language, and the cause is
  largely tokenization: two copies of English with disjoint token IDs already
  fail to share knowledge. Mapping Arabic words into English tokens
  (word-wise translation) makes knowledge transfer 14× better.
tags: [multilinguality, pretraining, tokenization, knowledge]
---

We read this paper together in the first class. Every post below was written as an **example** of what a task can look like, so you can copy its structure (and see how citations, figures, charts and code work on this site).
