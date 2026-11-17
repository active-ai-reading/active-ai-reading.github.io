---
title: "LLM-JEPA: Large Language Models Meet Joint Embedding Predictive Architectures"
short: LLM-JEPA
authors: Hai Huang, Yann LeCun, Randall Balestriero
year: 2025
arxiv: "2509.14252"
code: https://github.com/rbalestr-lab/llm-jepa
license: CC BY-NC-SA 4.0
tldr: >
  (To be written by the class after week 6. Edit this file: one or two sentences someone can read in 10 seconds.)
tags: [jepa, self-supervised learning, fine-tuning, pretraining]
---

## For more reading

- [Semantic Tube Prediction: Beating LLM Data Efficiency with JEPA](https://arxiv.org/abs/2602.22617): the same lab's follow-up. It needs no paired views and claims the same accuracy with 16x less data on NL-RX-SYNTH.

The arguments against:

- [Representation Without Reward: A JEPA Audit for LLM Fine-Tuning](https://arxiv.org/abs/2605.15394): 22 JEPA-style auxiliary losses change the hidden-state geometry, but none improves task accuracy beyond seed noise.
- [The JEPA Paradox in Language: The Geometry of Linguistic Alternatives](https://arxiv.org/abs/2607.23531): text often has several valid completions, so predicting a single embedding averages them into a point that matches none.
