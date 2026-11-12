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
 <h4>The Main Idea</h4>
<p>
    Unigram is a probabilistic tokenization algorithm. Unlike BPE,
    which starts with individual characters or bytes and gradually
    merges them into larger tokens, Unigram works in the opposite
    direction. It starts with a large vocabulary of possible tokens
    and gradually removes the ones that are less useful.
</p>
<p>
    The main idea is to assume that a word can be constructed by
    independently sampling tokens from a probability distribution
    over the vocabulary.
</p>
<p>
    For example, consider the word playing. Depending on
    the vocabulary, it could be represented as:
</p>
<ul>
    <li>playing</li>
    <li>play | ing</li>
    <li>p | lay | ing</li>
</ul>
<p>
    All three tokenizations represent the same word, but Unigram
    assigns each one a different probability.
</p>
<p>
    If a tokenization consists of the tokens
    \(t_1,t_2,\ldots,t_k\), its probability is defined as:
</p>
<p>
    \[
    P(t_1,\ldots,t_k)=\prod_{i=1}^{k}p(t_i)
    \]
</p>
<p>
    Here, \(p(t)\) is the probability assigned to token \(t\).
    These probabilities are learned during training, and their
    sum over the entire vocabulary must equal 1:
</p>
<p>
    \[
    \sum_{t\in V}p(t)=1
    \]
</p>
<p>
    The goal of Unigram is to find a vocabulary and token
    probabilities that assign high likelihood to the training corpus.
</p>

<h4>Initializing the Vocabulary and Probabilities</h4>
<p>
    Before training begins, we need to construct an initial vocabulary
    and assign probabilities to its tokens.
</p>
<p>
    Unlike BPE, which begins with a small vocabulary, Unigram starts
    with a much larger set of candidate tokens.
</p>
<p>
    In the SentencePiece implementation discussed in the paper,
    the initial vocabulary contains all characters appearing in
    the training corpus, together with a large number of frequent
    substrings. These candidate substrings are identified using
    a suffix array.
</p>
<p>
    For example, if our corpus contains words such as
    play, playing, and player,
    the initial vocabulary might contain:
</p>
<p>
    \[
    V=\{\text{p},\text{l},\ldots,\text{play},
    \text{ing},\text{playing},\text{player},\ldots\}
    \]
</p>
<p>
    We also need to assign an initial probability to each candidate
    token. The exact initialization depends on the implementation.
    SentencePiece uses initial scores for its seed vocabulary.
</p>
<p>
    To understand the idea, one possible initialization is to use
    the frequency of each candidate token in the training corpus.
    If \(c_0(t)\) is the number of times the candidate token \(t\)
    appears in the training corpus, we can define:
</p>
<p>
    \[
    p_0(t)=\frac{c_0(t)}{\sum_{u\in V}c_0(u)}
    \]
</p>
<p>
    Here, the occurrences are counted as substrings, before
    choosing the final tokenization of the text.
    This gives more probability to frequently appearing
    candidates while ensuring that the probabilities sum to 1.
    This is an illustrative initialization and not necessarily
    the exact initialization procedure used by SentencePiece.
</p>
<p>
    The important point is that these probabilities are only
    initial estimates. During training, the EM algorithm updates
    them according to how well the tokens explain the training corpus.
</p>

<h4>A Simple Example</h4>
<p>
    Suppose our vocabulary contains the tokens
    play, ing, and playing, with the following initial probabilities:
</p>
<table>
    <tr>
        <td>Token</td>
        <td>Probability</td>
    </tr>
    <tr>
        <td>play</td>
        <td>0.40</td>
    </tr>
    <tr>
        <td>ing</td>
        <td>0.30</td>
    </tr>
    <tr>
        <td>playing</td>
        <td>0.10</td>
    </tr>
    <tr>
        <td>Other tokens</td>
        <td>0.20</td>
    </tr>
</table>
<p>
    These probabilities are chosen only to make the example simple.
    Now suppose we want to tokenize the word playing.
</p>
<p>
    For simplicity, assume there are only two possible tokenizations.
</p>
<p>
    Option 1: Represent the entire word as one token.
</p>
<p>
    \[
    P([\text{playing}])=0.10
    \]
</p>
<p>
    Option 2: Split the word into two tokens.
</p>
<p>
    \[
    P([\text{play},\text{ing}])
    =0.40\cdot0.30=0.12
    \]
</p>
<p>
    Since \(0.12>0.10\), the second tokenization has a higher
    probability according to our model.
    Therefore, the tokenizer would choose:
</p>
<p>
    \[
    [\text{play},\text{ing}]
    \]
</p>
<p>
    This illustrates how Unigram makes its decisions.
    Instead of following a predetermined sequence of merges,
    as BPE does, it compares the probabilities of possible
    tokenizations and chooses the most probable one.
</p>
<p>
    However, we still need to understand how these token
    probabilities are learned.
</p>

<h4>Learning the Token Probabilities</h4>
<p>
    Unigram uses an algorithm called Expectation-Maximization (EM)
    to learn the token probabilities.
</p>
<p>
    The difficulty is that the training corpus contains words,
    but we do not know which tokenization should be used for
    each word. For this reason, EM alternates between two steps.
</p>

<h5>E-step: Estimating Token Counts</h5>
<p>
    In this step, we consider all possible tokenizations of each
    word and calculate their probabilities.
</p>
<p>
    Returning to our example, the two possible tokenizations
    of playing had probabilities \(0.10\) and \(0.12\).
    The total probability assigned to the word is:
</p>
<p>
    \[
    P(\text{playing})=0.10+0.12=0.22
    \]
</p>
<p>
    We can now calculate the probability of each tokenization,
    given that the observed word is playing:
</p>
<p>
    \[
    P([\text{playing}]\mid\text{playing})
    =\frac{0.10}{0.22}\approx0.455
    \]
</p>
<p>
    \[
    P([\text{play},\text{ing}]\mid\text{playing})
    =\frac{0.12}{0.22}\approx0.545
    \]
</p>
<p>
    These probabilities tell us how likely each segmentation is,
    given the observed word.
</p>
<p>
    Instead of choosing only the most probable segmentation during
    training, we use both to calculate the expected number of
    occurrences of each token.
</p>
<p>
    For this example, the expected counts are:
</p>
<table>
    <tr>
        <td>Token</td>
        <td>Expected Count</td>
    </tr>
    <tr>
        <td>playing</td>
        <td>0.455</td>
    </tr>
    <tr>
        <td>play</td>
        <td>0.545</td>
    </tr>
    <tr>
        <td>ing</td>
        <td>0.545</td>
    </tr>
</table>
<p>
    For example, play appears only in the second
    segmentation, so its expected count is \(0.545\).
</p>
<p>
    In practice, these expected counts are calculated over
    the entire training corpus.
</p>

<h5>M-step: Updating Token Probabilities</h5>
<p>
    After estimating the expected counts, we update the probability
    of each token by dividing its expected count by the total
    expected number of tokens.
</p>
<p>
    The update rule is:
</p>
<p>
    \[
    p_{\text{new}}(t)=
    \frac{\mathbb{E}[\operatorname{count}(t)]}
    {\sum_{u\in V}\mathbb{E}[\operatorname{count}(u)]}
    \]
</p>
<p>
    For our simplified example, the total expected count is:
</p>
<p>
    \[
    0.455+0.545+0.545=1.545
    \]
</p>
<p>
    Therefore, the updated probabilities would be approximately:
</p>
<p>
    \[
    p_{\text{new}}(\text{playing})
    =\frac{0.455}{1.545}\approx0.294
    \]
</p>
<p>
    \[
    p_{\text{new}}(\text{play})
    =\frac{0.545}{1.545}\approx0.353
    \]
</p>
<p>
    \[
    p_{\text{new}}(\text{ing})
    =\frac{0.545}{1.545}\approx0.353
    \]
</p>
<p>
    Notice that these probabilities sum to 1, up to rounding.
    In this simplified corpus, the other candidate tokens
    have zero expected counts.
</p>
<p>
    Here we considered only one training word to keep the
    calculation simple. With a real corpus, the update would
    account for all the words and all their possible segmentations.
</p>
<p>
    The algorithm repeats the E-step and M-step.
    The updated token probabilities change the probabilities
    of possible segmentations, which in turn change the
    expected token counts.
</p>
<p>
    This process improves the likelihood assigned to the training
    corpus under the current vocabulary.
</p>

<h4>Removing Tokens from the Vocabulary</h4>
<p>
    So far, we have only learned probabilities for the tokens,
    but Unigram also needs to decide which tokens should remain
    in the vocabulary.
</p>
<p>
    As mentioned earlier, the algorithm begins with a large
    vocabulary containing many possible substrings.
    However, keeping all these tokens would require a large
    embedding table in the language model.
</p>
<p>
    To reduce the vocabulary size, Unigram periodically removes
    tokens. The important point is that we do not simply remove
    the tokens with the lowest probabilities.
</p>
<p>
    Instead, we estimate how much the likelihood of the
    training corpus would decrease if a particular token
    were removed.
</p>
<p>
    Conceptually, we can define the loss caused by removing
    token \(t\) as:
</p>
<p>
    \[
    \operatorname{Loss}(t)=
    \log P(D\mid V)-
    \log P(D\mid V\setminus\{t\})
    \]
</p>
<p>
    Here:
</p>
<ul>
    <li>
        \(D\) is the training corpus.
    </li>
    <li>
        \(V\) is the current vocabulary.
    </li>
    <li>
        \(t\) is the token we are considering removing.
    </li>
    <li>
        \(V\setminus\{t\}\) is the vocabulary after removing
        token \(t\).
    </li>
</ul>
<p>
    The probabilities also depend on the token probability
    parameters, which are omitted from the notation for simplicity.
</p>
<p>
    The idea behind this equation is to compare how well
    the model explains the training corpus before and after
    removing the token.
</p>
<p>
    A small loss means that the token can be removed without
    significantly affecting the likelihood assigned to the data.
</p>

<h5>Example: Removing a Token</h5>
<p>
    Let's return to our previous example, where the training
    corpus consists only of the word playing.
</p>
<p>
    Recall that the initial probabilities were:
</p>
<p>
    \[
    p(\text{play})=0.4,\quad
    p(\text{ing})=0.3,\quad
    p(\text{playing})=0.1
    \]
</p>
<p>
    For simplicity, assume there are only two possible
    tokenizations:
</p>
<p>
    \[
    [\text{playing}]
    \qquad\text{and}\qquad
    [\text{play},\text{ing}]
    \]
</p>
<p>
    The total probability assigned to the word using
    the current vocabulary is:
</p>
<p>
    \[
    P(D\mid V)=0.1+(0.4\cdot0.3)=0.22
    \]
</p>
<p>
    Now suppose we want to remove the token
    playing from our vocabulary.
</p>
<p>
    After removing it, the only remaining possible
    tokenization is:
</p>
<p>
    \[
    [\text{play},\text{ing}]
    \]
</p>
<p>
    If we temporarily keep the probabilities of the
    other tokens unchanged, the remaining score
    assigned to this word is:
</p>
<p>
    \[
    P_{\text{remaining}}(D)=0.4\cdot0.3=0.12
    \]
</p>
<p>
    Therefore, the decrease in log-likelihood under
    these fixed scores is:
</p>
<p>
    \[
    \begin{aligned}
    \operatorname{Loss}(\text{playing})
    &=\log(0.22)-\log(0.12)\\
    &=\log\left(\frac{0.22}{0.12}\right)\\
    &\approx0.606
    \end{aligned}
    \]
</p>
<p>
    This shows that removing playing eliminates
    one possible way to represent the word, but another
    segmentation remains available.
</p>
<p>
    This calculation is a simplified illustration using
    fixed scores. After permanently removing a token,
    the remaining probabilities must be normalized
    and can later be re-estimated by EM.
    Therefore, the actual change in corpus likelihood
    can be different from \(0.606\).
</p>
<p>
    Now imagine a larger corpus containing many occurrences
    of player, playing, and playful.
</p>
<p>
    Removing play might affect many different
    words, whereas removing playing might be
    less harmful because it can be replaced by
    play and ing.
</p>
<p>
    We would therefore prefer to remove the token
    with the smaller estimated removal loss.
</p>

<h4>Tokenization During Inference</h4>
<p>
    Once training is complete, the tokenizer has a fixed
    vocabulary and a probability assigned to each token.
</p>
<p>
    When a new word is given, the tokenizer needs to find
    the sequence of vocabulary tokens with the highest
    probability.
</p>
<p>
    For a tokenization consisting of \(t_1,\ldots,t_k\),
    this means finding:
</p>
<p>
    \[
    z^*=
    \arg\max_{z\in T(w)}
    \prod_{t\in z}p(t)
    \]
</p>
<p>
    Where \(T(w)\) is the set of all valid tokenizations
    of the input word \(w\).
</p>
<p>
    Equivalently, using log-probabilities:
</p>
<p>
    \[
    z^*=
    \arg\max_{z\in T(w)}
    \sum_{t\in z}\log p(t)
    \]
</p>
<p>
    Since a word may have many possible segmentations,
    enumerating all of them individually can be expensive.
</p>
<p>
    Instead, Unigram uses the Viterbi algorithm, a
    dynamic programming algorithm that efficiently
    finds the most probable segmentation by reusing
    the best solutions for shorter prefixes of the input.
</p>
<p>
    The result is a deterministic tokenization.
    However, Unigram can also sample different
    tokenizations according to their probabilities
    during training, a technique known as
    subword regularization.
</p>

<h4>Summary</h4>
<p>
    To summarize, the Unigram algorithm works as follows:
</p>
<ol>
    <li>
        Start with a large vocabulary of candidate tokens
        and initialize their probabilities.
    </li>
    <li>
        Use EM to estimate how frequently each token
        is used and update its probability.
    </li>
    <li>
        Estimate how much the corpus likelihood would
        decrease if each token were removed.
    </li>
    <li>
        Remove the least useful tokens and repeat
        the process until the desired vocabulary
        size is reached.
    </li>
    <li>
        During inference, use Viterbi to find the
        most probable tokenization of the input.
    </li>
</ol>
  </div>
</div>

## The general rule

What rule did you apply that others could use in their own writing? (e.g. "Lead with the finding, not the method.")

<!-- For key-points: list the 3 points most readers should leave with, where the paper currently says them, and how they could be emphasized better (title? figure 1? first sentence of the intro?). -->
