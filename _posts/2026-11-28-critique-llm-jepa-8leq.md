---
title: "Critique of When Forgetting is Not Catastrophic: On the Mechanics of Spurious Forgetting"
description: A sharp, well-controlled mechanistic result I would accept, but it stops at factual recall and never connects its irreversible "drift" term to the plasticity-loss literature where it belongs.
paper: spurious-forgetting
task: critique
by: dan22333
---

<!-- Critique of Palit, Draye, Zucchet, Jin & Schölkopf, arXiv:2610.08718. -->

## Summary of the claims

The paper argues that the accuracy drop we call "forgetting" during finetuning is really **two processes on different timescales**, and that conflating them is the field's mistake:

1. A shared, reversible **common shift**: every old memory moves in the *same* direction in hidden space, toward the region of the new answers. This is hiding, not erasure. The facts still rank correctly within their own answer region, and the shift is withdrawn on its own once the new facts are actually learned, producing the striking **collapse → recovery → erosion** curve *with no replay*.
2. A slow, irreversible **fact-specific drift**: each old memory moves in its *own* direction, with no restoring force, so it only accumulates. This is the real, catastrophic erosion.

The common shift needs three ingredients, each shown necessary: **shared key structure** (keys are `k_i = √α·μ + √(1−α)·e_i`, α > 0), **new answers concentrated in one region of the vocabulary**, and **normalization**. RMSNorm is the load-bearing and counterintuitive part: it both amplifies the collapse (rotating states toward the shift, shrinking their individual parts) and then supplies the restoring force that withdraws it, captured in a closed-form scalar ODE whose recovery is gated by *learning* of the new facts, not by step count. The practical payoff is an internals-light repair: **subtract the top singular direction of each weight update**, which restores the hidden facts in a real pretrained LM. Validated across three scales: a minimal associative-memory model, a controlled attention-only Transformer on synthetic biographies, and OLMo-2 1B on CounterFact / EntityQuestions.

## Strengths

- **It is mechanistic and falsifiable, not descriptive.** The two-term decomposition is backed by a clean causal test: subtract the common component of the logit change and the collapse disappears entirely; keep *only* the common component and you reproduce collapse-then-recovery. That is a real knife, not a correlation.
- **The three-ingredient ablation is complete** (remove key-sharing, answer-concentration, or normalization and the phenomenon dies), so the theory is not over-claimed.
- **The repair is genuinely useful and genuinely tested.** It works on a real LM, and it is explicitly *not* a training rewind: at matched new-fact accuracy the edited model recalls more old facts than the trained one. The removed direction holds only ~8-15% of the update norm but has 0.75-0.97 cosine with the common shift, which is a satisfying "small, well-localized cause" result.
- **It dissolves a confusing empirical object.** The "stability gap" (sharp early drop, then return) and linear-probe "shallow forgetting" become one thing: the common-shift hiding. It also explains *why* replay helps the trough but cannot stop erosion, which matches its own replay ablation (trough 0.17 → 0.50, but final only 0.54 → 0.62).
- Honest grounding in prior phenomenology (availability vs accessibility; spontaneous recovery) without overselling the analogy.

## Weaknesses

- **Scope is narrow: factual recall, first-token accuracy, one real LM (OLMo-2 1B).** The entire story is key-value lookup. Whether "hiding vs erasing" even has the same meaning for skills or multi-step reasoning is untested, and that is where most practical forgetting lives.
- **The headline self-healing is cleanest where it is least realistic.** The authors concede the normalization-driven recovery is probably weaker on real data; the full collapse → recovery → erosion curve is crispest in the minimal model and under a schedule deliberately engineered to make it observable.
- **A theory/experiment gap it does not close.** The theory is gradient-flow, where learning rate only rescales time, yet empirically the *depth* of collapse grows with LR. That is left unexplained rather than flagged as a limit of the model.
- **A confound in the key real-LM result.** Synthetic individuals recover; real entities never do. The paper attributes this to "what the subject reveals about the answer," but the two conditions differ in other ways too (entity distribution, answer overlap with pretraining), and there is no stimulus set that varies *only* that factor.
- **It does not connect its irreversible term to the plasticity-loss literature, where it clearly belongs.** "Fact-specific drift with no restoring term" is, operationally, a loss of capacity, and there is a mature line studying exactly that: how one update reduces what the model can later learn. Reading this paper's erosion as interference, rather than as plasticity loss, is a missed unification. Likewise, the whole story hinges on normalization and the geometry of the minimum, which is adjacent to the flat-vs-sharp-minima and weight-decay results, none of which are engaged (see Further reading).

## How it could have been improved

- **Measure future learnability, not just past recall.** If fact-specific drift is plasticity loss, show it with a plasticity probe: after the update, how fast can the model learn a *fresh* task? That would connect the erosion term to the unified learning-dynamics / data-attribution framework and turn a qualitative claim ("no restoring term") into a measured capacity curve.
- **Vary the geometry the theory says matters.** The model predicts no recovery without normalization and a central role for the curvature of the minimum. So test LayerNorm vs RMSNorm vs none on a *real* LM, and measure whether a flatter pretraining minimum (sharpness-aware pretraining, or no-LR-decay pretraining) changes the collapse depth and the erosion rate. The paper brushes against sharpness but never measures it.
- **Turn the generalization-recovery tradeoff into a usable frontier.** The repair costs new-fact accuracy because the removed direction also carries the signal that helps generalization. Sweep how much of the top direction to remove against new-fact retention and report the Pareto curve, so a practitioner has a knob rather than a binary edit.
- **Disentangle the real-entity confound** with a synthetic stimulus set where "subject reveals answer" is the only varied factor.
- **Scale the repair.** OLMo-2 1B only. Given that the ability to self-edit/repair is reported as scale-emergent in adjacent work, showing the rank-one edit holds at 7B+ and across model families would materially strengthen the practical claim.

## Verdict

**Accept, with the scope caveat.** The two-process decomposition is a real conceptual contribution and the causal interventions are convincing *within factual recall*. The direction is worth pursuing: the rank-one "un-hiding" edit is practically interesting for continual learning and, more pointedly, for safety, since it implies that behaviors "forgotten" during finetuning may be only hidden and recoverable by a weight edit. The two things that would move it from "nice mechanistic result" to "load-bearing": generalizing past key-value recall, and connecting the irreversible drift term to the plasticity-loss literature so that erosion is measured as lost learning capacity, not just lost recall.

## Further reading

The adjacent literature this paper should be read against (how training in one place changes what the model can do or learn elsewhere):

- **Learning Dynamics of Continual Learning: A Unified View of Data Attribution, Forgetting, and Plasticity Loss** — the unification the erosion term belongs in: how learning one token changes another prediction, and how updates slowly reduce what the model can learn later.
- **Can Scale Save Us From Plasticity Loss in Large Language Models?** — GPT-style models lose plasticity in multilingual continual learning, and larger models only delay the onset; directly relevant to the repair's scale dependence.
- **Weight Decay Improves Language Model Plasticity** — a base model that looks worse after pretraining can be better after finetuning; an optimizer lever the paper's normalization story ignores.
- **Pre-training LLM without Learning Rate Decay Enhances Supervised Fine-Tuning** and **(How) Learning Rates Regulate Catastrophic Overtraining** — LR decay gives sharper minima that adapt and retain worse; a prediction this paper could have tested against collapse depth.
- **Sharpness-Aware Pretraining Mitigates Catastrophic Forgetting** — flatter pretraining minima forget less after post-training; the curvature axis missing from this analysis.
- **Replaying pre-training data improves fine-tuning** and **Early Data Exposure Improves Robustness to Subsequent Fine-Tuning** — replay and data-order angles that complement the weight-edit repair, and the claim that *how* a capability is learned decides whether it survives later finetuning.
- **The Piggyback Hypothesis of Generalization** — narrow finetuning spreading to unrelated prompts through chat-template tokens; a different "spurious" spreading mechanism worth contrasting with the common shift.
