---
title: "<Critique / literature review / follow-ups> of <paper>"
description: One sentence summary of your take.
paper: matryoshka-language-model-suites
role: research
task: contact-authors
by: sprinzak
---

<!-- FOLLOW-UPS -->
## Follow-ups worth doing

**The question.** In Section 3.2.3, the Matryoshka pair fits a batch of 102 sequences in 80GB, versus 64 for the Vanilla pair. Throughput rises with batch size on its own. Were the Figure 5 throughput numbers measured at each pair's own maximum batch size, and how much of the reported gain (up to 26% over the Vanilla pair) comes from better draft-verifier agreement rather than the larger batch?

**The experiment.** Compare the Vanilla and Matryoshka pairs at the same batch size (at most 64 on an 80GB GPU, where the Vanilla pair maxes out), then run the Matryoshka pair at its own maximum of 102, using the same setup as Figure 5. The gap at equal batch size reflects draft-verifier agreement; the extra gap at 102 reflects the larger batch.
**Why it's worth doing.** The paper credits the speedup mainly to higher acceptance from shared weights and distillation, but reports accepted length only about 5% higher on average under nucleus sampling, while throughput is up 14% at the headline setting. These are not identical measurements, so this is only a hint. A matched-batch result would show whether the alignment benefit stands on its own, or whether much of the gain is the memory saving, which is a real benefit but a different one.

**Status.** Question sent to the authors (Nathan Godey and Yoav Artzi) on 24.10.2026. They confirmed that a NeurIPS reviewer had raised a similar question and that they had run additional experiments on different hardware. Matryoshka remained 10–15% faster at matched batch sizes, while its larger maximum batch size increased the speedup to approximately 33%.

These results suggest that both improved draft-verifier alignment and memory efficiency contribute to the throughput gains.
