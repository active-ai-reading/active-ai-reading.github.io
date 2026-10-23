---
title: Visualizing 🪆 Models
description: Diagrams of the nested model suite and its junction mechanism.
paper: matryoshka-lm-suites
role: visualization
task: key-visual
by: [IdoRavid]
---

## Architecture
The suggested Matryoshka Architecture Suite, outlined in the paper, essentially builds
nested sub-models, such that each one is composed of its predecessors:

<div style="position: relative; left: 50%; transform: translateX(-50%); width: min(1280px, calc(100vw - 2rem)); aspect-ratio: 16 / 9; margin: 1.5rem 0;">
  <iframe
    src="{{ '/assets/html/visualizing-matryoshka-slide1.html' | relative_url }}"
    title="Interactive comparison of Matryoshka and independent model suites"
    style="position: absolute; inset: 0; width: 100%; height: 100%; border: 0;"
    loading="lazy"
  ></iframe>
</div>


## The Junction Mechanism

To deal with the size mismatch between the different submodels, they suggest the following
"Junction" mechanism:

<figure style="position: relative; left: 50%; transform: translateX(-50%); width: min(1280px, calc(100vw - 2rem)); margin: 1.5rem 0;">
  <img
    src="{{ '/assets/img/posts/visualizing-matryoshka/slide2-junction.svg' | relative_url }}"
    alt="Junction J matches the old output norm to a fresh embedding, concatenates their 1024 and 1280 channels, then sends a 2304-channel vector to the next stage."
    style="display: block; width: 100%; height: auto;"
    loading="lazy"
  >
</figure>


We do 2 things here:

1. match the norm of the output, to the norm of the next sub-models' embedding of the input.
2. concat the normalized output from the previous model, to the input embedding, and feed both to the next submodel.

## The Key Idea
The nested structure that we visualized here, is what allows the Matryushka models to be modular -
we essentially trained one model (the largest one), and recieved the smaller models "for free" (hence the 36% reduction in training compute). The benefits
of the structure are also related to sharing the KV-cache,and allowing for easier inter-model tasks, namely Speculative Decoding and Model Distillation.
