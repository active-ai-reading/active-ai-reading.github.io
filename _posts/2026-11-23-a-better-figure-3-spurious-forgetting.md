---
title: "The core idea: a shortcut that helps, until it hurts"
description: "Why old facts vanish and come back without retraining, in one picture: a shortcut that helps the new facts, until it hurts them."
paper: spurious-forgetting
task: key-visual
by: [Reuvenspitz]
---

## How the paper shows it

[Figure 3 of the paper](https://arxiv.org/abs/2610.08718) explains why recall of the old facts collapses and then recovers on its own. It has three panels: the old facts' hidden states projected on the shared direction, the size of the common shift *s* during fine-tuning (with and without normalization), and the shared and individual margins of the new facts.

Everything is there, but the reader has to bring Eq. 5 to decode it. The turning point of the story, the moment the shift starts to hurt the new facts, appears only as the individual margin γ̄<sub>ind</sub> crossing zero in the right panel. And no panel shows what any of this does to the answer of a single fact.

## The redesign

A shared shortcut helps new learning but hides old knowledge. Once precise learning takes over, the shortcut becomes harmful, and retracts. Press **Watch the story**, or jump between the stages.

<iframe src="{{ '/assets/html/spurious-forgetting-core-idea/index.html' | relative_url }}" title="One shared lift, two consequences: an interactive view of spurious forgetting" loading="lazy" style="width: 100%; height: 1500px; border: 0;"></iframe>

### What did we just see?

Early in training, the model finds a shortcut: boosting all B answers helps it learn new facts, even before it can distinguish their correct answers. But this shared boost also affects old facts, hiding their correct answers without erasing the underlying information.

The key is **RMSNorm**. As the shared component grows, normalization weakens the fact-specific signals. Initially, this helps by suppressing misleading signals. Later, once the new associations become accurate, the same effect becomes harmful: the shared boost reduces the score difference between correct and incorrect B answers.

Gradient descent therefore pulls the shared component back. As a side effect, the old facts become accessible again, **without ever being retrained**.

### Not everything comes back

The shared shift can retract: it hid the old fact without erasing it. But a second, slower process is not. Small **fact-specific changes** keep accumulating and gradually erase some old facts for good. The paper calls this **erosion**, and only this part is truly catastrophic forgetting.

## What changed and why

- **Answers instead of hidden-state geometry**, so "the model now answers wrong" is visible directly.
- **One purple lift, identical in both rows**, so the shared shift reads as a single object that grows and shrinks.
- **A dashed outline for the stored signal**, so hidden and erased look different.

*The bars are a qualitative schematic of the mechanism, not measured logits. The curve of the shared lift comes from a simulation of the paper's minimal model (§3.1; d = 128, α = 0.5, one seed); the code is in [minimal_model.py]({{ '/assets/html/spurious-forgetting-core-idea/minimal_model.py' | relative_url }}).*
