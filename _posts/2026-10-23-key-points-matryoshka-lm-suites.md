---
title: "Copyediting Section 1 (Introduction) of Matryoshka Language Model Suites"
description: Fixing the repetitive structure and turning passive academic prose into a more direct pitch.
paper: matryoshka-lm-suites
role: writing
task: copyedit
by: shaharOssy
---

## What I changed and why

When reading the original introduction, I felt a bit of déjà vu. The authors explain their three main ideas in the second paragraph, summarize them again in the fourth paragraph, and then list them *again* in the bullet points at the end. It's exhausting for the reader. I also noticed the opening sentence was really passive and clunky ("The way training and inference costs... scale steeply... creates a demand..."). 

I merged the repetitive paragraphs directly into the final bullet points to cut out the filler, and rewrote the opening to focus directly on the actual engineering problem developers face. 

## Before and after

<div class="before-after">
  <div class="before"><span class="label">Before</span>

The way training and inference costs of large language models (LLMs) scale steeply with model size creates a demand for models across a broad spectrum of sizes, from 100M [Allal et al., 2025] to trillion [DeepSeek-AI, 2026] parameters, for diverse deployment scenarios. Delivering models from different scales allows for different load/performance tradeoffs, with smaller models being more memory- and compute-efficient than their larger counterparts. As a result, models are usually released in suites: groups of models trained separately on similar data, with smaller models often distilled from larger ones in the suite. The question of efficiency in training and serving model suites jointly is rarely studied. We propose a training framework that is particularly well-suited to the model-suite paradigm and offers several concrete benefits over the standard approach.

Instead of training separate models, our approach progressively stacks the outputs of smaller sub-models as inputs to larger ones. For instance, rather than training a {1B, 8B, 30B, 70B} suite as four independent runs, our method trains a single architecture combining a 1B sub-model with additional 7B, 22B, and 40B parameter blocks, resulting in 70B trained parameters instead of 109B. Contrarily to previous work [Devvrit et al., 2023], each sub-model can be detached as a standalone language model, with its own depth and KV cache footprint, and served independently just like a regular checkpoint. This setup also makes distillation from the largest model to all smaller ones a natural by-product, as logits from all submodels are available during training. As a result, training the Matryoshka suite costs on the same order as training only the largest model alone, and delivers all N sub-models in a single run, with cheap knowledge distillation.

At inference time, the nested structure further benefits speculative decoding [Leviathan et al., 2023]: the draft model is nested in the verifier model, and both already share KV cache, eliminating the usual memory overhead of maintaining a separate draft model. Cross-model prediction agreement is also higher than in independently trained suites, directly increasing token acceptance rates.

We verify our approach by training a 3B-parameter Matryoshka suite with 500M, 1.5B, and 3B sub-models on 35B tokens from the FineWeb-Edu dataset. Our suite matches independently trained baselines on validation perplexity, out-of-domain perplexity, and benchmark performance while using 36% less total training compute. Moreover, the shared-weight structure and low-cost distillation substantially improves cross-model agreement and makes larger draft models practical for speculative decoding. We also conduct an extensive analysis of architectural design, and show the impact of width and depth configurations in Matryoshka suites, and that both the distillation loss and our model junction mechanism are crucial for the performance of smaller sub-models. We release trained checkpoints and a HuggingFace's transformers-compatible implementation.

Overall, our contributions can be summarized as:
• We introduce Matryoshka Language Model Suites, a pretraining framework that nests sub-models of increasing width and depth into a single jointly trained architecture (Section 2);
• We derive a low-cost distillation objective that leverages the availability of all sub-model logits at every forward pass;
• We train a 3B-parameter Matryoshka suite and show it reaches near-parity (within 0.5 average points at every size) with independently trained baselines on standard benchmarks while using 36% less training compute (Section 3);
• We demonstrate that the shared-weight structure and low-cost distillation substantially improve cross-model agreement and make larger drafts practical for speculative decoding, where plain vanilla speculative decoding barely improves over autoregressive inference.
• We provide extensive ablations at smaller scale (50M/100M/200M suite) that provide insights for architectural hyperparameters and training objectives.

  </div>
  <div class="after"><span class="label">After</span>

Because training and inference costs for large language models scale so steeply, developers rely on model families spanning everything from 100M to a trillion parameters. Releasing these models in "suites"—families of different sizes trained on the same data—is standard practice. But the way we build them is surprisingly inefficient: each model is trained in isolation, and transferring knowledge from large to small models requires expensive offline storage or parallel forward passes.

We propose Matryoshka Language Model Suites, a framework that trains an entire model family in a single nested architecture. Instead of running separate training jobs, we feed the outputs of smaller sub-models into wider, deeper transformer blocks. For example, rather than training a {1B, 8B, 30B, 70B} suite across four independent runs, we stack 7B, 22B, and 40B blocks on top of a 1B base, training just 70B parameters in one pass. Unlike previous architectures that only change the width, each Matryoshka sub-model has its own width *and* depth. You can detach any size and serve it as an independent checkpoint with a proportionally smaller KV-cache.

This shared backbone provides two major advantages:
1. **Free Online Distillation:** One forward pass through the full model generates predictions for every sub-model, meaning the largest model distills knowledge into the smaller ones at every training step for free.
2. **Better Speculative Decoding:** Normally, a separate draft model wastes GPU memory and duplicates the KV-cache. Here, smaller sub-models already live inside the verifier and share early layers. This eliminates the memory overhead and increases prediction agreement, making larger draft models practical.

We validated this on a 3B Matryoshka suite (500M, 1.5B, 3B) using 35B tokens from FineWeb-Edu. Our checkpoints and code are public. In short, our main contributions are:

* **End-to-End Architecture (Sec 2):** A parameter-free junction that rescales norms across hidden dimensions, combined with an integrated distillation loss across all exits.
* **Parity at 36% Less Compute (Sec 3.2.1):** Our 3B suite matches independently trained baselines within 0.5 accuracy points across standard benchmarks, but uses 36% less training compute.
* **Faster Speculative Decoding (Sec 3.2.2–3.2.3):** Shared weights boost token agreement by up to 5.7%, allowing a 500M-draft / 3B-verifier pair to achieve a 14–26% throughput speedup where standard speculative decoding would actually hurt latency.
* **Architectural Guidelines (Sec 3.2.5):** We map the width-depth design space and show that norm rescaling and online distillation are crucial for small sub-model performance.

  </div>
</div>

## The general rule

1. **Don't preview your preview.** If you explain the mechanism in the narrative text, save the specific numbers and section signposts for the contribution list instead of summarizing the exact same points twice in a row.
2. **Lead with the action.** Instead of passive nominalizations like *"The way X scales creates a demand for Y,"* write directly: *"Because X scales steeply, practitioners rely on Y."*
