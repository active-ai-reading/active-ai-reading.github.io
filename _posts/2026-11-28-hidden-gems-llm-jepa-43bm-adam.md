---
title: "Papers worth knowing this week"
description: More JEPAs in Language and looped transformer distiliation.
paper: llm-jepa
task: hidden-gems
by: AdamJaber03
---

## ["BERT-JEPA: Reorganizing CLS Embeddings for Language-Invariant Semantics"](https://arxiv.org/abs/2601.00366)
Taj Gillin, Adam Lalani, Kenneth Zhang, Marcel Mateos Salles, 2026.

This paper uses multilingual parallel documents to train a BERT language model and applies the JEPA objective to the CLS token embedding. The authors show demonstrate that this added objective helps create a more language-agnostic embedding, benificial for various downstream tasks.


## ["Learning from Recurrence: Internalizing Depth-Induced Preferences in Looped Language Models"](https://arxiv.org/abs/2611.33468)
Hui Chen, Joshua Elsdon, Can Goksen, 2026.

This paper relates to our recent discussion on looped transformers and latent reasoning. The authors show that deep recurrence often redistributes the probability the model assigns across the same leading options; therefore, distilling later recurrences into earlier ones can provide a better learning signal.
