---
title: "Beyond Fixed Tokenization: New Strategies"
description: "Two papers extending the survey's discussion: one addressing the noted limitations of byte-level generation, and the other further exploring the claim of why fewer tokens don't necessarily mean greater efficiency."
paper: tokenization-survey
role: scouting
task: trending
by: [chenshani-droid]
---

This week's survey discusses several limitations of traditional subword tokenization, including its reliance on fixed vocabularies and segmentation rules that cannot adapt during model training, as well as challenges in generalizing across languages. It also explores alternative approaches, such as byte-level modeling, and highlights the trade-off between sequence length, model performance, and computational cost - emphasizing that fewer tokens do not necessarily mean faster or better models.

The following two papers build on these ideas: the first addresses the computational limitations of byte-level generation, while the second further investigates how tokenization choices affect model efficiency.

### 1. [Fast Byte Latent Transformer (Kallini et al., 2026)](https://arxiv.org/abs/2605.08044)

This paper makes byte-level language models faster at generating text by allowing them to predict multiple bytes at once, rather than generating them one by one. The survey discusses Byte Latent Transformer (BLT) as an alternative to traditional subword tokenization, but highlights the computational challenges of byte-level generation. This paper builds on BLT and proposes techniques to make generation more efficient.

### 2. [Compute Optimal Tokenization (Limisiewicz et al., 2026)](https://arxiv.org/abs/2605.01188)

This paper investigates how the amount of text represented by each token affects language model efficiency, showing that the optimal degree of token compression (token size) depends on the available computational budget. The survey emphasizes that shorter token sequences do not necessarily mean faster or better models. This paper investigates that trade-off and shows why choosing the right tokenization strategy matters for efficient model training.
