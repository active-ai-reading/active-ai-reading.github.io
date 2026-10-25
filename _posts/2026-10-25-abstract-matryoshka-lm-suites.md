---
title: "Rewriting the abstract of Matryoshka Language Model Suites"
description: "Making the comparisons clearer, with a trade-off in technical detail."
paper: matryoshka-lm-suites
role: writing
task: abstract
by: [chanoch1234]
---

## What I changed and why

I tried to make the motivation and comparisons clearer, especially what the compute savings and speedup are measured against. I also clarified that accuracy is averaged across benchmarks and separated the training and decoding results. The result is more technical, and I’m not sure it is better than the original, but I think the comparisons are easier to understand.

## Before

Training a language model suite classically requires training each model separately and serving them independently. We improve both training and inference efficiency by stacking sub-models of increasing size into a single nested architecture trained end-to-end. This Matryoshka training framework reduces the total parameter count of the suite, enables low-cost distillation from the largest to all smaller sub-models at every training step, and is well-suited for speculative decoding as the draft model is contained within the verifier. We validate our approach by training a Matryoshka suite comprising 500M, 1.5B, and 3B sub-models. Our suite is on par with independently trained baselines on benchmark performance and validation and out-of-domain perplexities, while using 36% less training compute and improving the throughput of speculative decoding by 14–26%. We also ablate key architectural choices, offering guidance for building strong Matryoshka LM suites.

## After

Language model suites accommodate different resource budgets, but their members are typically trained independently. We introduce Matryoshka Language Model Suites, an end-to-end framework that nests smaller models within larger ones through shared Transformer blocks, with widths and depths tailored to each model size. This reduces the suite’s total parameter count and enables low-cost online distillation from the largest model to smaller models. Shared blocks and KV caches also support speculative decoding. We train a suite comprising 500M, 1.5B, and 3B models that achieves near-parity with token-matched, independently trained baselines in average benchmark accuracy and validation and out-of-domain perplexity, while using 36% less total suite-training compute. With a 500M draft and 3B verifier, speculative-decoding throughput increases by 14–26% over an independently trained draft–verifier pair under the same GPU-memory budget. Architectural and training ablations assess the design choices underlying these results.

Source: [Matryoshka Language Model Suites](https://arxiv.org/abs/2608.09703), Nathan Godey and Yoav Artzi.
