---
title: "Representation Collapse: When a Perfect Loss Means a Useless Model"
description: Understanding why learning in embedding space can lead to trivial solutions and how modern self-supervised learning methods prevent them.
paper: llm-jepa
task: teach
by: [MatanBarTov]
---

## Why this matters

While reading LLM-JEPA, I encountered a fundamental challenge in self-supervised learning: **representation collapse**.

JEPA learns by predicting representations in latent space rather than reconstructing the original input. However, if both the predicted and target representations are learned, what prevents the model from mapping every input to the same vector?

## The idea

### Representation collapse

Consider an encoder trained to minimize the distance between representations of two views of the same input:

```math
\mathcal{L} = \mathbb{E}_{x,x'}\left[\|f_\theta(x)-f_\theta(x')\|_2^2\right]
```

Consider two possible solutions:

| Input | Meaningful representation | Collapsed representation |
|---|---|---|
| Dog | (0.9, 0.1) | (1, 1) |
| Augmented dog | (0.9, 0.1) | (1, 1) |
| Cat | (0.1, 0.9) | (1, 1) |
| Augmented cat | (0.1, 0.9) | (1, 1) |

Both solutions achieve zero loss, but only the first preserves meaningful information.

The second is called **complete representation collapse**. The model achieves the optimal loss without learning anything useful.

A more subtle phenomenon is **dimensional collapse**, where representations are not identical but occupy a low-dimensional subspace, leaving much of the embedding capacity unused.

### How do different methods prevent collapse?

**SimCLR: Negative examples**

Contrastive learning brings representations of positive pairs closer while pushing negative pairs apart. Mapping every input to the same vector is therefore no longer optimal.

**BYOL and I-JEPA: Architectural asymmetry**

These methods use a target encoder whose parameters are updated through an exponential moving average of the online encoder:

```math
\xi \leftarrow \tau\xi + (1-\tau)\theta
```

Combined with a predictor and stop-gradient mechanism, this asymmetry helps avoid collapse in practice, without requiring negative examples.

**VICReg: Explicit regularization**

VICReg combines three objectives:

- Invariance: align representations of related inputs.
- Variance: prevent embedding dimensions from becoming constant.
- Covariance: reduce redundancy between dimensions.

For example, its simplified variance loss is:

```math
\mathcal{L}_{var}=\frac{1}{d}\sum_{j=1}^{d}\max(0,\gamma-\operatorname{Std}(Z_j))
```

Constant representations have zero variance and are therefore penalized.

### How does LLM-JEPA address this?

LLM-JEPA combines the standard next-token prediction objective with a JEPA objective:

```math
\mathcal{L}_{\text{LLM-JEPA}}=\mathcal{L}_{\text{NTP}}+\lambda\mathcal{L}_{\text{JEPA}}
```

While the JEPA objective encourages alignment between semantically related inputs, next-token prediction encourages the model to preserve information necessary for generation.

This provides a complementary learning signal that may help avoid collapse, although it does not theoretically guarantee non-collapsed sequence-level embeddings.

**Takeaway:** A low training loss does not necessarily indicate meaningful representations. When designing a learning objective, we must consider not only the solutions we want to encourage, but also the trivial solutions it allows.

## Learn more

- [SimCLR (2020)](https://arxiv.org/abs/2002.05709): Contrastive learning with negative examples.
- [BYOL (2020)](https://arxiv.org/abs/2006.07733): Learning without negative examples.
- [VICReg (2022)](https://arxiv.org/abs/2105.04906): Explicit anti-collapse regularization.
- [Understanding Dimensional Collapse (2022)](https://arxiv.org/abs/2110.09348): Partial representation collapse.
- [I-JEPA (2023)](https://arxiv.org/abs/2301.08243): Predictive learning in embedding space.
