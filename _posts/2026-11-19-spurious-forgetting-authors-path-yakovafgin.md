---
layout: post
title: "The authors’ path"
description: "How Vedant Palit’s work on interpretability and Bernhard Schölkopf’s research on causality connect to spurious forgetting."
paper: spurious-forgetting
role: research
task: authors
by: [yakovafgin]
---

**Vedant Palit** works on mechanistic interpretability, studying how computations inside a model shape its answers. In a [2023 study of BLIP](https://arxiv.org/abs/2308.14179) (a vision-language model), he and his coauthors traced how the model used information from an image to answer a question. In [*How Do Linear Probes Emerge?*](https://aclanthology.org/2026.emnlp-main.1728/), Palit explored a related question: which computations make a concept detectable inside a language model even when its answer never mentions it? The [current paper](https://arxiv.org/abs/2610.08718) brings that question to memory. When a model stops recalling a fact after fine-tuning, how can we tell whether it still retains that knowledge?

**Bernhard Schölkopf** is a machine learning researcher known for his work on [kernel methods](https://is.mpg.de/publications/730). He has also studied [causal inference](https://jmlr.org/papers/volume17/14-518/14-518.pdf), particularly how to uncover the mechanisms behind patterns in data. His recent work on mechanistic interpretability with Palit brings that causal perspective to language models. By changing specific parts of a model’s computation and observing the effect, they investigate which internal mechanisms explain its behavior.
