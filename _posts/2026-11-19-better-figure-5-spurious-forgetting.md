---
title: "A better Figure 5"
description: One panel per run, so you can see what removing the top direction does to old facts and what it costs on new facts.
paper: spurious-forgetting
task: redo-graph
by: [AdamGabet]
---

## The original

Figure 5 fine-tunes OLMo 2 1B on new facts only (no replay) and checks the old facts it already knew. It has three panels, one per analysis: old and new facts for both runs (left), old facts with the top singular direction of each weight update removed (middle), and a small vs. large set of new individuals (right).

What makes it hard to read:

- The panels are organized by analysis, so one run is spread over three panels and you compare by eye.
- The middle panel shows old facts only, so the edit looks like a pure win. Its cost on the new facts is not shown.
- Line shades change between panels (navy, red, pink, gray) and the legends differ in each one.

## The redesign

{% include figure.liquid path="assets/img/posts/better-figure-5-spurious-forgetting/better-figure-5.png" class="img-fluid rounded" caption="Figure 5 (redrawn). Removing the top direction of each weight update prevents the collapse of old facts. OLMo 2 1B is finetuned on new facts without replay, in separate runs. Old facts (CounterFact facts the model knows) are blue, and green when the top direction of each weight update is removed; new facts are gray dashed; the star marks new-fact accuracy at step 400 with the top direction removed (Table 3). (1) Synthetic individuals (invented names with random answers, so the name gives no hint of the answer): old facts collapse, then partly recover; removing the top direction largely prevents the collapse. (2) Real entities (real products with their real makers, so the product type hints at the maker): old facts drop less and do not recover; removing the top direction keeps them higher. (3) With a larger set of 1,000 synthetic individuals instead of 250, the collapse goes deeper and lasts longer. Curves are read off Fig. 5 of Palit et al. (2026) and are approximate; stars are from Table 3." %}

## What changed and why

- One panel per run (synthetic individuals, real entities, large set).
- Same color means the same thing in every panel: blue is old facts, green is old facts with the top direction removed, gray dashed is new facts.
- The edit sits next to normal training in the same panel, so its effect on old facts is one comparison.
- One shared legend under the plots, and no labels on the plot. The one-line hint for each run is in the caption.
- The large set gets its own panel with old and new facts only, since the paper does not report the edit for it.
- The original shows the edit only helping old facts. The redesign adds its cost on the new facts, from Table 3: a gray hollow star at step 400 in each run. For synthetic individuals, new-fact accuracy drops from 0.90 to 0.40, and for real entities, from 1.00 to 0.66. Only step 400 is drawn; the step 80 values (0.03 to 0.01 and 0.46 to 0.25) are in the table.
