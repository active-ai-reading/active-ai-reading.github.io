---
title: "Copyediting Section 1 (Introduction) of Matryoshka Language Model Suites"
description: Removing repetition
paper: matryoshka-lm-suites
role: writing
task: copyedit
by: [shaharOssy]
---


## What I changed and why

The original introduction repeats its three main points (stacking, distillation, speculative decoding) three times: in the middle paragraphs, in a summary paragraph, and finally in the bullet points. For example: "...the nested structure further **benefits speculative decoding**", and then: "Moreover, the shared-weight structure and low-cost distillation substantially improves cross-model agreement and **makes larger draft models practical for speculative decoding."** and then: "We demonstrate that the shared-weight structure and low-cost distillation substantially improve cross-model agreement and **make larger drafts practical for speculative decoding..."**

This makes it longer than it needs to be. I removed the repetition by deleting the redundant sentences in the summary paragraph—keeping only the unique details like the dataset and code release—and leaving the original bullet points intact. I also simplified the opening sentence so it gets straight to the engineering problem without using passive language.

## Before and after

<div class="before-after">
<div class="before" markdown="1">
<span class="label">Before</span>

The way training and inference costs of large language models (LLMs) scale steeply with model size creates a demand for models across a broad spectrum of sizes, from 100M [Allal et al., 2025] to trillion [DeepSeek-AI, 2026] parameters, for diverse deployment scenarios. Delivering models from different scales allows for different load/performance tradeoffs, with smaller models being more memory- and compute-efficient than their larger counterparts. As a result, models are usually released in suites: groups of models trained separately on similar data, with smaller models often distilled from larger ones in the suite. The question of efficiency in training and serving model suites jointly is rarely studied. We propose a training framework that is particularly well-suited to the model-suite paradigm and offers several concrete benefits over the standard approach.

Instead of training separate models, our approach progressively stacks the outputs of smaller sub-models as inputs to larger ones. For instance, rather than training a {1B, 8B, 30B, 70B} suite as four independent runs, our method trains a single architecture combining a 1B sub-model with additional 7B, 22B, and 40B parameter blocks, resulting in 70B trained parameters instead of 109B. Contrarily to previous work [Devvrit et al., 2023], each sub-model can be detached as a standalone language model, with its own depth and KV cache footprint, and served independently just like a regular checkpoint. This setup also makes distillation from the largest model to all smaller ones a natural by-product, as logits from all submodels are available during training. As a result, training the Matryoshka suite costs on the same order as training only the largest model alone, and delivers all N sub-models in a single run, with cheap knowledge distillation.

At inference time, the nested structure further benefits speculative decoding [Leviathan et al., 2023]: the draft model is nested in the verifier model, and both already share KV cache, eliminating the usual memory overhead of maintaining a separate draft model. Cross-model prediction agreement is also higher than in independently trained suites, directly increasing token acceptance rates.

We verify our approach by training a 3B-parameter Matryoshka suite with 500M, 1.5B, and 3B sub-models on 35B tokens from the FineWeb-Edu dataset. Our suite matches independently trained baselines on validation perplexity, out-of-domain perplexity, and benchmark performance while using 36% less total training compute. Moreover, the shared-weight structure and low-cost distillation substantially improves cross-model agreement and makes larger draft models practical for speculative decoding. We also conduct an extensive analysis of architectural design, and show the impact of width and depth configurations in Matryoshka suites, and that both the distillation loss and our model junction mechanism are crucial for the performance of smaller sub-models. We release trained checkpoints and a HuggingFace's transformers-compatible implementation.

Overall, our contributions can be summarized as:

* We introduce Matryoshka Language Model Suites, a pretraining framework that nests sub-models of increasing width and depth into a single jointly trained architecture (Section 2);

* We derive a low-cost distillation objective that leverages the availability of all sub-model logits at every forward pass;

* We train a 3B-parameter Matryoshka suite and show it reaches near-parity (within 0.5 average points at every size) with independently trained baselines on standard benchmarks while using 36% less training compute (Section 3);

* We demonstrate that the shared-weight structure and low-cost distillation substantially improve cross-model agreement and make larger drafts practical for speculative decoding, where plain vanilla speculative decoding barely improves over autoregressive inference.

* We provide extensive ablations at smaller scale (50M/100M/200M suite) that provide insights for architectural hyperparameters and training objectives.
</div>

<div class="after" markdown="1">
<span class="label">After</span>

The steep training and inference costs of large language models (LLMs) create a demand for models across a broad spectrum of sizes, from 100M [Allal et al., 2025] to trillion [DeepSeek-AI, 2026] parameters. As a result, models are usually released in suites: groups of models trained separately on similar data, with smaller models often distilled from larger ones. The question of efficiency in training and serving model suites jointly is rarely studied. We propose a training framework that offers several concrete benefits over the standard approach.

Instead of training separate models, our approach progressively stacks the outputs of smaller sub-models as inputs to larger ones. For instance, rather than training a {1B, 8B, 30B, 70B} suite as four independent runs, our method trains a single architecture resulting in 70B trained parameters instead of 109B. Contrarily to previous work [Devvrit et al., 2023], each sub-model can be detached as a standalone language model, with its own depth and KV cache footprint, and served independently. This setup also makes distillation from the largest model to all smaller ones a natural by-product, as logits from all submodels are available during training.

At inference time, the nested structure further benefits speculative decoding [Leviathan et al., 2023]: the draft model is nested in the verifier model, and both already share KV cache, eliminating the usual memory overhead of maintaining a separate draft model. Cross-model prediction agreement is also higher than in independently trained suites, directly increasing token acceptance rates.

Overall, our contributions can be summarized as:

* We introduce Matryoshka Language Model Suites, a pretraining framework that nests sub-models of increasing width and depth into a single jointly trained architecture (Section 2);

* We derive a low-cost distillation objective that leverages the availability of all sub-model logits at every forward pass;

* We train a 3B-parameter Matryoshka suite on 35B tokens from the FineWeb-Edu dataset and show it reaches near-parity (within 0.5 average points at every size) with independently trained baselines on standard benchmarks while using 36% less training compute (Section 3);

* We demonstrate that the shared-weight structure and low-cost distillation substantially improve cross-model agreement and make larger drafts practical for speculative decoding, where plain vanilla speculative decoding barely improves over autoregressive inference.

* We provide extensive ablations at smaller scale (50M/100M/200M suite) that provide insights for architectural hyperparameters and training objectives.

* We release trained checkpoints and a HuggingFace's transformers-compatible implementation.
</div>
</div>

## The general rule

Don't repeat your summary. If you explain your main points in the text, you don't need to summarize them again right before the bullet points. Remove sentences that state the obvious or repeat facts already mentioned.
