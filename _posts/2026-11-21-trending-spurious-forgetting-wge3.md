---
title: "Papers worth knowing this week"
description: A run of trending papers keeps finding the same thing — a lot of what we call "training" turns out to be one shift in activations or weights, plus a clean attention-architecture conversion that lands next to our MSAR read.
paper: spurious-forgetting
task: trending
by: dan22333
---

<!-- At least two papers, one sentence each, with a link. Grouped by the theme that ties them to what we just read. -->

**Theme this week: most of "training" is one shift.** Two of these show RL and self-improvement collapsing onto a single activation or weight edit, which lines up directly with our spurious-forgetting read (the reversible "common shift") and the JEPA audit's representation-vs-reward split. The third is the attention-architecture line we were on with MSAR.

1. **RL Post-Training in Diffusion Transformers Is Activation Steering** — A single fixed steering vector recovers 90 to 96% of the reward gain from policy-gradient RL post-training using 65× fewer parameters than LoRA, so most of what RL "learns" here is one constant activation shift. https://arxiv.org/abs/2611.26627

2. **Language Models Can Rewrite Their Own Weights** — A 27B model acts as its own optimizer, diagnosing its wrong answers and editing its own weights through forward passes only (no backprop), keeping the edits that survive a few practice problems. https://arxiv.org/abs/2611.21885

3. **On-Policy Morphing into Hybrid Attention Models** — FlashMorph2 converts a pretrained Transformer into a full/linear-attention hybrid by scoring candidate layer configurations end to end on the model's own hidden states while co-adapting the weights, beating proxy-based conversion. https://arxiv.org/abs/2611.24809

**Pick if we only read one:** the activation-steering paper. It is the sharpest version of the pattern we keep hitting (one shift explains the gain), and it is a short, concrete read.
