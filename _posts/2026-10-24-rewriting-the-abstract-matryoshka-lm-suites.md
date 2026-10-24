---
title: "Rewriting the abstract"
description: Why should we care about language model suites ?
paper: matryoshka-lm-suites
role: writing
task: abstract
by: [odedorenstein]
---

<!-- Keep the sections that fit your task, delete the rest. -->

## What I changed and why

The original abstract is concise and clear, but readers unfamiliar with language model suites may not understand why they are important. 
The abstract should briefly explain the motivation for developing suites of models at different scales, so that readers can appreciate not only the contribution of this paper to the field, but also the broader significance of the problem it addresses.

## Before and after

<div class="before-after">
  <div class="before"><span class="label">Before</span>
  Training a language model suite classically requires training each model separately
  and serving them independently. We improve both training and inference efficiency
  by stacking sub-models of increasing size into a single nested architecture trained
  end-to-end. This Matryoshka training framework reduces the total parameter count
  of the suite, enables low-cost distillation from the largest to all smaller sub-models
  at every training step, and is well-suited for speculative decoding as the draft
  model is contained within the verifier. We validate our approach by training a
  Matryoshka suite comprising 500M, 1.5B, and 3B sub-models. Our suite is on par
  with independently trained baselines on benchmark performance and validation and
  out-of-domain perplexities, while using 36% less training compute and improving
  the throughput of speculative decoding by 14–26%. We also ablate key architectural
  choices, offering guidance for building strong Matryoshka LM suites.
  </div>
  <div class="after"><span class="label">After</span>
    Language model suites provide models at different scales to accommodate diverse computational and memory constraints, allowing users to choose models suited to their deployment requirements.
    Training a language model suite classically requires training each model separately
    and serving them independently. We improve both training and inference efficiency
    by stacking sub-models of increasing size into a single nested architecture trained
    end-to-end. This Matryoshka training framework reduces the total parameter count
    of the suite, enables low-cost distillation from the largest to all smaller sub-models
    at every training step, and is well-suited for speculative decoding as the draft
    model is contained within the verifier. We validate our approach by training a
    Matryoshka suite comprising 500M, 1.5B, and 3B sub-models. Our suite is on par
    with independently trained baselines on benchmark performance and validation and
    out-of-domain perplexities, while using 36% less training compute and improving
    the throughput of speculative decoding by 14–26%. We also ablate key architectural
    choices, offering guidance for building strong Matryoshka LM suites.

  </div>
</div>

## The general rule

Briefly explain why the problem your paper addresses matters, so readers understand the broader motivation before encountering the technical contribution.

<!-- For key-points: list the 3 points most readers should leave with, where the paper currently says them, and how they could be emphasized better (title? figure 1? first sentence of the intro?). -->
