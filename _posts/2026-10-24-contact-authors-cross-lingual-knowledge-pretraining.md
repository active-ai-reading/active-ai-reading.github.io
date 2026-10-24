---
title: "<Critique / literature review / follow-ups> of <paper>"
description: One sentence summary of your take.
paper: cross-lingual-knowledge-pretraining
role: research
task: contact-authors
by: sprinzak
---

<!-- FOLLOW-UPS -->
## Follow-ups worth doing

**The question.** In Section 3.2.3, the Matryoshka pair fits a batch of 102 sequences in 80GB, versus 64 for the Vanilla pair. Throughput rises with batch size on its own. Were the Figure 5 throughput numbers measured at each pair's own maximum batch size, and how much of the reported gain (up to 26% over the Vanilla pair) comes from better draft-verifier agreement rather than the larger batch?

**The experiment.** Rerun the Figure 5 comparison with both pairs at the same batch size (for example 64, then a sweep up to 102 where memory allows). Report throughput and accepted length across draft lengths, with plain autoregressive decoding at each batch size as a reference. This needs no retraining, since the checkpoints are released.

**Why it's worth doing.** The paper credits the speedup mainly to higher acceptance from shared weights and distillation, but reports accepted length only about 5% higher on average under nucleus sampling, while throughput is up 14% at the headline setting. These are not identical measurements, so this is only a hint. A matched-batch result would show whether the alignment benefit stands on its own, or whether much of the gain is the memory saving, which is a real benefit but a different one.

**Status.** Question sent to the authors (Nathan Godey, Yoav Artzi) on <date>. No reply yet.
