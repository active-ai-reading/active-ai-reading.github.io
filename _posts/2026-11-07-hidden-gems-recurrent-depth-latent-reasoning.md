---
title: "Can we read Huginn's latent thoughts? It depends on the lens"
description: Two papers that try to decode the recurrent states of this week's model, and why they seem to disagree.
paper: recurrent-depth-latent-reasoning
role: scouting
task: hidden-gems
by: [ItamarFruchter]
---

This week's paper claims that looping a recurrent block is a form of reasoning in latent space. If that is true, we should be able to watch the answer form across the recurrences. Two papers tried to do this on Huginn, the model from this week's paper.

**[Latent Chain-of-Thought? Decoding the Depth-Recurrent Transformer](https://arxiv.org/abs/2507.02199)** (Lu, Yang, Lee, Li & Liu, 2025):
Decodes Huginn's intermediate states with the logit lens and with a *coda lens*, which runs the state through Huginn's own two learned decoder blocks. The two lenses disagree about which recurrent blocks are readable, and neither shows a clear latent chain of thought.

**[Looped Transformers under the Jacobian Lens: Does the Global Workspace Survive Recurrence?](https://openreview.net/forum?id=EwfPUo0f4x)** (anonymous ICLR 2027 submission, under review):
Fits a lens aimed at each stage of the loop and finds the answer is readable at every recurrence. Each lens can only read about two recurrences ahead, though, so a lens that fails on early states says nothing about whether those states contain the answer.
(Caveat - still under review. This looks good and highly relevant, but we should probably wait for a peer-reviewed version)

## Why the two papers seem to disagree

The Jacobian lens is a linear map: the average, over many prompts, of how a change in one hidden state moves a later one. A logit-lens or coda-lens readout asks the early state to look like the final one. The Jacobian lens instead learns how to carry the early state forward to a chosen target recurrence (4, 8, 12 or 16) and reads it there.

On *"The capital city of the country famous for sushi is"*, *Tokyo* ranks first at recurrences 2–3 through the lens aimed at recurrence 4. Through the lenses aimed at 8, 12 and 16 it ranks first at recurrences 7, 10–11 and 14–15. The same forward pass looks empty or full depending on which lens you use and how far it has to reach. That is one explanation for the disagreement Lu et al. saw.

Here a *recurrence* is one pass of Huginn's 4-layer core, so "two recurrences" is about 8 transformer layers.

## What the model seems to be doing

- **It recomputes rather than remembers.** Shrinking the input that Huginn re-injects at every recurrence to a quarter of its size breaks the answer on every tested prompt. Swapping in another prompt's input changes the answer within about two recurrences.
- **It can steer old content but can't report new content.** If you swap a concept the model already computed, it reports the new one 98% of the time (124/126). If you inject a concept it never computed, it never names it (0/97). Ouro, a looped model trained to be readable after every loop, manages 31%.
- **Only late edits stick.** Edits in the last lens window are as effective as edits everywhere (25/192 flips each). Edits in the window before it get 5/192.

## Questions for class

- If the answer is readable from recurrence 2–3, what are the remaining recurrences doing? Is that "reasoning", or re-deriving the same answer from the input?
- The paper's convergent, orbiting and drifting trajectories (Figure 12): does "the state keeps being rebuilt from the input" change how we read them?
- How much of what we call latent reasoning is a property of the model, and how much of the instrument we use to look?

*Bonus, if you care about compute:* **[What Does Another Loop Buy?](https://openreview.net/forum?id=mQUR2BQm7r)** (anonymous ICLR 2027 submission) stops looping once the attention pattern stops changing between iterations. On Huginn it saves 48% of the compute for a 2-point drop on GSM8K, and beats a KL-based exit at matched compute. That is a simple alternative to the early-exit criterion in this week's paper.
