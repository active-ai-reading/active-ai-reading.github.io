---
title: "Thinking Without More Tokens: Visualizing Recurrent Depth"
description: "An interactive comparison of three approaches to improving language model reasoning."
paper: recurrent-depth-latent-reasoning
role: visualization
task: key-visual
by: [shaharOssy]
---

## The core idea

How can we improve a language model's ability to solve difficult problems without simply making it bigger or asking it to generate more reasoning steps?

Geiping et al. (2025) explore a third scaling approach: **recurrent depth**. Instead of adding distinct Transformer layers or generating a longer verbal chain of thought, the model repeatedly updates its hidden state using the **same four-layer recurrent core**. A two-layer *prelude* processes the input, and a two-layer *coda* produces next-token probabilities after the recurrent computation.

The authors show that repeating this process can improve the model's performance on reasoning tasks.

## Interactive visualization

The visualization compares three approaches: increasing model size, generating more reasoning tokens, and repeating the same layers internally.

**Select an approach, move the slider, and see what changes.**

{% include recurrent-depth-explorer.liquid %}

## What to explore

1. **Scale parameters:** Add more independently learned layers.
2. **Scale output tokens:** Generate more intermediate reasoning steps.
3. **This paper:** Repeat the same four-layer block without adding parameters or reasoning tokens.

In the third approach, 32 repetitions produce an effective depth of 132 layer applications, while the model still has only eight distinct Transformer layers.

## The takeaway

**A model can do more internal processing without becoming larger or producing more text.**

The paper shows that this approach can significantly improve reasoning performance, especially on challenging tasks. Recurrent depth offers a promising new way to make language models better at reasoning by allowing them to think longer before producing an answer.
