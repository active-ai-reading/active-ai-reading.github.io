---
title: "Rewriting Section 2 - Forgetting that undoes itself"
description: One sentence that makes people want to click.
paper: spurious-forgetting
task: copyedit
by: [TalSokolov]
---

## What I changed and why

Mainly the ordering: setting first, then each finetuning set with its outcome, then the evidence and leading questions. 
This flow seemed more natural, given section 2 is between the introduction and the results. 

## Before and after

<div class="before-after">
  <div class="before"><span class="label">Before</span>
    
  2 FORGETTING THAT UNDOES ITSELF
To understand when forgetting is not catastrophic, we first need a setting in which it clearly is not:
one in which performance collapses, yet the knowledge demonstrably survives (Appendix C.1).
We use synthetic biographies (Allen-Zhu & Li, 2024), on which spurious forgetting was identified
(Zheng et al., 2025), as they let us control what the model knows before finetuning and what it
learns during it. A transformer is pretrained on two non-overlapping sets of biographies, A and B,
in a single stage rather than one per set (Zheng et al., 2025), until it recalls all of their facts, and
is then finetuned on biographies of new individuals, without any replay. We compare two sets of
new biographies, C and B′
, which differ only in how they overlap with the old ones. We describe
how they are built, and what overlapping means precisely, in Section 4; for now, the only relevant
property is that C overlaps with both A and B, while B′ overlaps only with B (Figure 1, middle).
Finetuning on C yields classical catastrophic forgetting behavior (Figure 1, left): as the new facts
are learned, recall of both A and B declines slowly and steadily. Finetuning on B′ barely affects
recall of B, but recall of A follows a strikingly different trajectory (Figure 1, right), in three phases
that we refer to throughout the paper:

– Collapse: recall of A quickly drops, well before the new facts are learned.
– Recovery: recall of A then partially returns as the new facts are acquired, although A never
reappears in training.
– Erosion: finally, recall of A declines slowly and persistently, as in catastrophic forgetting.
This trajectory raises two questions: why finetuning on B′ hides the facts of A while sparing those of
B, and why the collapse reverses on its own. Section 3 answers both in a minimal model. Section 4
then returns to Transformers, and to the biography structure needed for the phenomenon to appear.
  </div>
  <div class="after"><span class="label">After</span>
    
  2 FORGETTING THAT UNDOES ITSELF
  
We study forgetting in two settings: a minimal associative memory model (Cabannes et al., 2024), 
which allows the mechanism to be analyzed (Section 3), and a controlled Transformer (Section 4), a more realistic setting. 
We use synthetic biographies (Allen-Zhu & Li, 2024), on which spurious forgetting was identified (Zheng et al., 2025), 
as they let us control what the model knows before finetuning and what it learns during it.

We pretrain on two non-overlapping sets of biographical facts, A and B, where for each attribute (e.g., birthplace, employer, etc.), 
A's answers are drawn from half of the possible vocabulary and B's from the other half. 
We then finetune on a third set of biographies of new individuals, without any replay of the individuals of A and B. 
We compare two sets of new finetuning biographies, C and B′, 
which differ by how their vocabulary overlaps with the disjoint vocabularies of A and B (Figure 1, middle). 

When the answers of the new individuals are drawn only from B's half, we call the set B′. 
Finetuning on B′ barely affects recall of B, but recall of A follows a strikingly different trajectory (Figure 1, right), 
in three phases that we refer to throughout the paper:

- Collapse: recall of A quickly drops, well before the new facts are learned.
- Recovery: recall of A then partially returns as the new facts are acquired, although A never reappears in training.
- Erosion: finally, recall of A declines slowly and persistently, as in catastrophic forgetting.

When the answers are drawn from both parts of the vocabulary, we call the set C. 
Finetuning on C yields classical catastrophic forgetting behavior (Figure 1, left): as the new facts are learned, 
recall of both A and B declines slowly and steadily.

**The knowledge is hidden, not erased**

At the bottom of the collapse in the B′ finetuning scenario, only 12% of A's facts are recalled, 
yet 86% still rank their correct answer first among the answers in their own half (Appendix C.1). 
Finetuning on B′ thus gives a setting in which forgetting clearly is not catastrophic: one in which performance collapses, 
yet the knowledge demonstrably survives.

This trajectory raises two questions: why finetuning on B′ hides the facts of A while sparing those of B, 
and why the collapse reverses on its own. Section 3 answers both in a minimal model. Section 4 then returns to Transformers, 
and to the biography structure needed for the phenomenon to appear.

  </div>
</div>

## The general rule

Help readers orient by introducing the variables before showing results, so the next sections follow naturally. 
Keep each condition next to its outcome. 
