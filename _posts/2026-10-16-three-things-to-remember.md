---
title: Three things to remember, and where the paper hides them
description: The points most readers should leave with, and how the paper could make them harder to miss.
paper: cross-lingual-knowledge-pretraining
role: writing
task: key-points
by: [course-team]
example: true
---

Most readers will skim the abstract, look at Figure 1, and maybe read the intro. So the question for this task is: **what should they leave with, and do those places deliver it?**

## The three points

**1. A model that learns a fact in one language mostly does not know it in the other, and this starts in pretraining.**
One exposure in Arabic is worth about 1% of one in English for recalling a fact in English (CLeq = 0.9% at 360M, 5.9% at 7B). Standard fixes (code-switching, activation alignment) stay below 3%.

**2. Disjoint tokens alone are enough to cause it.**
Two *identical* copies of English, differing only in token IDs, share nothing (CLeq = −2.6%, and −0.1% even when both copies see the same text). The models learn matching structures in both embedding spaces but never connect them.

**3. Sharing tokens helps, but only if the shared tokens mean the same thing.**
Writing Arabic word by word in English tokens raises CLeq to 12.6%. Shuffling the dictionary (shared tokens, wrong meanings) drops it to 3.0%, and transliteration alone to −0.3%.

## Where they currently live

| Point | Abstract | Figure 1 | Intro |
| --- | --- | --- | --- |
| 1. It starts in pretraining | ✓ (no numbers) | ✓ (left panel, baseline bar) | ✓ |
| 2. Disjoint tokens suffice | ✓ (sentence 6) | ✗ | ✓ (bold) |
| 3. Meanings, not just tokens | ✗ | ✗ | ✗ |

Point 2 is the paper's most original result, but **Figure 1 is about point 3's intervention (WWT)**, not about the cause. And point 3's "meaning matters" half appears only in Section 6.4.

## Suggestions

- **Make Figure 1 tell the causal story.** Left: CLeq for En–Ar baseline, En₁–En₂ (clone), and En–WWT-Ar side by side. That one panel says "natural pairs fail, identical clones fail too, merging tokens helps". The perplexity panel can move to Section 6.
- **Add the controls to the WWT bar chart.** A bar for "shuffled dictionary (3.0%)" and "transliteration (−0.3%)" next to WWT (12.6%) makes point 3 visible at a glance.
- **Put a number in the first paragraph.** "Exposure in a second language is worth about 1% of a native one" is memorable in a way "surprisingly limited transfer" is not.
- **Say what CLeq is in one human sentence wherever it first appears in a caption.** Figure 1's caption says it "measures cross-lingual knowledge learning efficiency", which a skimmer can't decode.
