---
title: "Papers worth knowing this week"
description: Two recent and trending papers about JEPA.
paper: llm-jepa
task: trending
by: [shniki]
---

## ["Proving and Improving the Platonic Representation Hypothesis with JEPAs"](https://arxiv.org/abs/2610.39302)
Randall Balestriero and Yann LeCun, 2026.

This paper proves the conjecture that models trained on different modalities converge to the same internal representation of the world.
They do so by training and comparing Good-View Text JEPA, Bad-View Text JEPA, standard next-token LLM, and image JPEA.
The results show the good-view model aligns with the image model far better than all others.
Furthermore, good-view training needs 42x fewer samples than next-token prediction to reach the same cross-modal alignment. 


## ["VL-JEPA: Joint Embedding Predictive Architecture for Vision-language"](https://arxiv.org/abs/2512.10942)
Delong Chen, Mustafa Shukor, Theo Moutakanni, Willy Chung, Jade Yu, Tejaswi Kasarla, Yejin Bang, Allen Bolourchi, Yann LeCun, Pascale Fung, 2025.

This paper replaces standard autoregressive text-token generation in vision-language models (VLMs) with a JEPA that predicts continuous embeddings of the target text in latent space.
The results show VL-JEPA training requires 50% fewer trainable parameters than the original VLMs.