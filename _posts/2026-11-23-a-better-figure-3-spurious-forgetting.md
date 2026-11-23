---
title: "A better Figure 3: one shared lift, two consequences"
description: "Why old facts vanish and come back without retraining, in one picture: a shortcut that helps the new facts, until it hurts them."
paper: spurious-forgetting
task: key-visual
by: [Reuvenspitz]
---

## The original

[Figure 3 of the paper](https://arxiv.org/abs/2610.08718) explains why recall of the old facts collapses and then recovers on its own. It has three panels: the old facts' hidden states projected on the shared direction, the size of the common shift *s* during fine-tuning (with and without normalization), and the shared and individual margins of the new facts.

Everything is there, but the reader has to bring Eq. 5 to decode it. The turning point of the story, the moment the shift starts to hurt the new facts, appears only as the individual margin γ̄<sub>ind</sub> crossing zero in the right panel. And no panel shows what any of this does to the answer of a single fact.

## The redesign

A shared shortcut helps new learning but hides old knowledge. Once precise learning takes over, the shortcut becomes harmful, and retracts. Press **Watch the story**, or jump between the stages.

<iframe src="{{ '/assets/html/spurious-forgetting-core-idea/index.html' | relative_url }}" title="One shared lift, two consequences: an interactive view of spurious forgetting" loading="lazy" style="width: 100%; height: 1500px; border: 0;"></iframe>

*[Open the figure on its own page]({{ '/assets/html/spurious-forgetting-core-idea/index.html' | relative_url }}). The curve of the shared lift comes from [minimal_model.py]({{ '/assets/html/spurious-forgetting-core-idea/minimal_model.py' | relative_url }}), a NumPy re-implementation of the paper's minimal model (§3.1, App. B.1).*

## What changed and why

- **Answers instead of hidden-state geometry.** Each row shows the scores a fact gives its possible answers, so "the model now answers wrong" is visible without decoding a projection.
- **The shared shift as one object.** A purple lift under all B answers, identical in both rows, that the reader can watch grow and shrink.
- **A new fact next to an old one.** The new fact shows *why* the lift moves; the old fact shows the *consequence*.
- **The turning point in words, not as a zero crossing.** Early, the new fact's own spikes point to wrong answers, so diluting them helps. Later they point to the right one, so the lift only dilutes useful information, and gradient descent pulls it back.
- **A dashed outline for the stored signal.** The old fact's spike shrinks under normalization, but what is stored stays. That is the difference between hidden and erased.
- **Erosion in one sentence, not a stage.** It is a separate, slower process. Keeping it apart keeps the main mechanism clear, without implying that everything comes back.
- **The math one click away.** Eq. 5 and the real curve of the shift sit in a collapsible section, for readers who want the exact link to the paper.
- **Schematic where it has to be, real where it can be.** The bars are illustrative; the size of the shift over time comes from a real run, and the code is linked.
