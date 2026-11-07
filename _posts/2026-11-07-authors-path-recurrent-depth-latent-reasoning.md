---
title: "literature review of recurrent depth latent reasoning"
description: "How Jonas Geiping and Tom Goldstein's earlier work on efficient language models and recurrent computation converged in a new approach to test-time scaling."
paper: recurrent-depth-latent-reasoning
role: research
task: authors
by: [MatanBarTov]
---

---
title: "The authors' path: From efficient training and deep thinking to latent reasoning"
description: "How Jonas Geiping and Tom Goldstein's earlier work on efficient language models and recurrent computation converged in a new approach to test-time scaling."
paper: recurrent-depth-latent-reasoning
role: research
task: authors
by: your-github-username
---

## The authors' path

The first and last authors of *Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach* are **Jonas Geiping** and **Tom Goldstein**. Their previous research provides two particularly relevant foundations for this paper: making language models more computationally efficient, and enabling neural networks to solve harder problems by performing more computation.

### Jonas Geiping: Making language models more efficient

Jonas Geiping is a researcher at the ELLIS Institute Tübingen and the Max Planck Institute for Intelligent Systems. His research focuses on the efficiency, safety, and reliability of modern machine learning systems, particularly large language models.

One of his most relevant earlier works is [*Cramming: Training a Language Model on a Single GPU in One Day* (ICML 2023)](https://proceedings.mlr.press/v202/geiping23a.html), co-authored with Tom Goldstein.

Rather than asking how much performance could be gained by increasing computational resources, they explored how much could be achieved under strict computational constraints. By optimizing the training pipeline, they demonstrated that a BERT-like language model could achieve competitive performance after just 24 hours of training on a single GPU.

The connection to the current paper is clear: **both studies challenge the assumption that improving language models necessarily requires increasing their parameter count.** While *Cramming* investigated how to use a limited training budget efficiently, the recurrent-depth paper explores how to use additional computation at inference time without increasing the number of model parameters.

### Tom Goldstein: From optimization to recurrent reasoning

Tom Goldstein is a Professor of Computer Science at the University of Maryland and Director of the Maryland Center for Machine Learning. His research combines optimization, machine learning, and efficient computing.

The recurrent-depth paper builds especially closely on his earlier research into what his group calls **"deep thinking" networks**.

In [*The Uncanny Similarity of Recurrence and Depth* (2021)](https://arxiv.org/abs/2102.11011), Goldstein and his collaborators showed that recurrent neural networks could reproduce some of the benefits of deeper feedforward networks by repeatedly applying the same layers.

This idea was extended in [*Can You Learn an Algorithm? Generalizing from Easy to Hard Problems with Recurrent Networks* (NeurIPS 2021)](https://www.cs.umd.edu/~tomg/project/thinking/). The researchers demonstrated that recurrent networks trained on relatively simple reasoning problems, such as small mazes, could generalize to harder instances by performing additional iterations at inference time.

These results established a central motivation for the current paper: **a model's computational depth does not have to be fixed at training time.** Instead, the model can reuse learned operations for as long as a problem requires.

## How their research connects to this paper

The recurrent-depth paper can be viewed as a convergence of these two research directions:

- **From Geiping and Goldstein's *Cramming*:** Efficient model design and careful use of computational resources can provide alternatives to simply increasing model size.
- **From Goldstein's earlier deep-thinking research:** Recurrent computation enables models to increase their effective depth and potentially solve harder problems without introducing additional parameters.

The current work combines these ideas at the scale of modern language modeling. The authors train a 3.5-billion-parameter Transformer with a recurrent block that can be executed repeatedly at inference time, allowing the model to perform additional reasoning internally rather than generating longer chains of thought.

The important progression is **from demonstrating recurrence on relatively controlled reasoning tasks to testing whether the same principle can work in a large-scale, pretrained language model**.

This makes the paper more than an isolated architectural experiment. It represents a continuation of the authors' broader investigation into how neural networks can use computation more effectively, both during training and at inference time.

## The bigger picture

The authors' research trajectory suggests an alternative perspective on scaling language models. Instead of treating parameter count and training data as the primary ways to improve performance, their work investigates whether **the organization and allocation of computation** can be equally important.

The recurrent-depth paper is an important step in this direction, although it leaves open whether latent recurrence can match the reasoning capabilities and efficiency of leading models that rely on explicit Chain-of-Thought reasoning.

**The main takeaway:** This paper connects two established research threads from its authors: efficient language-model training and recurrent neural computation. Its novelty lies in bringing these ideas together to demonstrate test-time reasoning through increased depth rather than increased token generation.
