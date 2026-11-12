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

### 2.1 The Main Idea

Unigram is a probabilistic tokenization algorithm. Unlike BPE, which starts with individual characters or bytes and gradually merges them into larger tokens, Unigram works in the opposite direction. It starts with a large vocabulary of possible tokens and gradually removes the ones that are less useful.

The main idea is to assume that a word can be constructed by independently sampling tokens from a probability distribution over the vocabulary.

For example, consider the word *playing*. Depending on the vocabulary, it could be represented as

- `[playing]`

- `[play, ing]`

- `[p, lay, ing]`

All three tokenizations represent the same word, but Unigram assigns each one a different probability.

If a tokenization consists of the tokens $t_1,t_2,\ldots,t_k$, its probability is defined as

$$
P(t_1,\ldots,t_k)=\prod_{i=1}^{k}p(t_i).
$$

Here, $p(t)$ is the probability assigned to token $t$. These probabilities are learned during training, and their sum over the entire vocabulary must equal 1:

$$
\sum_{t\in V}p(t)=1.
$$

The goal of Unigram is to find a vocabulary and token probabilities that assign high likelihood to the training corpus.

### 2.2 Initializing the Vocabulary and Probabilities

Before training begins, we need to construct an initial vocabulary and assign probabilities to its tokens.

Unlike BPE, which begins with a small vocabulary, Unigram starts with a much larger set of candidate tokens. In the SentencePiece implementation discussed in the paper, the initial vocabulary contains all characters appearing in the training corpus, together with a large number of frequent substrings. These candidate substrings are identified using a suffix array.

For example, if our corpus contains words such as *play*, *playing*, and *player*, the initial vocabulary might contain

$$
V=\{\texttt{p},\texttt{l},\ldots,\texttt{play},\texttt{ing},\texttt{playing},\texttt{player},\ldots\}.
$$

We also need to assign an initial probability to each candidate token. The paper does not specify one universal initialization rule, since the exact procedure depends on the implementation. SentencePiece uses initial scores for its seed vocabulary.

To understand the idea, one possible initialization is to use estimated token frequencies. If $c_0(t)$ is an initial frequency-based weight assigned to token $t$, we can define

$$
p_0(t)=\frac{c_0(t)}{\sum_{u\in V}c_0(u)}.
$$

This assigns more probability to frequent candidates while ensuring that the probabilities sum to 1. It is an illustrative initialization, not a claim about the exact default used by SentencePiece.

The important point is that these probabilities are only initial estimates. The EM algorithm will update them according to how well the candidate tokens explain the training corpus.

### 2.3 A Simple Example

Suppose our vocabulary contains the tokens `play`, `ing`, and `playing`, with the following initial probabilities:

| Token | Probability |
|---|---:|
| `play` | 0.40 |
| `ing` | 0.30 |
| `playing` | 0.10 |
| Other tokens | 0.20 |

These values are chosen only to make the example simple. For this example, suppose the word *playing* has only two possible tokenizations.

Option 1: Represent the entire word as one token.

$$
P([\texttt{playing}])=0.10.
$$

Option 2: Split the word into two tokens.

$$
P([\texttt{play},\texttt{ing}])=0.40\cdot 0.30=0.12.
$$

Since $0.12>0.10$, the second tokenization has a higher probability according to the model. The tokenizer therefore chooses $[\mathrm{play},\mathrm{ing}]$. Unlike BPE, Unigram does not replay a learned sequence of merges. It compares the probabilities of possible segmentations and selects the most probable one.

### 2.4 Learning the Token Probabilities

Unigram uses Expectation-Maximization (EM) to learn token probabilities. The difficulty is that the training corpus contains words, but we do not know which segmentation should be used for each word. EM therefore alternates between two steps.

#### E-step: Estimating Token Counts

In this step, we consider all valid tokenizations of each word and calculate their probabilities. In our example, the two tokenizations of *playing* have probabilities $0.10$ and $0.12$.

The total probability assigned to the word is

$$
P(\texttt{playing})=0.10+0.12=0.22.
$$

We then calculate the conditional probability of each tokenization, given that we observed the word *playing*:

$$
\begin{aligned}
    P([\texttt{playing}]\mid\texttt{playing})
    &=\frac{0.10}{0.22}\approx0.455,\\
    P([\texttt{play},\texttt{ing}]\mid\texttt{playing})
    &=\frac{0.12}{0.22}\approx0.545.
\end{aligned}
$$

Instead of choosing only one segmentation during training, we use these conditional probabilities to calculate expected token counts:

| Token | Expected count |
|---|---:|
| `playing` | 0.455 |
| `play` | 0.545 |
| `ing` | 0.545 |

For example, `play` appears only in the second segmentation, so its expected count is $0.545$. In practice, expected counts are accumulated across the entire training corpus.

#### M-step: Updating Token Probabilities

After obtaining expected counts, we update each token's probability by dividing its expected count by the total expected number of tokens:

$$
p_{\mathrm{new}}(t)=
    \frac{\mathbb{E}[\operatorname{count}(t)]}
    {\sum_{u\in V}\mathbb{E}[\operatorname{count}(u)]}.
$$

In our simplified corpus, the total expected count is

$$
0.455+0.545+0.545=1.545.
$$

Therefore,

$$
\begin{aligned}
    p_{\mathrm{new}}(\texttt{playing})
    &=\frac{0.455}{1.545}\approx0.294,\\
    p_{\mathrm{new}}(\texttt{play})
    &=\frac{0.545}{1.545}\approx0.353,\\
    p_{\mathrm{new}}(\texttt{ing})
    &=\frac{0.545}{1.545}\approx0.353.
\end{aligned}
$$

These probabilities sum to 1, up to rounding. In this toy corpus, the other candidate tokens have zero expected counts.

The E-step and M-step are repeated: the updated token probabilities change the probabilities of possible segmentations, which in turn change the expected token counts. With a real corpus, this process uses all observed words and their possible segmentations.

### 2.5 Removing Tokens from the Vocabulary

The EM algorithm updates token probabilities, but Unigram also needs to decide which tokens to keep. The vocabulary starts large and is gradually reduced to a desired size.

We do not simply remove tokens with the smallest probabilities. Instead, we want to remove tokens whose absence causes the least harm to the likelihood of the training corpus.

Conceptually, the loss caused by removing a token $t$ can be written as

$$
\operatorname{Loss}(t)
    =\log P(D\mid V)
    -\log P(D\mid V\setminus\{t\}),
$$

where $D$ is the training corpus, $V$ is the current vocabulary, and $V\setminus\{t\}$ is the vocabulary after removing $t$. This expression is shorthand: the probability also depends on the token probability parameters. Comparing full models after removal may require re-estimating these parameters.

#### Example: Removing a Token

Return to our example, where the training corpus consists only of the word *playing*. Before the EM update, the token probabilities were

$$
p(\texttt{play})=0.4,\qquad
    p(\texttt{ing})=0.3,\qquad
    p(\texttt{playing})=0.1.
$$

The two possible segmentations are $[\texttt{playing}]$ and $[\texttt{play},\texttt{ing}]$, so

$$
P(D\mid V)=0.1+(0.4\cdot0.3)=0.22.
$$

Suppose we remove the token `playing`. It is no longer available, but the word can still be represented as $[\texttt{play},\texttt{ing}]$. If we temporarily keep the scores of the other tokens fixed, the probability assigned to this word is

$$
P_{\mathrm{remaining}}(D)=0.4\cdot0.3=0.12.
$$

The decrease in log-likelihood under these fixed scores is therefore

$$
\begin{aligned}
    \operatorname{Loss}_{\mathrm{fixed}}(\texttt{playing})
    &=\log(0.22)-\log(0.12)\\
    &=\log\left(\frac{0.22}{0.12}\right)\\
    &\approx0.606.
\end{aligned}
$$

This illustrates that removing `playing` eliminates one possible way to represent the word, but another segmentation remains available.

The calculation is only an illustration: after permanently removing a token, the remaining token probabilities must be normalized and can later be re-estimated by EM. Therefore, the actual change in corpus likelihood under the updated model can be different from $0.606$.

Now imagine a larger corpus that contains many occurrences of *player*, *playing*, and *playful*. Removing `play` might affect many different words, whereas removing `playing` might be less harmful because it can be replaced by `play` and `ing`. We would therefore prefer to remove the token with the smaller estimated removal loss.

#### Approximating the Removal Loss

Computing the exact change in corpus likelihood for every candidate token would be expensive. The paper gives an approximation of the form

$$
\widehat{\operatorname{Loss}}(t)
    =c_t\left(\log p(t)-s_{-t}(t)\right),
$$

where $c_t$ is the expected count of token $t$, and

$$
s_{-t}(t)
    =\max_{z\in T(t),\;t\notin z}
      \sum_{u\in z}\log p(u)
$$

is the best log-score for representing the same string without using token $t$. This score can be found using Viterbi decoding while excluding the candidate token.

The intuition is that a token is less useful if it is rarely used or if it can be replaced by other tokens with similar scores. Tokens with the smallest estimated removal losses are candidates for pruning.

After pruning a portion of the vocabulary, Unigram repeats EM with the remaining candidates. This continues until the desired vocabulary size is reached. Necessary atomic tokens are retained so the input can still be represented.

### 2.6 Tokenization During Inference

Once training is complete, the tokenizer has a fixed vocabulary and token probabilities. To tokenize a new input word $w$, it chooses the most probable segmentation:

$$
z^*=\arg\max_{z\in T(w)}\prod_{t\in z}p(t).
$$

Equivalently, using log-probabilities,

$$
z^*=\arg\max_{z\in T(w)}\sum_{t\in z}\log p(t).
$$

Since a word can have many possible segmentations, testing all of them separately would be expensive. Instead, Unigram uses the Viterbi algorithm, which finds the most probable segmentation by reusing optimal solutions for shorter prefixes of the input.

This produces a deterministic segmentation at inference time. During training, Unigram can also sample alternative segmentations according to their probabilities, a technique known as subword regularization.

### 2.7 Summary

The Unigram algorithm can be summarized as follows:

1.  Start with a large vocabulary of candidate tokens and initialize their probabilities.

2.  Use EM to estimate expected token counts and update token probabilities.

3.  Estimate the loss of removing each candidate token.

4.  Remove the least useful tokens and repeat until the desired vocabulary size is reached.

  </div>
</div>

## The general rule

What rule did you apply that others could use in their own writing? (e.g. "Lead with the finding, not the method.")

<!-- For key-points: list the 3 points most readers should leave with, where the paper currently says them, and how they could be emphasized better (title? figure 1? first sentence of the intro?). -->
