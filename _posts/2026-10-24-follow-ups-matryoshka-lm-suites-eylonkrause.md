---
title: "Is nesting the cheapest way to build a model suite?"
description: Five follow-ups that test the paper's efficiency claims, all starting from checkpoints the authors have already released.
paper: matryoshka-lm-suites
role: research
task: followups
by: [EylonKrause]
---

The paper {% cite godey2026matryoshka %} is mostly about saving compute. One nested training run gives you a 500M, a 1.5B and a 3B model for 36% less compute than training them separately, and speculative decoding gets 14–26% faster, with quality about the same. But all of those numbers come from one setup: a single training budget, draft–verifier pair, baseline and distillation loss, with all blocks always trained together. Each follow-up below changes one of these, to check whether nesting really is the cheapest way to build and run the nested models (the "dolls"). I call each nested model an *exit*: the point in the network where you stop and read off that model's prediction through its own output layer. *Vanilla* means a model of the same size trained on its own. The follow-ups go roughly from cheapest to most expensive.

## 1. Does parity hold past 35B tokens?

*Why this part: the 36% only matters if quality holds where small models are actually trained, and the paper stops at 35B tokens.*

**Question.** The paper's curves (Figures 3 and 4) track the gap to vanilla up to 35B tokens, about 11 tokens per parameter for the 3B. That is even below the roughly 20 tokens per parameter that [Chinchilla](https://arxiv.org/abs/2203.15556) found gives the best model for a fixed training budget. Small models that actually ship are trained far longer: a model that answers millions of queries costs more to run than to train, so it pays to over-train a small model rather than serve a bigger one. SmolLM2's 1.7B, for example, saw about 11T tokens, roughly 6,500 per parameter {% cite allal2025smollm2 %}. Does the gap to vanilla grow with more training (one 500M block has to serve three models) or shrink (the small exits keep learning from the 3B, at no extra cost in a nested run)?

**Experiment.** The authors' Hugging Face page has checkpoints up to 60B tokens with vanilla counterparts, plus an unpublished four-exit 100M / 300M / 600M / 1B suite trained to 105B. Compare every exit with its vanilla counterpart at every checkpoint. The cleanest pairs are the 500M exit (up to 60B tokens) and the four-exit suite's 100M (up to 105B, about 900 tokens per parameter), because their vanilla twins have exactly the same shape. One catch: a model only reaches its final quality after the learning rate is lowered at the end of training (the "cooldown"), and mid-run checkpoints haven't had that yet. So give both models a short cooldown at two or three points, as the paper did for its compute-matched vanilla baseline (cooled down from 21B to 23B tokens).

**Why it's worth doing.** It's cheap, and the answer matters for #3 and #5: if the gap grows with training, those should be tested at longer budgets too. It's also the weakest of the five, because the range is still short: the 500M exit only gets to ~120 tokens per parameter, about 50× less than SmolLM2.

## 2. Every doll as a draft, at a fixed batch size

*Why this part: the paper's speedup is measured on one draft–verifier pair, at batch sizes that differ between the two suites.*

**Question.** In speculative decoding, a small *draft* model guesses a few tokens ahead and the big *verifier* checks them all in one pass, keeping the ones it agrees with. The output is the same, just faster. The paper drafts with the 500M, verifies with the 3B, and runs each suite at the largest batch that fits in GPU memory: 102 for Matryoshka, 64 for vanilla. So its +26% (greedy) and +14% (nucleus sampling) speedups mix three effects:

- more drafted tokens kept per check (+5%, reported for nucleus sampling only);
- cheaper checking: the verifier reuses the draft's 24 layers (the whole 500M) instead of recomputing them, roughly 15–20% less compute than a vanilla 3B;
- a bigger batch, because draft and verifier share one KV cache (the stored attention state of earlier tokens), which leaves memory for more requests.

A nested suite also has more than one possible draft. Each exit's KV cache is already part of the next one's, and nesting raises next-token agreement most for the 1.5B–3B pair (+5.7% over the vanilla pair; agreement is what drives acceptance). Yet only 500M → 3B is tested. Does a chain like 500M → 1.5B → 3B do better?

**Experiment.** Write a decoding loop that keeps one KV cache per block (the released code has no generation). Then test:

- Chains: 500M → 3B, 1.5B → 3B, 500M → 1.5B → 3B, and n-gram → 500M → 1.5B → 3B. An n-gram draft costs almost nothing, so it can propose tokens for the 500M to check.
- Small vanilla drafts for the vanilla 3B (vanilla 100M, SmolLM2-135M/360M; they share the tokenizer, so they can draft for these models). Drafts are usually 10–100× smaller than the verifier, and the paper itself shows that a 500M draft barely speeds up the vanilla 3B, so the fair baseline is the best vanilla draft, not that one.
- Batch sizes of 1 (a single user, where latency is what matters), 64 for both suites (which removes the memory difference), and the maximum (the paper's setting).

**Why it's worth doing.** Multi-level speculation has been tried before, even with a shared KV cache: HiSpec gets 1.28× over a single draft level {% cite kumar2026hispec %}. But its middle levels are early exits, intermediate layers of one network that all have the same width. Here each level is a complete model of its own width, and adding a level costs only its output layer (~0.23 GB). The 3B's last five layers are about half its compute, and in a chain they only run on tokens the 1.5B already accepted. If the chain wins, nested suites get multi-level speculation almost for free. Separately, the fixed-batch runs split the paper's speedup into its three parts. None of the released models use grouped-query attention, a standard trick that makes the KV cache several times smaller (Llama-3.2-3B, whose shape the vanilla 3B copies, uses it). With it, sharing the cache saves less memory, so the batch-size gain is probably larger here than it would be in practice.

## 3. Compare against train-big-then-prune

*Why this part: the 36% is measured against the most expensive way to build a suite, not the one people use.*

**Question.** The baseline trains every size from scratch without distillation, even though the paper itself says suite members are "often distilled from larger ones". The usual recipe today is to train the largest model, prune it (cut layers or width), and then distill: train the smaller model to imitate the big one. Minitron derives 8B and 4B models from a 15B this way, "with up to 40x fewer training tokens per model" {% cite muralidharan2024compact %}, and [Llama 3.2 1B and 3B](https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/) were pruned from Llama 3.1 8B and trained to match the next-token probabilities (logits) of the 8B and 70B. The paper calls this approach "complementary" because it starts from "a sunk pretraining cost", but in a suite the largest model gets trained anyway.

**The budget.** Count training compute as $$6ND$$ (6 × parameters × tokens, the usual estimate). A nested suite then costs *more* than its largest model alone, because each exit has its own output layer, and with a 49K-token vocabulary those layers are big: about 27% more at 200M scale and 5% more at 3B. That extra is what prune-and-distill can spend before it costs more than nesting: about 4–6B distillation tokens per small model at 200M scale (20–30% of pretraining), but only 1–2B at 3B (2–6%). Minitron used under 3% of the original pretraining tokens, so at 3B it's tight but possible. So it comes down to which approach gives better models.

**Experiment.** Prune the released vanilla 3B to the 1.5B and 500M shapes, distill each on 1–2B tokens, and compare with the paper's Table 2. Try it at 200M scale first, where it's cheap. Count compute both as $$6ND$$ and as GPU time, because the two disagree: by $$6ND$$ the 3B saving is 35%, but the paper's 200M-scale "41%" comes out at about 27%. The paper turns GPU-hours into FLOPs using the GPU's peak speed (Appendix B), and small models trained separately probably use the GPU less efficiently, so the 41% is a real GPU-time saving but overstates the compute saving.

**Why it's worth doing.** It tells us whether nesting is the cheapest way to build a suite, or only cheaper than training every size separately, and I don't know which way it goes. Cutting a 3B down to 500M removes 84% of its parameters, and at that point a pruned model may have lost most of what it inherited. On the other hand, distillation beats ordinary training (up to a compute level that grows with the student's size) "in settings involving many students or an existing teacher" {% cite busbridge2025distillation %}, and a suite has both: the big model is trained anyway, and there are two smaller ones to teach. If prune-and-distill wins, the main thing nesting still has is a draft that shares the verifier's weights and cache, which pruning can't give you.

## 4. Train the draft for acceptance, not likelihood

*Why this part: in a nested suite the draft's loss is a free choice, and the paper picked it for perplexity, not speed.*

**Question.** A drafted token is accepted with probability $$\beta = \sum_v \min(p_v, q_v)$$, the overlap between the draft's next-token distribution $$q$$ and the verifier's $$p$$ {% cite leviathan2023speculative %}. For a given draft size and draft length, that overlap is all that matters for speed. The paper trains its draft for something else: 70% ordinary next-token loss and 30% imitating the 3B (the distillation weight, $$\alpha_d = 0.3$$), with the weight chosen for perplexity. A small draft can't copy the big model exactly, so it has to compromise, and the best compromise for imitation isn't the best one for acceptance: "minimizing KL does not guarantee maximizing acceptance rate" {% cite samarin2026lk %}. How much faster would a draft trained for acceptance be?

**Experiment.**

- *No training:* the authors released small-scale runs (a 50M / 100M / 200M suite) whose names suggest $$\alpha_d$$ = 0, 0.3, 0.5 and 0.7. Measure the acceptance between the 50M and 200M exits at the paper's sampling settings. The paper only reports imitation (KL) and perplexity for these, not acceptance.
- *At 3B:* include the undocumented vanilla `500M_35B_distill` branch. If it really is a vanilla 500M distilled from the vanilla 3B, comparing it with Matryoshka's 500M shows how much of the agreement comes from distillation and how much from sharing layers.
- *Then train:* replace the imitation loss with reverse KL, Jensen–Shannon or an acceptance loss, and also try training on text the draft generates itself, since that's what it sees while decoding. Run each as a short cooldown branch from one checkpoint, as the paper does in Appendix G, which is much cheaper than full runs. Train the best loss two ways: into the draft's output layer only, and into its whole block.

**Why it's worth doing.** Work on acceptance-trained drafts usually keeps the verifier frozen; one [unrefereed preprint](https://sergiu-nistor.com/assets/publications/Halfway_Speculative_Decoding.pdf) tunes an 8B verifier together with its draft head (a small module on top of the verifier that does the drafting). Here the draft *is* the verifier's first block, trained from scratch, so a loss that makes the draft agree more can also change the verifier. That's why the two training variants matter, and why the verifier's perplexity should be reported next to every speedup. Don't expect a big win: LK losses, which train the draft on acceptance directly {% cite samarin2026lk %}, report up to 8–10% longer accepted length, and the paper's whole accepted-length gain over vanilla is 5%. A flat result would still be useful, because it would mean agreement is limited by the 1:6 size gap rather than by the loss.

## 5. Does the big doll need to teach the small ones?

*Why this part: the paper always trains all blocks together and never tests what happens if it doesn't.*

**Question.** When everything trains together, the 1.5B and 3B losses also send gradients into the 500M block, so the small model's weights are partly shaped by what the bigger models need. Does that help the small exits, and does sharing cost the big one? There are hints that the biggest exit pays a price: in the paper's 200M-scale ablation (Table 3), the 200M exit is worse than vanilla (15.62 vs 15.21 perplexity), while the 100M exit beats its vanilla model.

**Experiment.** Four runs at 200M scale, with the same tokens and the paper's per-exit loss weights (the paper blames part of the gap on those weights, Appendix G):

- **(A) Joint:** the paper's recipe (already released).
- **(B) Stop-gradient at every junction** (where one block's output feeds the next): each block learns only from its own exit, but all blocks still train at the same time.
- **(C) Sequential growth:** train the 50M on its own (the released vanilla 50M has exactly this shape, so this step is already done), freeze it, add and train the 100M block, freeze that, then add the 200M.
- **(D)** (C) plus a short joint fine-tune at the end.

**Why it's worth doing.** If (B) matches (A), the gradients coming down from the bigger models aren't needed. If (C) matches too, a suite can grow after release: you train only a new, bigger block on top of the frozen ones, and the existing models don't change. I couldn't find anyone who has done this. Greedy local learning trains each block on its own local loss with no gradients between blocks, which is close to (B), but its per-block heads are thrown away after training, so the blocks never become usable models {% cite moon2026greedy %}. LLaMA Pro grows a model by training new blocks around frozen ones, but the old model doesn't survive as a working exit of the new one {% cite wu2024llama %}. If they fall short, joint training is what makes nesting work.
