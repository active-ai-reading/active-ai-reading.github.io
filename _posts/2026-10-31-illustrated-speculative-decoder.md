---
title: "The Illustrated Speculative Decoder"
description: "Speculative decoding in four pictures."
paper: matryoshka-lm-suites
by: [liadber]
---

## A single forward pass

A forward pass is multiplying every layer's weight matrices against the input.

{% include figure.liquid path="assets/img/posts/illustrated-speculative-decoder/forward-pass.png" class="img-fluid rounded z-depth-1" %}

> For one input you load *all* the weight matrices into SRAM (× 24).
> **So it is cheaper to feed in a matrix holding all the tokens (= vectors) than one vector at a time.**

> **The catch:** at **inference** the model doesn't know the next token until it computes it — so one vector goes in at a time.
> **In contrast,** at **training** the whole text is known in advance — so all the tokens go in at once.
> Speculative decoding is the way to exploit this at inference too (coming up…)

## A model's input and output

**Input:** a token, or several tokens at once.
**Output:** a probability table for the next word, for every token that went in.

{% include figure.liquid path="assets/img/posts/illustrated-speculative-decoder/input-output.png" class="img-fluid rounded z-depth-1" %}

## Speculative decoding

A small model guesses a few tokens ahead, one after another. The large model takes all of them at once and checks.

{% include figure.liquid path="assets/img/posts/illustrated-speculative-decoder/speculative-decoding.png" class="img-fluid rounded z-depth-1" %}

> **The gain:** the large model gets several tokens in one forward pass — it loads its weights once, not once per token.

## A draft that is part of the verifier

The paper: [Matryoshka LM Suites](https://arxiv.org/abs/2608.09703).

**The problem:** in speculative decoding with two separate models, the draft has to be tiny — so that time is really saved. But a tiny draft guesses badly: it agrees with the large model less often, and more guesses are rejected.

{% include figure.liquid path="assets/img/posts/illustrated-speculative-decoder/draft-inside-verifier.png" class="img-fluid rounded z-depth-1" %}

> **What the paper proposes:** train the draft and the verifier as one model — the draft is the first layers of the verifier, with its own head, and during training the large model distills into the small one.

**What this gives:**

- The small model agrees with the large one more — same layers + distillation.
- One model in memory, not two.
- Per the paper: the verifier does not recompute the first layers — the draft already did.
- **So the draft can be larger than usual.**
