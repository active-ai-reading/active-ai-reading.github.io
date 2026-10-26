---
title: "Visualizing Core ideas"
description: One figure showing how three separate models become one nested model, how the blocks connect, and how the smaller models learn from the largest.
paper: matryoshka-lm-suites
role: visualization
task: key-visual
by: [gilk717]
---

## Core idea

A model suite (here 500M, 1.5B and 3B parameters) is normally three separate training runs. [Godey and Artzi (2026)](https://arxiv.org/abs/2608.09703) instead stack the models into one: the 500M model is the first block, the 1.5B model is the first two blocks, and the 3B model is all three. One run trains every size, and each smaller model can be cut out and served on its own.

The idea is spread across the paper: Section 2 gives the nesting, Equation 1 the junction between blocks, Equations 2 and 3 the distillation loss, and Table 1 the sizes. The figure puts them in one place.

## The figure

{% include figure.liquid path="assets/img/posts/matryoshka-figure-1/figure.svg" class="img-fluid rounded" caption="(a) Three independent models versus one nested model. (b) The nested architecture, widths to scale (layers × width above each block). A sentence with a missing word enters the model, and each block ends in an output head that predicts the blank as a distribution over five candidate words (schematic). The largest model's distribution (graduation cap) is the teacher: its shape (dashed outlines) is passed to the two smaller models, which are trained to match it. (c) The junction: the previous block's output (o) is rescaled to the norm of a fresh embedding (e) and concatenated with it. Bar heights in (c) are illustrative." %}

## How to read it

- **(a) What is nested.** The one-run bar nests the 500M, 1.5B and 3B bars inside each other, with widths proportional to the paper's parameter counts (3.2B against 5.2B).
- **(b) How it is built.** Bar heights follow the paper's block widths (1024, 2304, 4352) and layer counts (24, 10, 5). Orange strips are fresh embedding channels added at each junction. Each exit predicts the same blank. Distillation is shown as the teacher's distribution passed one way to the smaller models, and only to them, because the paper defines the distillation term only for the smaller exits.
- **(c) How the blocks connect.** The output of one block is much larger than a fresh embedding, so it is rescaled to the embedding's norm and the two are concatenated. This adds no parameters. In the paper's 200M ablation, dropping the rescaling costs about 0.2 validation perplexity, and replacing the fresh embedding with zeros costs about 0.54.

**Results (not in the figure).** One nested run uses 36% less training compute than three independent runs, and speculative decoding is 26% faster than with an independently trained pair (greedy, draft length 6). Accuracy is within 0.5 average points of token-matched baselines, which use 57% more compute.

**Caveats.** The 3.2B vs. 5.2B count leaves out the LM heads of the two smaller exits (about 0.16B), and part of the decoding speedup comes from a larger batch fitting in memory (102 vs. 64).
