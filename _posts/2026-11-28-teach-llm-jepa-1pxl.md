
---
title: "Representation Collapse: When a Perfect Loss Means Nothing Was Learned"
description: Why predicting embeddings can lead to trivial solutions and how different learning methods deal with this problem.
paper: llm-jepa
task: teach
by: [golombi]
---

## Why this matters

While reading LLM-JEPA, I came across an interesting problem with training models to predict embeddings rather than tokens.

In standard language modeling, the targets are given by the training data. When predicting embeddings, however, the targets themselves are representations learned by the model.

This made me wonder: what prevents the model from simply learning embeddings that are easy to predict, rather than embeddings that actually capture meaningful information?

This problem is known as **representation collapse**.

## The idea

### How can a model minimize its loss without learning anything useful?

Suppose we have two inputs that express the same idea:

- x: "Return the square of a number."
- y: `def square(x): return x * x`

We have an encoder E that maps inputs to embeddings and a predictor P that tries to predict the embedding of y given the embedding of x.

Consider the following simplified loss function:

$$
\mathcal{L} = \|P(E(x))-E(y)\|^2
$$

We would hope that minimizing this loss encourages the encoder to capture the meaning shared by the two inputs.

However, there is a much simpler solution. Suppose the encoder learns to map every input to the same constant vector c:

$$
E(x) = c \quad \text{for every } x
$$

If the predictor also learns to output c, we get:

$$
\mathcal{L} = \|c-c\|^2 = 0
$$

The loss is zero, yet the embeddings contain no information about the inputs.

To illustrate this, consider the following toy example:

| Input | Non-collapsed embedding | Collapsed embedding |
|---|---|---|
| Dog | [1, 0, 0] | [1, 1, 1] |
| Car | [0, 1, 0] | [1, 1, 1] |
| House | [0, 0, 1] | [1, 1, 1] |

In the second case, given only the embedding, we have no way of knowing what the original input was.

### Why isn't this a problem in standard next-token prediction?

Consider two training examples:

- "The capital of France is" → Paris
- "The capital of Italy is" → Rome

If the model produces identical representations for both contexts, its prediction head will produce the same probability distribution over the vocabulary for both.

Since the correct next tokens are different, the model cannot predict both correctly with high confidence.

The important difference is that the model cannot change the target tokens. In embedding prediction, on the other hand, the model can potentially change both the prediction and the target to minimize the loss.

### How do we prevent collapse?

There are several interesting approaches to this problem.

**Contrastive learning (SimCLR)**

Instead of only encouraging related inputs to have similar embeddings, we also encourage unrelated inputs to have different embeddings. Mapping everything to the same vector is therefore no longer a good solution.

**Variance regularization (VICReg)**

We explicitly encourage the embeddings of different samples in a batch to vary. If all embeddings are identical, their variance is zero, and the model is penalized for it.

**Momentum target encoders (BYOL and I-JEPA)**

We use a separate encoder to produce the target embeddings. Instead of updating this encoder directly through gradient descent, we update its weights gradually using a moving average of the main encoder's weights.

This means that the model cannot directly change the target embeddings during a gradient update. Together with other design choices, this helps prevent collapse.

**Combining objectives (LLM-JEPA)**

Another approach is to combine embedding prediction with standard language modeling:

$$
\mathcal{L}_{total}
=
\mathcal{L}_{LLM}
+
\lambda \mathcal{L}_{JEPA}
$$

Even if collapsing the representations reduces the JEPA loss, the language modeling objective still encourages the model to preserve information needed for token prediction.

This does not guarantee that collapse cannot occur in particular parts of the model, but it provides an additional incentive to learn useful representations.

### A quick question

Would replacing Euclidean distance with cosine distance solve the collapse problem?

Think about it before reading the answer.

The answer is no. If every input is mapped to the same nonzero vector, the cosine similarity between any two embeddings is 1, so their cosine distance is still zero.

What I find interesting about this problem is that it highlights something we should keep in mind when designing loss functions: it is not enough to show that the solution we want minimizes the loss. We should also ask what other solutions minimize it.

## Learn more

- [SimCLR](https://arxiv.org/abs/2002.05709): An introduction to contrastive learning.
- [VICReg](https://arxiv.org/abs/2105.04906): Preventing collapse through variance and covariance regularization.
- [BYOL](https://arxiv.org/abs/2006.07733): Learning representations without negative samples.
- [I-JEPA](https://arxiv.org/abs/2301.08243): Applying joint embedding predictive architectures to images.
