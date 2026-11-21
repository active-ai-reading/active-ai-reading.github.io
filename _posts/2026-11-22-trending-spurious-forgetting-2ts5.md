---
title: "Papers worth knowing this week"
description: "Five recent papers on forgetting during finetuning, each answering a different part of the question this week's paper raises: when is lost knowledge really gone?"
paper: spurious-forgetting
task: trending
by: [EylonKrause]
---

This week's paper argues that much of what looks like forgetting during finetuning is a reversible loss of access rather than lost knowledge. The five papers below approach the same question from different directions: the paper that named the phenomenon, one on why some finetuning methods forget less, one on when models stop being able to absorb new facts without overwriting old ones, one separating forgetting in the features from forgetting in the output layer, and one on how pretraining length affects finetuning.

## The paper that named it

**[Spurious Forgetting in Continual Learning of Language Models](https://arxiv.org/abs/2501.13453)** (Zheng et al., ICLR 2025). Shows that performance drops in continual learning often reflect a loss of task alignment in the first optimization steps rather than a loss of knowledge, and proposes freezing the bottom layers as a remedy. This week's paper builds directly on it, and suggests that its shared shift toward the new answers may be one concrete form of that loss of alignment.

## Why some finetuning forgets less

**[RL's Razor: Why Online Reinforcement Learning Forgets Less](https://arxiv.org/abs/2509.04259)** (Shenfeld et al., 2025). At equal performance on the new task, reinforcement learning preserves prior capabilities better than supervised finetuning, and the amount of forgetting is predicted by the KL divergence between the finetuned and base model on the new task; on-policy RL is implicitly biased toward the KL-minimal solution. It gives a distribution-level account of forgetting, where this week's paper gives a geometric one.

## When replay is enough, and when it is not

**[Forgetting in Language Models: Capacity, Optimization, and Self-Generated Replay](https://arxiv.org/abs/2605.26097)** (Marek et al., 2026). Samples a language model generates from its own training distribution work as replay data and nearly eliminate forgetting, unless the model was pretrained close to saturation and has no capacity left; without replay, low learning rates reduce forgetting at the cost of many more steps. It complements this week's finding that higher learning rates deepen the collapse.

## Features stay, heads collapse

**[Heads Collapse, Features Stay: Why Replay Needs Big Buffers](https://arxiv.org/abs/2512.07400)** (Lanzillotta et al., ICLR 2026). Separates deep forgetting, in the features, from shallow forgetting, in the classifier: a tiny replay buffer keeps the features linearly separable, but fixing the classifier needs a much larger one. It is the image-classification counterpart of this week's result that the old facts keep their relative geometry while only the readout loses them.

## Pretraining length and adaptability

**[Overtrained Language Models Are Harder to Fine-Tune](https://arxiv.org/abs/2503.19206)** (Springer et al., ICML 2025). Longer pretraining can make a model worse after finetuning: the instruction-tuned OLMo-1B pretrained on 3T tokens scores over 2% lower on several benchmarks than its 2.3T-token counterpart, because its parameters become more sensitive to any modification. It raises a question this week's paper leaves open: whether the shared, recoverable part of forgetting changes with pretraining budget.
