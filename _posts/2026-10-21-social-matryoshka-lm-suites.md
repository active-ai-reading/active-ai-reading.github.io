---
title: "Matryoshka Language Model Suites in a thread"
description: Social media posts for Matryoshka Language Model Suites.
paper: matryoshka-lm-suites
role: communication
task: social
by: [Shueyr]
---

## X / Twitter

> Three language models. One training run. 36% less training compute.
>
> Matryoshka nests 500M, 1.5B and 3B LMs together and gets nearly the same benchmark accuracy as training each one separately.

> 2/ Think nesting dolls, but for Transformers.
>
> Each larger LM builds on the smaller one. Each size has its own width, depth and output head, so you can deploy the 500M or 1.5B model without loading the full 3B model.

> 3/ The clever part: the 3B LM teaches the smaller ones *during the same training run*. No separate teacher pass.
>
> At inference, shared layers and KV cache give 26% higher greedy speculative-decoding throughput than a separate 500M/3B pair in the reported A100 test.

> 4/ And the accuracy cost? At most 0.5 percentage points on average across 7 zero-shot benchmarks, at each model size.
>
> Three deployable models. 38% fewer total parameters to store.
>
> Paper: https://arxiv.org/abs/2608.09703

## Bluesky

> Why train 3 LMs separately? Matryoshka nests 500M, 1.5B and 3B models in one stack: 36% less training compute, with average zero-shot accuracy within 0.5 points of separate models. Shared KV cache also boosts speculative-decoding throughput by 26% in an A100 test. https://arxiv.org/abs/2608.09703

## Mastodon

> Three LMs. One training run.
>
> Godey & Artzi's Matryoshka suite nests 500M, 1.5B and 3B models instead of training each separately.
>
> Result: 36% less training compute, average benchmark accuracy within 0.5 points, and 26% higher greedy speculative-decoding throughput than a separate draft/verifier pair in an A100 test.
>
> Each model can still be deployed independently.
>
> https://arxiv.org/abs/2608.09703 #NLProc #MachineLearning

## LinkedIn

> If you train language models in several sizes, why train each one from scratch?
>
> *Matryoshka Language Model Suites*, by Nathan Godey and Yoav Artzi, nests 500M, 1.5B and 3B models into one architecture. Train them together, then deploy any size independently, with its own width, depth and KV cache.
>
> **The payoff:** 36% less total training compute, while average accuracy stays within 0.5 percentage points of separately trained models across seven zero-shot benchmarks. Shared layers also make speculative decoding more efficient: **26% higher greedy throughput** than a separate 500M/3B draft and verifier pair in the reported A100 setup.
>
> The bigger idea: optimize the *whole model family*, not just the largest checkpoint. The results are promising, though so far tested only up to 3B parameters.
>
> Paper: https://arxiv.org/abs/2608.09703
