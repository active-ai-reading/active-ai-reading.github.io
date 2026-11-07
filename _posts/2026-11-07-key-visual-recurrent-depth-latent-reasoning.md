---
title: "Thinking Without More Tokens: Visualizing Recurrent Depth"
description: "An interactive visualization of how language models can increase inference-time computation by repeatedly reusing the same Transformer layers."
paper: recurrent-depth-latent-reasoning
role: visualization
task: key-visual
by: [shaharOssy]
---

## The core idea

Most approaches to scaling language models involve increasing the number of parameters or generating additional reasoning tokens through Chain-of-Thought.

Geiping et al. (2025) explore a third possibility: **increasing computation in latent space without increasing the number of parameters or generating intermediate reasoning tokens.**

Their model, Huginn-0125, consists of three components:

1. **Prelude:** Processes the input into a latent representation.
2. **Recurrent core:** Repeatedly updates the hidden state using the same Transformer layers.
3. **Coda:** Converts the final hidden state into next-token probabilities.

The key distinction is between **the number of unique layers a model stores** and **the number of times those layers are executed**.

## Interactive visualization

The following visualization illustrates how recurrent depth works and what happens when we increase the number of recurrent iterations.

{% include recurrent-depth-explorer.liquid %}

## What to explore

1. **Compare the three scaling approaches.** Notice that recurrent depth increases computation without adding parameters or generating intermediate reasoning tokens.
2. **Adjust the recurrence slider.** Observe how the same four-layer recurrent block is reused while the effective computational depth increases.
3. **Watch the recurrence animation.** The model repeatedly updates its latent state before producing the next token.
4. **Explore the benchmark results.** Additional iterations can improve performance, but different tasks benefit from different amounts of computation.

## The key takeaway

**Computational depth and parameter count are not the same thing.**

With only eight distinct Transformer layers, Huginn-0125 can achieve an effective depth of 132 layer applications when its four-layer recurrent core is executed 32 times.

The model does not become larger. Instead, it performs more computation using the parameters it already has.

This raises an interesting question: **Could future language models dynamically decide how much internal computation each problem requires?**

