---
title: "Does sharing kv cache ruin alignment and why do we apply forward KL-Divergance"
description: 2 papers similar to parts of the paper
paper: matryoshka-lm-suites
role: scouting
task: Recent papers nobody is talking about
by: AdamGabet
---

- **[To Cache or Not to Cache: Understanding and Mitigating Safety Incompatibility in Cross-Model KV Cache Reuse](https://arxiv.org/abs/2610.15721)** (Lin, Liu, Liu & Wang, 2026): This paper shows that using the KV cache from a model in its instruct version makes it lose its safety training, meaning it stops refusing harmful requests (Llama-3-8B answers 6% -> 31%). That raises the question: does Matryoshka training keep the safety of the larger model when its sub-models share a KV cache?
- **[Divergence controls entropy in distillation](https://arxiv.org/abs/2610.03529)** (Zucchet & Linderman, 2026): This paper shows that when distilling a student model from a teacher, the choice of forward or reverse KL controls the confidence of the student model: forward KL makes it less confident than the teacher, reverse KL more confident. This might explain the stability of Matryoshka training, since its forward-KL distillation keeps the small models from collapsing onto a live teacher that is still training.

