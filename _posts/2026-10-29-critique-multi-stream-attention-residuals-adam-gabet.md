---
title: "Critique of Multi-Stream Attention Residuals"
description: Is their technique really attention over residuals?
paper: multi-stream-attention-residuals
role: research
task: critique
by: AdamGabet
---
<!-- To cite, add the BibTeX to _bibliography/references.bib and use the cite tag (see the guide page). -->

## Summary of the claims

Attention Residuals (AttnRes) replace the fixed residual sum with softmax attention over earlier layers {% cite kimi2026attnres %}. Each layer has one learned query. That is one attention distribution over depth. MSAR claims to make it multi-head {% cite qin2026msar %}. It expands each stored source into 4 streams. Stream 0 is the source itself. Streams 1–3 are causal depthwise convolutions over previous input tokens with 4 lengths (0, 4, 8, 12).  

The claims: lowest loss at 18B (1.750 vs 1.769 for AttnRes, Fig. 1a). 1.58× iso-loss compute speedup over Vanilla, vs 1.35× for AttnRes (Fig. 3). Cost: +0.3% parameters and +0.5% FLOPs (Table 5).

## Strengths

The idea is simple. Splitting the hidden state into heads doesn't work. Copies of the same vector give identical keys. Borrowing diversity from the previous token avoids both. Pipeline communication stays at AttnRes cost. They win in the loss at (almost) same compute.

## Weaknesses

**The gain may come from token mixing, not from multiple depth heads.** The convolutions add information about earlier tokens into every sublayer input. This includes MLP sublayers, which normally see only the current token. A short causal convolution might be a known win. Canon layers put a kernel-4 causal convolution before attention and before the MLP {% cite allenzhu2025canon %}. Primer added depthwise convolutions after Q, K and V and cut training compute by up to 4× {% cite so2021primer %}.

**Efficiency is reported in FLOPs, not time.** Memory traffic is 21.5d per token per sublayer. AttnRes is 5.5d (Table 6). The 1.58× is a FLOP ratio. No throughput is reported. The convolution also breaks the per-token locality of AttnRes. Sequence parallelism now needs a halo exchange across shards which introduces communication overhead. Decoding needs a convolution state at every layer. 

## How it could have been improved

Add one control: AttnRes plus a single causal convolution on the sources, one head. Add Vanilla plus Canon-A/C. If these match MSAR, the contribution is token mixing. Report tokens per second. Test long context with sequence parallelism. 

## Verdict

Would you accept it? Is the direction worth pursuing? Why?

I wouldn't accept until they show the gain is from the "attention" on residual connection and not convolution on the previous tokens. They also need to prove that this can be trained efficiently at scale with training time not just flops.
