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
 
## 2. Proposed Rewrite: Unigram Language Modeling Tokenization

### 2.1 The Main Idea

Unigram is a probabilistic tokenization algorithm. Unlike BPE, which starts with individual characters or bytes and gradually merges them into larger tokens, Unigram works in the opposite direction. It starts with a large vocabulary of possible tokens and gradually removes the ones that are less useful.

The main idea is to assume that a word can be constructed by independently sampling tokens from a probability distribution over the vocabulary.

For example, consider the word *playing*. Depending on the vocabulary, it could be represented as:

- `[playing]`
- `[play, ing]`
- `[p, lay, ing]`

All three tokenizations represent the same word, but Unigram assigns each one a different probability.

If a tokenization consists of the tokens \(t_1,t_2,\ldots,t_k\), its probability is defined as:

\[
P(t_1,\ldots,t_k)=\prod_{i=1}^{k}p(t_i)
\]

Here, \(p(t)\) is the probability assigned to token \(t\). These probabilities are learned during training, and their sum over the entire vocabulary must equal 1:

\[
\sum_{t\in V}p(t)=1
\]

The goal of Unigram is to find a vocabulary and token probabilities that assign high likelihood to the training corpus.

### 2.2 Initializing the Vocabulary and Probabilities

Before training begins, we need to construct an initial vocabulary and assign probabilities to its tokens.

Unlike BPE, which begins with a small vocabulary, Unigram starts with a much larger set of candidate tokens.

In the SentencePiece implementation discussed in the paper, the initial vocabulary contains all characters appearing in the training corpus, together with a large number of frequent substrings. These candidate substrings are identified using a suffix array.

For example, if our corpus contains words such as *play*, *playing*, and *player*, the initial vocabulary might contain:

\[
V=\{\text{p},\text{l},\ldots,\text{play},\text{ing},\text{playing},\text{player},\ldots\}
\]

We also need to assign an initial probability to each candidate token.

The paper does not specify one general formula for initializing these probabilities, since the exact initialization depends on the implementation. The SentencePiece implementation uses initial scores for its seed vocabulary.

To understand the idea, one possible initialization is to use estimated token frequencies. If \(c_0(t)\) is an initial frequency-based weight assigned to token \(t\), we can define:

\[
p_0(t)=\frac{c_0(t)}{\sum_{u\in V}c_0(u)}
\]

This gives more probability to frequently occurring candidates while ensuring that the probabilities sum to 1. It is a simple illustrative initialization, rather than the exact initialization rule specified by SentencePiece.

The important point is that these are only initial estimates. During training, the EM algorithm will update the probabilities according to how useful the tokens are for representing the corpus.

### 2.3 A Simple Example

Suppose our vocabulary contains the tokens `play`, `ing`, and `playing`, with the following initial probabilities:

| Token | Probability |
|---|---|
| play | 0.40 |
| ing | 0.30 |
| playing | 0.10 |
| Other tokens | 0.20 |

These are illustrative probabilities, chosen to make the example simple.

Now suppose we want to tokenize the word *playing*.

For simplicity, assume there are only two possible tokenizations.

Option 1: Represent the entire word as one token.

\[
P([\text{playing}])=0.10
\]

Option 2: Split the word into two tokens.

\[
P([\text{play},\text{ing}])=0.40\cdot0.30=0.12
\]

Since \(0.12>0.10\), the second tokenization has a higher probability according to our model.

Therefore, the tokenizer would choose:

\[
[\text{play},\text{ing}]
\]

This illustrates how Unigram makes its decisions. Instead of following a predetermined sequence of merges, as BPE does, it compares the probabilities of the possible tokenizations and chooses the most probable one.

However, we still need to understand how these token probabilities are learned.

### 2.4 Learning the Token Probabilities

Unigram uses an algorithm called Expectation-Maximization (EM) to learn the token probabilities.

The difficulty is that the training corpus contains words, but we do not know which tokenization should be used for each word.

For this reason, EM alternates between two steps.

#### E-step: Estimate How Often Each Token Is Used

In this step, we consider all possible tokenizations of each word and calculate their probabilities.

Returning to our example, the two possible tokenizations of *playing* had probabilities 0.10 and 0.12.

The total probability assigned to the word is:

\[
P(\text{playing})=0.10+0.12=0.22
\]

We can now calculate the probability of each tokenization, given that the observed word is *playing*:

\[
P([\text{playing}]\mid\text{playing})
=\frac{0.10}{0.22}\approx0.455
\]

\[
P([\text{play},\text{ing}]\mid\text{playing})
=\frac{0.12}{0.22}\approx0.545
\]

These probabilities tell us how likely each segmentation is, given the observed word.

Instead of choosing only the most probable segmentation during training, we use both to calculate the expected number of occurrences of each token.

For this example, the expected counts are:

| Token | Expected count |
|---|---|
| playing | 0.455 |
| play | 0.545 |
| ing | 0.545 |

For example, `play` appears only in the second tokenization, so its expected count is 0.545.

In practice, these expected counts are calculated over the entire training corpus.

#### M-step: Update the Token Probabilities

After estimating the expected counts, we update the probability of each token by dividing its expected count by the total expected number of tokens.

The update rule is:

\[
p_{\text{new}}(t)=
\frac{\mathbb E[\operatorname{count}(t)]}
{\sum_{u\in V}\mathbb E[\operatorname{count}(u)]}
\]

For our simplified example, the total expected count is:

\[
0.455+0.545+0.545=1.545
\]

Therefore, the updated probabilities would be approximately:

\[
p_{\text{new}}(\text{playing})
=\frac{0.455}{1.545}\approx0.294
\]

\[
p_{\text{new}}(\text{play})
=\frac{0.545}{1.545}\approx0.353
\]

\[
p_{\text{new}}(\text{ing})
=\frac{0.545}{1.545}\approx0.353
\]

Notice that these probabilities sum to 1, up to rounding. In this simplified corpus, the other candidate tokens have zero expected counts.

Here we considered only one training word to keep the calculation simple. With a real corpus, the update would account for all the words and all the possible segmentations.

The algorithm repeats the E-step and M-step, using the updated probabilities to calculate new expected counts. This process improves the likelihood assigned to the training corpus under the current vocabulary.

### 2.5 Removing Tokens from the Vocabulary

So far, we have only learned probabilities for the tokens, but Unigram also needs to decide which tokens should remain in the vocabulary.

As mentioned earlier, the algorithm begins with a large vocabulary containing many possible substrings. However, keeping all these tokens would require a large embedding table in the language model.

To reduce the vocabulary size, Unigram periodically removes tokens.

The important point is that we do not simply remove the tokens with the lowest probabilities.

Instead, we estimate how much the likelihood of the training corpus would decrease if a particular token were removed.

Conceptually, we can define the loss caused by removing token \(t\) as:

\[
\operatorname{Loss}(t)
=
\log P(D\mid V)
-
\log P(D\mid V\setminus\{t\})
\]

where \(D\) is the training corpus, \(V\) is the current vocabulary, and \(V\setminus\{t\}\) is the vocabulary without token \(t\). The probabilities here are understood to be calculated under the corresponding Unigram models.

This equation measures how much worse the corpus likelihood becomes when we can no longer use token \(t\).

#### Example: Removing a Token

Let's return to our previous example, where the training corpus consists only of the word *playing*.

Recall that the initial probabilities were:

\[
p(\text{play})=0.4,\quad
p(\text{ing})=0.3,\quad
p(\text{playing})=0.1
\]

For simplicity, assume there are only two possible tokenizations of this word:

\[
[\text{playing}]
\qquad\text{and}\qquad
[\text{play},\text{ing}]
\]

The total probability of the word using the current vocabulary is:

\[
P(D\mid V)
=
0.1+(0.4\cdot0.3)
=
0.22
\]

Now suppose we want to remove the token `playing` from our vocabulary.

After removing it, the only remaining possible tokenization is:

\[
[\text{play},\text{ing}]
\]

Keeping the other token scores unchanged temporarily, the probability assigned to the word becomes:

\[
P_{\text{remaining}}(D)
=
0.4\cdot0.3
=
0.12
\]

Therefore, the decrease in log-likelihood under these fixed scores is:

\[
\begin{aligned}
\operatorname{Loss}(\text{playing})
&=\log(0.22)-\log(0.12)\\
&=\log\left(\frac{0.22}{0.12}\right)\\
&\approx0.606
\end{aligned}
\]

This means that removing `playing` reduces the log-likelihood of our example by approximately 0.606 before adjusting the remaining token probabilities.

This is a simplified illustration of the removal cost. Strictly speaking, after removing a token, the remaining token probabilities must be normalized and can be re-estimated using EM, so the final likelihood change may differ.

We would perform a similar calculation for other candidate tokens and prefer removing those that have the smallest estimated effect on the corpus likelihood.

For example, removing `play` might be more harmful if our training corpus also contains many words such as *player* and *playful*, since the token `play` could be useful in representing all of them.

#### Approximating the Removal Loss

Calculating the exact change in corpus likelihood for every possible token removal would be computationally expensive.

The implementation presented in the paper uses an approximation:

\[
\operatorname{Loss}(t)
\approx
c_t\left(
\log p(t)
-
\operatorname{BestAlternativeLogScore}(t)
\right)
\]

Here:

- \(c_t\) is the expected count of token \(t\).
- \(\log p(t)\) is the log-probability of representing the string using token \(t\) directly.
- \(\operatorname{BestAlternativeLogScore}(t)\) is the highest log-probability of representing the same string using other tokens, without using \(t\).

The alternative score is calculated using the Viterbi algorithm.

The intuition is that if a token rarely appears, or if it can easily be replaced by other tokens with similar probabilities, removing it is less harmful.

The algorithm estimates the loss caused by removing each token and removes a fraction of the least useful ones, meaning those with the smallest estimated removal loss.

It then runs EM again to update the probabilities using the reduced vocabulary.

This process continues until the desired vocabulary size is reached. Essential atomic tokens, such as individual characters in a character-based implementation, are preserved so that the tokenizer can still represent the input text.

### 2.6 Tokenization During Inference

Once training is complete, the tokenizer has a fixed vocabulary and a probability assigned to each token.

When a new word is given, the tokenizer needs to find the sequence of vocabulary tokens with the highest probability.

For a tokenization consisting of \(t_1,\ldots,t_k\), this means finding:

\[
(t_1^*,\ldots,t_k^*)
=
\arg\max_{(t_1,\ldots,t_k)\in T(w)}
\prod_{i=1}^{k}p(t_i)
\]

where \(T(w)\) is the set of all valid tokenizations of the input word \(w\).

Since a word may have many possible segmentations, enumerating all of them individually can be expensive.

Instead, Unigram uses the Viterbi algorithm, a dynamic programming algorithm that efficiently finds the most probable segmentation by reusing the best solutions for shorter prefixes of the input.

The result is a deterministic tokenization, although Unigram can also sample different tokenizations according to their probabilities during training.

### 2.7 Summary

To summarize, the Unigram algorithm works as follows:

1. Start with a large vocabulary of candidate tokens and initialize their probabilities.
2. Use EM to estimate how frequently each token is used and update its probability.
3. Estimate how much the corpus likelihood would decrease if each token were removed.
4. Remove the least useful tokens and repeat the process until the desired vocabulary size is reached.
5. During inference, use Viterbi to find the most probable tokenization of the input.
  </div>
</div>

## The general rule

What rule did you apply that others could use in their own writing? (e.g. "Lead with the finding, not the method.")

<!-- For key-points: list the 3 points most readers should leave with, where the paper currently says them, and how they could be emphasized better (title? figure 1? first sentence of the intro?). -->
