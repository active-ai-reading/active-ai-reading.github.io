---
title: "Before you read MSAR: the three ideas it builds on"
description: "A short guide to the background the paper assumes: residual connections, Hyper-Connections and Attention Residuals, and the problem that leads to MSAR."
paper: multi-stream-attention-residuals
role: communication
task: social
by: [liadber]
---

Our reading group spent this week on ["Multi-Stream Attention Residuals"](https://arxiv.org/abs/2610.13630) (Qin et al., 2026), which proposes a new way to connect the layers of a Transformer and reports solid gains on 18B and 28B parameter models.

The paper builds on three earlier ideas and assumes you already know them. This post walks through those ideas in order, with the problem each one leaves open, and shows how the last of those problems leads directly to MSAR. If the background is familiar, skip to the final section.

## The question

A token passes through the layers of a Transformer one by one, and each layer changes it a little. So every architecture has to decide: **how does a layer draw on the layers below it?** The three ideas below are three answers.

## Answer 1 · Residual connections: add everything

This is the standard connection. Each layer adds its output to a running sum, and the next layer reads that sum. It is simple and stable, and it works. The cost is that every output lands in the same vector with the same weight. As the network gets deeper, the contribution of early layers is diluted, and nothing downstream can recover it on its own.

## Answer 2 · Hyper-Connections: several streams in parallel

Hyper-Connections replace the single residual stream with several streams that run through the whole network, mixed at every layer by learned matrices. Information no longer has to collapse into one sum. mHC from DeepSeek, which the paper refers to often, is a variant that constrains the mixing matrices to keep training stable.

The limitation is that the mixing is learned once and then frozen. Every token, on every input, gets the same mix. But which layer holds the useful information varies from token to token: for one token it is layer 2, for the next it is layer 7. A fixed mix cannot track that. Running several streams also multiplies memory.

## Answer 3 · Attention Residuals: let the input decide

Attention Residuals replace the sum with attention over the outputs of the earlier layers. It is the familiar mechanism, applied along the depth axis rather than the sequence axis. The twist is that there are no Q, K or V projections. Each layer has a single learned query vector, and those earlier outputs serve as both keys and values. The method adds almost no parameters, yet the weights now depend on the input: one token can draw mostly on layer 2 while its neighbour draws on layer 7.

{% include figure.liquid path="assets/img/posts/before-you-read-msar/three-answers.png" class="img-fluid rounded z-depth-1" %}

*The three answers. Arrow width shows how much the top layer takes from each earlier layer. Only in the third case does the pattern change from token to token.*

## The problem that remains: a single head

Attention over the sequence uses several heads, each with its own view of the sentence. What makes them different is either separate projection matrices or separate slices of the vector. Attention Residuals has neither option: there are no matrices, and slicing the vector degrades the selection. Run four heads and they all see the same outputs, so they end up nearly identical. This is the point where MSAR begins.

## What MSAR adds

MSAR gives each head a different view without adding matrices or slicing the vector. Before a head selects among layers, each output is passed through a causal convolution along the sequence, blending in a few of the preceding tokens, and each head uses a different window size. The four heads therefore see four slightly different views of the same column and make different selections. How the heads are fused, and why this costs no extra memory, is covered in the method section, which reads easily once this background is in place.

{% include figure.liquid path="assets/img/posts/before-you-read-msar/heads-with-and-without-conv.png" class="img-fluid rounded z-depth-1" %}

*Left: four heads without the convolution see identical inputs. Right: each head gets its own window, and so its own selection.*

One reading tip: the paper calls this a "depth-wise" convolution, but it runs over tokens, not over layers. The attention is along depth; the convolution is along the sequence.

## In short

There are three ways to connect layers, and what separates them is whether the weights are fixed or computed from the input. Attention Residuals is the dynamic one, but without projection matrices it is limited to a single head. MSAR gives each head a different window over the sequence, and that is the whole idea. With these three pieces in place, the paper is a straightforward read.

Posted at: [LinkedIn](https://www.linkedin.com/feed/update/urn:li:share:7524911557277802496/) · [X](https://x.com/LiadBercovitch/status/2119148408984248760)
