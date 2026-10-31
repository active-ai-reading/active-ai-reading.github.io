---
title: Critique of Multi-Stream Attention Residuals -"
description: One sentence summary of your take.
paper: multi-stream-attention-residuals
role: research
task: critique
by: [gilk717]
---

<!-- Keep the block for your task, delete the others. To cite, add the BibTeX to _bibliography/references.bib and use the cite tag (see the guide page). -->

<!-- CRITIQUE -->
## Summary of the claims

The paper upgrades single-stream depth attention (AttnRes) into multi-head depth attention. It creates multiple streams from earlier layers by running short causal convolutions across neighboring tokens, lets each stream attend over depth independently, and mixes them back into a single layer input.

## Strengths
MSAR generalizes single-stream depth attention into a multi-head retrieval mechanism, allowing layers to query earlier blocks through multiple parallel attention distributions and achieving strong scaling with minimal overhead.

## Weaknesses

MSAR attributes its gains to multi-head depth attention, using 1D depthwise causal convolutions (K in {4, 8, 12}) to generate diverse source streams from neighboring tokens. However, injecting short causal convolutions into the residual path introduces explicit local sequence mixing before every Attention and MLP/MoE sublayer—an inductive bias already known to independently improve language modeling in architectures like Mamba and hybrid Transformers. In Table 2, removing the convolutions while keeping 4 query heads (`w/o Conv`) degrades Pile loss, nearly reverting to single-stream AttnRes. The authors interpret this drop as proof that depth-attention heads need source diversity, but it is equally consistent with the convolutions themselves doing the heavy lifting via local token mixing while the multiple depth queries add very little.

## Verdict
Accept, as the empirical gains on 18B and 28B MoE models are strong, but the paper needs a control experiment adding the same convolutions to a single-stream baseline to verify that the gains actually come from multi-head depth routing rather than local token mixing.
