---
title: "Papers worth knowing this week"
description: A single-line optimizer adjustment may serve as the primary defense against catastrophic forgetting.
paper: spurious-forgetting
task: hidden-gems
by: ohad-agadi
---

<!-- At least two papers, one sentence each, with a link. How you organize the rest is up to you. -->
[A DEAFENING SILENCE: CATASTROPHIC FORGETTING
LIVES IN THE OUTPUT EMBEDDINGS OF TOKENS
THE DATA NEVER SPEAKS:](https://arxiv.org/abs/2610.09835)
These guys make some claims about why and where forgetting occurs. The main one is that optimizing a single paramater (Adam's epsilon) may reduce 50%+ in catastrophic forgetting.

[Do LLMs Really Forget? Hidden-State Leakage in Model
Unlearning and How to Fix it
](https://arxiv.org/abs/2609.36612
)
Claim is that "forgetten" information is often hidden in intermediate layers. They purpose an interesting mechanism, probe intermediate layers, train train the probe to reconstruct forgotten answers, update the llm to make the probes fail(min-max).

