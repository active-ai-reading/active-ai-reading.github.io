---
title: "Follow-ups of Matryoshka Language Model Suites"
description: The nested suite was built for efficiency, but its shared backbone makes it a ready-made interpretability testbed.
paper: matryoshka-lm-suites
role: research
task: followups
by: [ItamarFruchter]
---

The paper {% cite godey2026matryoshka %} mostly aims at efficiency gains, but I believe there is real interpretability work to be had from its setup.
Some of these follow-ups require post-training, but others can be run as-is on the released checkpoints:

### 1. What does the upper block add?

**Question:** On which kinds of tokens and contexts does a bigger sub-model outperform a smaller one? I think this is different from comparing models of different sizes, since these share a joint backbone up to some point. Can we measure where the added block helps: on rare tokens, factual recall, arithmetic, etc.?

**Experiment:** Some metrics would require a different training dataset and some question-answering post-training, but we can already run two interesting experiments:

- Run the full suite on factual claims from the training data, framed as a sentence-completion task.
- Evaluate each sub-model, and a vanilla (independently trained) model of the same size, on the same claims.

**Why?** If additional capabilities are discernible, they must come from parameters outside the first block, which may tell us something about the minimal depth or width a capability needs. Additionally, these are inference-time experiments only, so they require no retraining and can use the published checkpoints.

### 2. Embedding analysis

**Question:** The junction, as shown in the [visualization post]({{ '/posts/2026/visualizing-🪆-models/' | relative_url }}), feeds sub-model $$m+1$$ with the (rescaled) output of sub-model $$m$$, $$\tilde{o}^m$$, concatenated with $$D_{m+1}-D_m$$ dimensions of a fresh embedding, $$e^{m+1}$$.
Analyzing how the block uses these two distinct groups of channels, or analyzing the embeddings themselves, might teach us something about how the work is "divided" between the blocks, or where their additional capabilities emerge from.

**Experiment:**

- Analyze the attention heads in the first layer of any block other than the first. Attention selects positions, not channels, so the question is which channels a head *reads* from: are there heads whose query, key and value weights read mostly from the $$o$$ channels? Mostly from the $$e$$ channels? This can be measured from the weights alone, before running anything.
  - If such heads are found, try to find their "purpose": what do they do?
- Do the two groups get mixed? After the first layer of a block the residual stream mixes the channels, so the clean split only exists at its input. Each sub-model keeps its own LM head, so on deeper layers of the larger block we can apply sub-model $$m$$'s head to the first $$D_m$$ channels and read off its predictions directly. This is a logit lens {% cite nostalgebraist2020logitlens %} that needs no training, unlike the tuned lens {% cite belrose2023tunedlens %}, and it uses a head that was trained on exactly these channels, which the usual logit lens on intermediate layers is not. Do these predictions change, and by how much (cross-entropy on the logits as well as argmax agreement)?
- Instead of feeding block 2 with $$[o^1, e^2]$$, try feeding it $$[e^1, e^2]$$ and see what happens. This ablation is missing from the paper (its "zero junction" ablation zeroes the fresh embedding but keeps $$o$$). Retrained this way, the larger model becomes a shallower model, which will surely be worse. But the size of the gap is the point: it separates how much the first sub-model's computation helps the second from how much comes from the added layers and width alone.

**Why?** Models have emergent capabilities, and pointing out the specific components that give rise to a trait is a big part of interpretability. This architecture reduces the search space and might help locate such answers.

### 3. Will post-training trickle down?

**Question:** If post-training is applied to the full suite, what happens to the sub-models? The paper itself lists instruction tuning and alignment of nested suites as an open question, and the [critique by achi-or]({{ '/posts/2026/critique-matryoshka-lm-suites-achi-or/' | relative_url }}) argues it is critical for the paper's real-world claims to hold.

**Experiment:** Post-train the whole suite on a simple target (SFT, question answering, refusal training), then ask:

- Do the smaller sub-models also show the same behaviors?
- Did the smaller sub-models drift away from being usable stand-alone models?
  - This will probably need some ablations and sweeps to find the limits.
- How does each sub-model perform on specific tasks, such as question answering or refusal tests?

**Why?** Post-training is a crucial and expensive part of LLM training in the real world. It would also be interesting to see how such training regimes affect this architecture, given the glimpse it offers into the model's "inner thoughts" before it answers. This is especially interesting for refusal, which in conventionally trained models is mediated by a single direction in the residual stream {% cite arditi2024refusal %} and appears to depend on a specific range of middle layers {% cite li2025safetylayers %}.

### What each one costs

- **#1** is the cheapest: inference only, on the released checkpoints. A comparison to vanilla models of the same size would require training those baselines.
- **#2** is mostly inference too: the head analysis needs only the weights, and the lens needs only forward passes. The $$[e^1, e^2]$$ ablation is the exception, since it means retraining a suite.
- **#3** is the most expensive: post-training a whole suite, plus the sweeps needed to find where the sub-models stop being usable on their own.
