---
title: Diffusion Language Models are Super Data Learners
short: Diffusion LMs as data learners
authors: Jinjie Ni, Qian Liu, Longxu Dou, Chao Du, Zili Wang, Hang Yan, Tianyu Pang, Michael Qizhe Shieh
year: 2025
arxiv: "2511.03276"
license: CC BY 4.0
tldr: >
  (To be written by the class after week 9. Edit this file: one or two sentences someone can read in 10 seconds.)
tags: [diffusion language models, data efficiency, scaling, pretraining]
---

## Background

- [How autoregressive and diffusion LMs imitate each other, and why it is inefficient](/posts/2026/autoregressive-vs-diffusion/): a post from this class, with pictures of how the two model types relate.

## For more reading

- [Diffusion Beats Autoregressive in Data-Constrained Settings](https://arxiv.org/abs/2507.15857): the earlier paper on the same crossover, with a formula for how much compute it takes before diffusion pulls ahead.
- [Language Diffusion Models are Associative Memories Capable of Retrieving Unseen Data](https://arxiv.org/abs/2604.26841): diffusion models behave like Hopfield networks and switch sharply from memorizing to generalizing as the dataset grows.
- [Theoretical Benefit and Limitation of Diffusion Language Model](https://arxiv.org/abs/2502.09622): parallel decoding gets fluency in a fixed number of steps, but a fully correct sequence needs steps that grow with its length.
- [Scaling Beyond Masked Diffusion Language Models](https://arxiv.org/abs/2602.15014): scaling laws for the other kinds of discrete diffusion, and why perplexity misleads when comparing them.
