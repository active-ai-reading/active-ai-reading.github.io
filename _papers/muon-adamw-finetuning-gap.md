---
title: Pretraining Data Scale Reverses the Muon-AdamW Fine-Tuning Gap
short: Muon vs AdamW after fine-tuning
authors: Catherine Li, Jingchu Gai, Andrej Risteski, Jacob Mitchell Springer, Aditi Raghunathan
year: 2026
arxiv: "2611.03633"
license: CC BY 4.0
tldr: >
  (To be written by the class after week 7. Edit this file: one or two sentences someone can read in 10 seconds.)
tags: [optimizers, muon, fine-tuning, forgetting]
---

Tentative for week 7: that day (13 Dec) has a guest lecture on visualization, so this paper might be postponed.

## Background: what Muon and Adam are doing

The paper treats Muon as a given. To understand why the two optimizers end up so different, read first:

- [Old Optimizer, New Norm: An Anthology](https://arxiv.org/abs/2409.20325): Adam (without its moving averages) is steepest descent under one norm and Muon under another, the spectral norm. This explains why Muon orthogonalizes its updates and what Adam does to each coordinate.
- [Muon: An optimizer for hidden layers in neural networks](https://kellerjordan.github.io/posts/muon/): the blog post that introduced Muon.

## For more reading

- [Muon Outperforms Adam in Tail-End Associative Memory Learning](https://arxiv.org/abs/2509.26030): the same toy model (one linear associative memory layer), used to show Muon's advantage: it learns rare facts as well as frequent ones.
- [Overtrained Language Models Are Harder to Fine-Tune](https://arxiv.org/abs/2503.19206): the earlier finding from the same group that more pretraining can make a model worse after fine-tuning, which this paper revisits from the optimizer side.
- Week 5's [spurious forgetting](/papers/spurious-forgetting/) paper and its reading list on forgetting and plasticity.
