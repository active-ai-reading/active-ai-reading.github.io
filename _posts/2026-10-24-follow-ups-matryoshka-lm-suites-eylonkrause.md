---
title: "Is nesting the cheapest way to build a model suite?"
description: Five follow-ups that test the paper's efficiency claims, all starting from checkpoints the authors have already released.
paper: matryoshka-lm-suites
role: research
task: followups
by: [EylonKrause]
---

The paper {% cite godey2026matryoshka %} is really about cost: 36% less training compute and 14–26% faster speculative decoding, at near-parity quality. Each number comes from one setup: one training budget, one draft–verifier pair, one baseline, one distillation loss, and joint training throughout. Each follow-up below changes one of these. The [other follow-ups post]({{ '/posts/2026/follow-ups-matryoshka-lm-suites/' | relative_url }}) asks what is inside the dolls; this one asks whether nesting is the cheapest way to make and serve them.

## First: Hugging Face has much more than the paper

The first author's account has four Matryoshka repositories, not one:

- `matryoshka-3B`: checkpoints from 5B to 52B tokens, plus a cooled-down 60B run (`_60B_cd`).
- `matryoshka-baselines`: vanilla models matched in size and tokens. The smallest exit of each suite (500M, 100M, 50M) has a vanilla twin of exactly the same shape.
- `matryoshka-200M`: the small-scale ablations ($$\alpha_d$$ sweep, depth splits, loss weights, junctions).
- `matryoshka-1B`: a four-exit 100M / 300M / 600M / 1B suite trained to 105B tokens, which the paper never mentions.

An *exit* is one nested sub-model, read off at its own LM head. The follow-ups go roughly from cheapest to most expensive.

## 1. Does parity hold past 35B tokens? (a day of evaluation, then a few A100-days)

*Why this part: the 36% only matters if quality holds where small models are actually trained, and the paper stops at 35B tokens.*

**Question.** The paper's curves (Figures 3 and 4) track the gap to vanilla up to 35B tokens, about 11 per parameter for the 3B, below the compute-optimal ~20 {% cite hoffmann2022empirical %}. SmolLM2's 1.7B saw about 11T {% cite allal2025smollm2 %}. With more training, does the gap grow, because one 500M block serves three models, or shrink, because the free distillation keeps paying off?

**Experiment.** Evaluate every exit at every checkpoint against its vanilla counterpart. The cleanest pairs are the 500M exit (up to 60B tokens) and the four-exit suite's 100M (up to 105B, about 900 tokens per parameter). Mid-run checkpoints never had their learning rate decayed, so branch short matched cooldowns at two or three points, as the paper did for its 23B baseline: about 2.5 A100-days each for the four-exit suite, 7.5 for the 3B.

**Why it's worth doing.** It is cheap, and it tells #3 and #5 which regime to worry about. It is also the weakest here: the range is still short (the 500M reaches ~120 tokens per parameter, about 50× below SmolLM2), and the authors will probably publish this curve themselves, so share it with them. [achi-or's critique]({{ '/posts/2026/critique-matryoshka-lm-suites-achi-or/' | relative_url }}) asks for about 60B tokens, which is exactly where `_60B_cd` sits.

## 2. Every doll as a draft, at a fixed batch size (a few days of coding, then a day on one GPU)

*Why this part: speculative decoding is the paper's whole inference claim, and it is measured on one pair under conditions that mix several effects.*

**Question.** The paper runs 500M → 3B with each suite at its largest batch: 102 for Matryoshka, 64 for vanilla. So the +26% (greedy) and +14% (nucleus) mix three effects:

- higher acceptance (+5% accepted length, nucleus only);
- cheaper verification (the verifier reuses the draft's 24 layers, roughly 15–20% less compute than a vanilla 3B);
- a bigger batch.

The suite is also a ladder of drafts, each one's KV cache the bottom of the next one's, and the 1.5B–3B pair has the largest agreement gain (+5.7%). Yet only one pair is tested. Does 500M → 1.5B → 3B beat it?

**Experiment.** Write a loop with one KV cache per block; the released code has no generation, but [TalSokolov's reimplementation]({{ '/posts/2026/reimplement-cross-lingual-knowledge-pretraining/' | relative_url }}) has a 500M → 3B loop to start from.

- Chains: 500M → 3B, 1.5B → 3B, 500M → 1.5B → 3B, and n-gram → 500M → 1.5B → 3B (in cascade drafting, one neural draft plus a near-free statistical bottom level gave most of the gain {% cite chen2024cascade %}).
- Also test small vanilla drafts for the vanilla 3B (vanilla 100M, SmolLM2-135M/360M), which achi-or asks for.
- Batch sizes 1, 64 for both suites, and the maximum.

Predict first with hierarchical speculative decoding's latency model {% cite mohri2025hierarchical %}, giving each level only its extra block's cost.

**Why it's worth doing.** Multi-level speculation exists, even with shared KV caches: HiSpec gets 1.28× over a single level {% cite kumar2026hispec %}. But its middle levels are early exits of one fixed-width model. Here each level is a full model of its own width, and an extra level costs only its LM head (~0.23 GB). The 3B's last five layers are about half its compute, and a cascade runs them only on tokens the 1.5B accepted. If cascades win, nested suites get multi-level speculation almost free. If not, the fixed-batch runs still split the speedup into its three parts. One caveat: no released model uses grouped-query attention, though Llama-3.2-3B, whose shape the vanilla 3B copies, does. So the memory gain is probably inflated.

## 3. Compare against train-big-then-prune (about a week on one A100)

*Why this part: the 36% is measured against the most expensive way to build a suite, not the one people use.*

**Question.** The baseline trains every size from scratch without distillation, although the paper itself says suite members are "often distilled from larger ones". Minitron derives 8B and 4B models from a 15B "with up to 40x fewer training tokens per model" {% cite muralidharan2024compact %}. Llama 3.2 1B and 3B were pruned from Llama 3.1 8B and trained on logits from the 8B and 70B {% cite meta2024llama %}. The paper calls this "complementary" because it starts from "a sunk pretraining cost", but in a suite the largest model gets trained anyway.

**The budget.** In $$6ND$$ terms (parameters times tokens), a nested suite costs *more* than its largest model alone, because each exit has its own LM head: about 27% more at 200M scale and 5% more at 3B. Before it costs more than nesting, prune-and-distill can therefore spend about 4–6B distillation tokens per student at 200M scale (20–30% of pretraining), but only 1–2B at 3B (2–6%). Minitron used under 3%. So it fits easily at small scale and tightly at 3B; the question is quality.

**Experiment.** Prune the released vanilla 3B to the 1.5B and 500M shapes, distill each on 1–2B tokens (about 6 A100-days), and compare with Table 2; pilot it at 200M scale first. Keep one ledger, in $$6ND$$ and in wall-clock. They disagree: by $$6ND$$ the 3B saving is 35%, but the 200M-scale "41%" is about 27%, probably because the paper converts GPU-time into FLOPs.

**Why it's worth doing.** It decides whether the headline means "cheaper than the most expensive way" or "the cheapest way", and the outcome is open. Cutting 3B to 500M removes 84% of the parameters, past the ratio where pruning's head start nearly vanishes {% cite xu2026small %}. But distillation wins, up to a compute level, "in settings involving many students or an existing teacher" {% cite busbridge2025distillation %}, and that describes a suite. If prune-and-distill wins, nesting's case narrows to what pruning can't give: a draft that shares the verifier's weights and cache.

## 4. Train the draft for acceptance, not likelihood (an afternoon, then an A100-week)

*Why this part: in a nested suite the draft's loss is a free choice, and the paper picked it for perplexity, not speed.*

**Question.** A drafted token is accepted with probability $$\beta = \sum_v \min(p_v, q_v)$$, one minus the total-variation distance between draft and verifier {% cite leviathan2023speculative %}. For a fixed draft cost, nothing else about the draft matters. The paper trains it on 0.7 next-token loss plus 0.3 cross-entropy to the 3B, tuned for perplexity. Small drafts typically stop short of the shared optimum, and there "minimizing KL does not guarantee maximizing acceptance rate" {% cite samarin2026lk %}. How much does that cost?

**Experiment.**

- *No training:* on the released $$\alpha_d \in \{0, 0.3, 0.5, 0.7\}$$ branches, measure $$\beta$$ between the 50M and 200M exits at the paper's sampling settings; the paper reports only KL and perplexity.
- *At 3B:* include the undocumented vanilla `500M_35B_distill`. If it is what its name suggests, it separates distillation from weight sharing, achi-or's question.
- *Then train:* swap in reverse KL, Jensen–Shannon and an acceptance loss, plus an on-policy variant {% cite zhou2024distillspec %}, as short cooldown branches. Train the best one into the head only and into the whole shared block.

**Why it's worth doing.** Acceptance training usually freezes the verifier; one [unrefereed preprint](https://sergiu-nistor.com/assets/publications/Halfway_Speculative_Decoding.pdf) tunes an 8B target with its draft head. Here the draft *is* the verifier's first block, trained from scratch, so report the verifier's perplexity next to every speedup. The upside is capped: LK losses report up to 8–10% longer accepted length, against the paper's total 5% gain. A flat result still says agreement is limited by the 1:6 size gap, not the loss.

## 5. Does the big doll need to teach the small ones? (about two A100-weeks)

*Why this part: joint end-to-end training is the paper's central design choice, and the one it never ablates.*

**Question.** In joint training, the 1.5B and 3B losses push gradients into the 500M block. Help or tax? There are hints that the biggest exit pays: at 200M scale the 200M exit trails vanilla (15.62 vs 15.21 perplexity) while the 100M beats it, and LayerSkip found early-exit losses hurt the last layer {% cite elhoushi2024layerskip %}. The other post asks how the small model's *forward* signal helps the big one; this is the backward version.

**Experiment.** At 200M scale, with the same tokens and the paper's loss weights (it blames part of the gap on them, Appendix G):

- **(A) Joint:** the paper's recipe (released).
- **(B) Stop-gradient at every junction:** each block learns only from its own exit, while all blocks still train together.
- **(C) Sequential growth:** train the 50M (the released vanilla 50M has the same shape), freeze it, add the 100M, freeze, then add the 200M.
- **(D)** (C) plus a short joint fine-tune.

**Why it's worth doing.** If (B) matches (A), the downward gradient isn't needed. If (C) matches too, suites can grow after release: add a bigger doll on frozen ones, pay for one block, and every existing exit stays bit-for-bit the same. Nothing I found does this. Greedy local learning isolates blocks but discards their heads {% cite moon2026greedy %}; growth methods retrain everything {% cite gong2019efficient du2024stacking %}; LLaMA Pro grows a model around frozen blocks, but the old model is not an exit of the new one {% cite wu2024llama %}; progressive networks freeze old columns to add tasks {% cite rusu2016progressive %}. If they fail, the paper gains its most important missing ablation.

## Where I'd start

| # | Tests | Released start | New compute |
|---|---|---|---|
| 1 | parity past 35B | checkpoints to 105B | a day, plus cooldowns |
| 2 | source of the speedup | both suites, vanilla pairs | coding, then a GPU-day |
| 3 | the right baseline | vanilla 3B and 200M | about an A100-week |
| 4 | the draft's loss | $$\alpha_d$$ branches | an afternoon, then an A100-week |
| 5 | joint training | joint run, vanilla 50M | about two A100-weeks |

Costs are $$6ND$$, calibrated to the paper's five A100-days per 200M-scale run. If only one gets done, I'd pick #3: it decides what the headline means. #5 is the most interesting scientifically, and #2 is what the speed claim needs. #4's upside is capped, and #1 is a sanity check the authors will likely beat us to.

## Traps in the released files

- Don't use `main`: it is 42B in `matryoshka-3B`, the 3B suite in `matryoshka-200M`, and 10B in `matryoshka-1B`. `main_21B` and `main_42B` don't match `3B_21B` and `3B_42B`.
- Some 3B branches carry stale 5B-token shards. Load `model.safetensors`.
- The 50M and 100M branches of 200M splits v5, v6, v9 and v10 store `rope_theta = 1e4`; the paper uses `1e5`. Load the `200M_*` branch instead.
- The code rescales the junction by RMS, not L2 norms as in Eq. 1. Follow the code.
- `dist0`, `d05`, `d07`, `v9_atop` and the `_distill` branches are undocumented. Ask before relying on them.
