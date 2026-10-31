---
title: "A token pov through MSAR"
description: Visualising the MSAR architecure from a token focuse prespective, emphasizing the convulution across the sequence dimension.
paper: multi-stream-attention-residuals
role: visualization
task: key-visual
by: [ohad-agadi]
chart:
---

## The original

The original figure shows an abstract view of individual components, each activating on the sequence matrix, compared against AttnRes.
For an unsuspecting reader, it might seem that the architectures are similar, and that MSAR is simply AttnRes but "more times". This however is not the case,
as the casual convolutions work along the sequence dimension rather then depth.

## The redesign

![MSAR at token t: learned convolutions across tokens, followed by depth attention and fusion.](/assets/img/papers/multi-stream-attention/token-msar.svg)

## What changed and why

The redesign is essentially a zoom-in of the original. Maintaining every component whilst emphasising the sequence-dimension activations.
