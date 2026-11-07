---
title: "Papers worth knowing this week"
description: Relevant latent reasoning papers
paper: recurrent-depth-latent-reasoning
role: scouting
task: hidden-gems
by: [gilk717]
---
## Papers worth knowing this week

- **[Latent Recurrent Thoughts: Recurrent Refinement of Proposed Latents for Reasoning with Frozen LLMs (Chen & Fu, September 2026)](https://arxiv.org/abs/2609.01117):** Introduces a lightweight, task-specific recurrent network that iteratively refines continuous reasoning representations while keeping the underlying LLM frozen. The approach improves reasoning on symbolic and natural-language tasks by training only a small fraction of the model's parameters, without requiring explicit reasoning traces for symbolic tasks.

- **[Latent Reasoning with Supervised Thinking States (Amos et al., February 2026)](https://arxiv.org/abs/2602.08332):** Proposes generating intermediate natural-language thoughts, compressing them into continuous hidden states, and feeding them into subsequent computations without extending the LLM's context. By supervising these thoughts using Chain-of-Thought examples, the method enables efficient parallel training and faster inference while retaining much of the reasoning accuracy of explicit CoT.
