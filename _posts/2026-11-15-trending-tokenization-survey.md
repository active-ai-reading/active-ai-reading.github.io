---
title: "Papers worth knowing this week"
description: Traditional tokenizers rely on fixed vocabularies, which can limit their ability to adapt to new domains and languages. These two papers explore alternative approaches to make tokenization more flexible and efficient.
paper: tokenization-survey
role: scouting
task: trending
by: [odedorenstein]
---

### 1. [FLEXITOKENS: Flexible Tokenization for Evolving Language Models (Owodunni et al., 2026)](https://aclanthology.org/2026.findings-acl.848/)

This paper introduces a learnable tokenizer that operates directly on bytes and produces variable-length segments. It explores how tokenization can adapt to different inputs rather than relying on a fixed segmentation strategy.

### 2. [Equity with Efficiency: An Empirical Study of Tokenizers for Multilingual Large Language Models (Wei et al., 2026)](https://aclanthology.org/2026.emnlp-main.1783/)

This paper investigates why tokenizers often represent some languages less efficiently than others. It compares alternative tokenization strategies and explores how to improve multilingual efficiency without sacrificing downstream performance.

Together, these papers show that tokenizer design can influence both model efficiency and its ability to handle diverse languages.
