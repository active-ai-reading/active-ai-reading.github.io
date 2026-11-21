---
title: "Multi-Stream Attention Residuals in a thread"
description: Social media posts for MSAR (Multi-Stream Attention Residuals), the paper that reframes the residual stream as multi-head attention over depth.
paper: multi-stream-attention-residuals
task: social
by: dan22333
---

## X / Twitter

> The residual stream in a Transformer is secretly attention over DEPTH. Every past layer gets dumped into one vector with a frozen weight of 1. Make it multi-head and you get a 1.58× compute speedup for +0.5% extra FLOPs. New paper: Multi-Stream Attention Residuals (MSAR). 🧵
>
> 2/ Why deep stacks waste depth: h₍l+1₎ = h₍l₎ + f(h₍l₎). Later layers read the accumulated sum, not individual earlier features. A feature born in layer 3 is hard to retrieve at layer 40. And as the stream grows, each new update shrinks relative to it. Depth dilutes itself.
>
> 3/ That additive sum IS attention along the layer axis. Just single-head, with fixed uniform weights. Hyper-Connections = a recurrent linear-attn depth memory. AttnRes = single-head softmax retrieval over depth. The obvious next step: multi-HEAD depth attention.
>
> 4/ The trap: split the hidden state into head fragments like normal MHA and it breaks. In depth attention the retrieved "value" is the hidden state itself. Slice it and you destroy its integrity. The paper tried it and performance dropped.
>
> 5/ MSAR's move: pull head diversity from the SEQUENCE axis instead. Expand each layer output into m full-dim streams via cheap causal depthwise 1-D convs (kernels 4/8/12). Each head attends over depth through a different contextual view. Diverse heads, every one full-dimensional.
>
> 6/ Results (DeepSeekMoE-style, 18B & 28B MoE): MSAR wins all 12 benchmarks at both scales. 28B avg 52.4 vs AttnRes 49.4 vs vanilla 44.6. Iso-loss speedup: 1.58× vs 1.35× (AttnRes), 1.30× (mHC). Overhead: +0.5% FLOPs, +0.3% params.
>
> 7/ The ablation that proves the mechanism: delete the convolutions (keep the extra query heads) and the gain mostly vanishes, 1.847 → 1.862 loss. The win comes from source diversity, not from more query heads. A hand-built AttnRes+mHC hybrid can't match it either.
>
> 8/ Mental model: a deep network is doing retrieval over its own history. Spending compute on better depth-wise retrieval beats simply adding parameters. A free 1.58× quality-per-FLOP. Paper: arXiv 2610.13630 (SJTU × Xiaohongshu Dots Studio).

## Bluesky

> The residual connection is a disguised attention mechanism over the depth axis: single-head, with frozen uniform weights. MSAR generalizes it to multi-head. The catch: you can't channel-split the heads, because the "value" in depth attention is the whole hidden state, so slicing breaks it. 🧵
>
> 2/ Fix: get head diversity from the sequence axis. Expand each layer output into m full-dimensional streams with cheap causal depthwise 1-D convs (kernels 4/8/12). Each head attends over depth through a different contextual view. +0.5% FLOPs, and it stores only single-stream summaries, expanded on demand.
>
> 3/ On 18B/28B MoE it wins all 12 benchmarks and hits a 1.58× iso-loss compute speedup (vs 1.35× AttnRes, 1.30× mHC). Ablation: remove the convs and the gain collapses. It's source diversity, not extra queries. arXiv 2610.13630.

## Mastodon

> New architecture paper worth knowing: Multi-Stream Attention Residuals (MSAR).
>
> The pitch: the residual stream h₍l+1₎ = h₍l₎ + f(h₍l₎) is secretly attention over the depth axis, single-head with fixed uniform weights. Later layers read an accumulating blob and dilute their own depth. MSAR makes depth attention multi-head.
>
> You can't channel-split the heads, because the value in depth attention is the full hidden state. So MSAR draws diversity from the sequence axis: cheap causal depthwise 1-D convs expand each layer output into m full-dim views.
>
> Result: +0.5% FLOPs, wins all 12 benchmarks at 18B/28B MoE, 1.58× iso-loss compute speedup. arXiv 2610.13630.
>
> #NLProc #MachineLearning

## LinkedIn

> **A 1.58× compute speedup hiding in the residual connection**
>
> One of the most overlooked parts of a Transformer is also one of the oldest: the residual connection, h₍l+1₎ = h₍l₎ + f(h₍l₎). Most of us treat it as plumbing. A new paper, Multi-Stream Attention Residuals (MSAR) from Shanghai Jiao Tong University and Xiaohongshu's Dots Studio, argues it's doing something much richer, and that we've been doing it in the crudest possible way.
>
> The insight: that additive sum is a form of attention along the depth axis, where every earlier layer's output is retrieved with a fixed, uniform weight of 1. That's why very deep models use depth inefficiently. Later layers read one accumulated vector rather than individual earlier features, and each new layer's contribution shrinks relative to the growing stream.
>
> Prior work (Hyper-Connections, Attention Residuals) had already started treating depth as something to attend over. MSAR takes the natural next step, multi-head depth attention, and solves the problem that blocked it. You can't split the hidden state into head fragments the way sequence-axis attention does, because in depth attention the "value" is the hidden state itself. MSAR instead builds diverse heads from the sequence axis, using lightweight causal convolutions to give each head a different contextual view of the same layer output.
>
> Why a practitioner should care: at 18B and 28B Mixture-of-Experts scale, MSAR wins all 12 evaluated benchmarks and delivers a 1.58× iso-loss compute speedup over a standard residual baseline, for +0.5% training FLOPs. The lineage it builds on (mHC, AttnRes) is already used in trillion-parameter training runs, so this is a live production architecture, not a research toy.
>
> The broader lesson: where you spend compute can beat how much you add. Better depth-wise retrieval is nearly free quality per FLOP, which is exactly the kind of lever that matters when you're compute-bound.
>
> Paper: arXiv 2610.13630.

## Notes

**Images per post**
- Hook (1/) and LinkedIn header: the headline bar chart, MSAR vs Vanilla/mHC/AttnRes 12-benchmark average at 18B/28B.
- 3/: the "residual stream = attention over layers" schematic (HC = linear-attn memory, AttnRes = single-head, MSAR = multi-head).
- 5/: the multi-stream source-expansion figure (one layer output, m conv views, per-stream depth attention, Hpre fusion).
- 6/ and 7/: the iso-loss scaling curve and the ablation table.

**Who to tag**
Authors: Qin, Zhang, Dai, Zou, Wu, Yang, Xia, Yao, Liu, Yan (Shanghai Jiao Tong University / Xiaohongshu "Dots Studio"). Pull their handles from the arXiv page (2610.13630) before tagging. Worth looping in the Hyper-Connections and Attention Residuals authors too, since this builds directly on their line.

**Success metrics**
- Hook: impressions, profile visits, and clicks on the arXiv link.
- Thread retention: how many readers reach post 6/ (the results).
- Reposts and quote-posts from people working on architecture; author engagement counts more than raw impressions.
- LinkedIn: comments from engineers, not just likes.

**Posted links**
- X:
- Bluesky:
- Mastodon:
- LinkedIn:
