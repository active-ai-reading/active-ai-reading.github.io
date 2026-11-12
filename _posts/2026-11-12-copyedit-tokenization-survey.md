---
title: "Rewriting Section 3.2 — Unigram Language Modeling Tokenization"
description: a detailed explanation of the unigram tokenization
paper: tokenization-survey
role: writing
task: copyedit
by: [matan2001]
---

<!-- Keep the sections that fit your task, delete the rest. -->

## What I changed and why

I chose to rewrite Section 3.2, which explains the Unigram tokenization algorithm.

I think the original section gives a good technical overview of the algorithm, but it moves quite quickly through the main ideas. In particular, it introduces the probabilistic model, the Expectation-Maximization (EM) algorithm, and vocabulary pruning without really showing how they work together.

For someone who is not already familiar with these concepts, I think it can be difficult to understand the intuition behind the algorithm. For example, it is not immediately clear why we assign probabilities to tokens, how these probabilities are initialized and updated, or how we decide which tokens to remove from the vocabulary.

My goal is to make the explanation more accessible to someone learning about tokenization for the first time. I would first explain the main idea behind Unigram and how it differs from BPE, then go through its training process step by step, using a small numerical example to demonstrate how the probabilities are calculated and updated.
## Before and after

<div class="before-after">
  <div class="before"><span class="label">Before</span>
  3.2 Unigram Language Modeling Tokenization
The Unigram tokenization algorithm (Kudo, 2018), sometimes known as UnigramLM or ULM, takes a prob
abilistic modeling approach to tokenization. The main underlying assumption of Unigram is that text is the
surface realization of samples from a latent-variable generative model. This generative model is parame
terized by a unigram distribution; each token in a token sequence is drawn independently from a unigram
language model, and the strings we see are the concatenations of them. Tokenization is then simply the
recovery of this underlying segmentation. We provide a brief description of the algorithm here; for a more
in-depth exposition, see Meister (2025).
Given the above probabilistic foundation, the first practical challenge lies in learning the specific parameters—
namely, the vocabulary and unigram distribution probabilities. The Unigram algorithm provides a top
down vocabulary construction method for learning both of these parameters. The training algorithm
uses expectation-maximization (EM) with iterative vocabulary pruning. Starting from a large initial seed
vocabulary, the algorithm alternates between: (1) computing expected (E) token counts across all possible
segmentations of the corpus, weighted by their probability under the current model; and (2) updating token
probabilities via maximum (M) likelihood. After each EM iteration, a pruning step removes tokens whose
absence causes the smallest decrease in corpus log-likelihood, continuing until the desired vocabulary size is
reached. A reference implementation is given in Code 3.4.
At inference time, we must choose a segmentation according to this model. Unigram chooses the most
probable segmentation under the model, which can be found efficiently via the Viterbi algorithm (Viterbi,
1967), as shown in Code 3.5.
In practice, the Unigram algorithm is primarily defined by its implementation in SentencePiece (Kudo &
Richardson, 2018), which makes several engineering choices not fully specified in the original paper. These
include vocabulary initialization via suffix arrays, a Bayesian variant of the M-step, and approximations to
the pruning loss computation. Recent work has provided clearer documentation of these implementation
details (Land & Pinter, 2026), finding that many expensive defaults have minimal impact on the final
tokenizer. MinGram (Land, 2026b) takes this further, replacing the suffix-array initialization with a BPE
derived seed vocabulary, marginal EM with hard EM over a minimum-token path, and the iterative pruning
loop with a single score-based pruning step. Sequence compression becomes the primary training objective,
with the learned unigram score retained only as a tiebreak among equally short segmentations.
Unigram provides several advantages over BPE, creating seemingly more morphologically plausible to
kens (Bostrom & Durrett, 2020; Vemula et al., 2025b). Despite these advantages, its adoption has been
limited, perhaps in part due to the inference efficiency of BPE, which makes it an appealing choice for
practitioners. Due to its probabilistic nature, Unigram naturally supports subword regularization (see Sec
tions 3.7 and 8): sampling from the distribution over segmentations during training, which can improve
model robustness (Kudo, 2018). BPE achieves a similar effect only through ad hoc modifications such as
BPE-dropout (Provilkov et al., 2020)
  </div>
  <div class="after"><span class="label">After</span>
  </div>
</div>

## The general rule

What rule did you apply that others could use in their own writing? (e.g. "Lead with the finding, not the method.")

<!-- For key-points: list the 3 points most readers should leave with, where the paper currently says them, and how they could be emphasized better (title? figure 1? first sentence of the intro?). -->
