---
title: "Critique of LLM-JEPA: LARGE LANGUAGE MODELS MEET JOINT
EMBEDDING PREDICTIVE ARCHITECTURES"
description: Necessity of JEPA-loss via Fig 3 is flawed; effect of different k values unclear
paper: llm-jepa
task: critique
by: deamir
---

<!-- Keep the block for your task, delete the others. To cite, add the BibTeX to _bibliography/references.bib and use the cite tag (see the guide page). -->

<!-- CRITIQUE -->
## Weaknesses

**Writing and notation.** Apart from grammatical errors, the notation has been incoherent. Specifically, `Pred(Enc(TEXT))` implies that `Pred` operates on a single vector, whereas it actually operates on the whole token sequence.

**Figure 3 (right).** This figure serves as a supporting evidence to the use of the `JEPA` loss term. It has several flaws:
1. _The figure is underspecified._ What is the value of `k`? What is the `x` axis, and what magnitudes of `x` values are seen in the figure?
2. _The comparison is misleading for `k>0`._ For nonzero `k`, the baseline is evaluated on tokens which it didn't train on - recall that the training for NTP does not include the `[PRED]` token. Therefore the observed loss may reflect an untrained prediction mechanism rather than a deficiency in the representations learned by the baseline model. There's also a mathematical argument that explains why the values of the loss when `k>0` are around 1. Because the embedding of `[PRED]` is randomly initialized, and never changes during training, the final-layer representation also has certain distribution properties. Assuming 'random in random out', when modeling the output embedding is uniformly distributed on the unit sphere, the expected cosine-similarity between this vector and another vector is 0, and the loss 1. _NOTE: inspecting the source code reveals that the default is `k=0`, but it's unclear how the experiment was run._
3. _Doesn't rule out the possibility that the baseline exhibits relative positive vs. negative separation._ The `JEPA` loss takes into account only 'positive' pairs, and measures the degree to which the embeddings of pair elements are close in the latent space. It doesn't take into account whether 'negative' pairs induce distant embeddings. Hence, we can't rule out from the figure (or anywhere else in the paper, as far as I know) that the baseline yields high separation in negative pairs, relative to the separation it yields on positive pairs. It could be that during training, the separation on negative pairs only grows while the separation of positive pairs stays put.
5. _Poor task diversity._ The evaluation is done over one specific task of regex generation. It's unclear whether the `JEPA` loss is required only for this task, and whether other tasks NTP objective better captures the aims of `JEPA`.

**Flaws in to evaluations.** They evaluate the models during and after training.
1. _NL-RX-SYNTH (regex)._ The way a given output is scored against the ground truth is flawed. Recall the task: the input is a natural language description of a regular expression, and the output should be the regular expression described by the input. Given a predicted regular expression, it is compared by string equality to the ground truth regex. There are multiple (infinite...) ways to write regular expressions for the same regular language. Perhaps the baseline model has certain regex styles it learned from the NTP objective, which is wrongly flagged incorrect.
2. _Rotten Tomatoes._ A dataset for the binary classification task of determining the sentiment (`Bad/Good`) of a movie review. (A) to determine whether the prediction is correct, the first generated token should be the ground truth label. There could be FNs in the scores. The two accuracy results between `baseline` (56.5%) and `LLM-JEPA` (57.7%) are very close to one another, as well as to random chance (50%). Without error analysis, it's hard to infer improvement from this result. (B) only accuracy is reported; a confusion matrix could've been insightful.

**Unclear contribution of different `k` values.** Figure 7 shows benchmarks using different `k` values. There's no clear evidence that certain values of `k` are generally better than others. 
1. In some cases, `k=0` gives better/comparable results to larger values. This calls into question the practical benefits of the additional nonlinear processing provided by predictor tokens.
2. Why is larger `k` more important on some tasks but not others? Is there a certain task type that most benefits from larger `k`?
3. Whether and how the benefits of large `k` diminish on longer tasks? Where longer means that the input given to the model is larger.

**Underspecification of the negative pair attempt.** The authors say they tried training using negative samples as well, with the `InfoNCE` loss, and got worse results. It doesn't fit with the intuition, and hence should have been expanded upon in detail. Key knowledge missing: 1) how many negative samples per positive sample was used in a single step? 2) what negatives did they choose, and how difficult were they?

## How it could have been improved

**Figure 3 (right).** 
1) Label both axes
2) state `k` value
3) separate it into two graphs one per evaluated loss
4) add evaluation over (hard) negative pairs as well
5) evaluate over multiple datasets with differing characteristics (and come up with a satisfactory definition of 'characteristics')

**Evaluations: NL-RX-SYNTH**. Instead of string equality, compare the predicted and ground truth regular expressions in terms of the languages they capture. There are algorithms that decide whether two regular expressions have the same language.

**Evaluations: Rotten tomatoes.** (1) Do error analysis. Show that we don't need to worry about mis-deserializations. (2) provide confusion matrices.

**Effects of `k`.** (1) try to understand which tasks demand large/small `k`, maybe one may characterize them. (2) fix large `k`, vary evaluation datasets by length (need to keep the same task though), find out the diminishing returns rule.




## Verdict
While the paper does propose and test a direction worth pursuing, I wouldn't accept the paper as is.
