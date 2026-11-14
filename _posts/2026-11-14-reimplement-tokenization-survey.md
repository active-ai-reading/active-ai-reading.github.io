---
title: "PickyBPE - Vocabulary Trimming Reimplemented"
description: 
paper: tokenization-survey
role: coding
task: reimplement
by: [shniki]
---

## What I reimplemented
I reimplemented BPE and compared it to PickyBPE - a BPE variant used for **vocabulary trimming**, mentioned in the survey (section 3.1.3). 

PickyBPE prunes **"junk" tokens** during vocabulary building. Intermediate "junk" tokens are tokens that are needed only to form long token ('entucky' in 'Kentucky'). PickyBPE requires the following properties in order to properly prune.

- **Intersection over Self (IoS) metric.** $IoS=\frac{\text{token-pair frequency}}{\text{token frequency}}$. The closer this value is to 1 ($IoS \in [0,1]$), the more likely the token is intermediate, as it is mostly used as a step on the way to form the next merge.
- **Token removal threshold $\tau$.** A threshold for IoS value for pruning tokens. Recommended as 0.9.

To summarize, PickyBPE prunes token $a$, if there exists a token $b$ such that it satisfies $\text{IoS}(a, (a, b)) = \frac{\text{freq}(a, b)}{\text{freq}(a)} \ge \tau$.

## The code

```python
def pickybpe_training(corpus, target_vocabulary_size, tau=0.9):
    pretokenized_corpus = [
        pretoken for sentence in corpus for pretoken in pretokenize(sentence)
    ]
    base_alphabet = set(c for pretoken in pretokenized_corpus for c in pretoken)
    vocab = set(base_alphabet)
    events = []
    pruned_tokens = set()  # Prevent pruned tokens from being re-added

    while len(vocab) < target_vocabulary_size:
        token_counts = collections.Counter(
            token for pretoken in pretokenized_corpus for token in pretoken
        )
        pair_counts = collections.Counter(
            (a, b)
            for pretoken in pretokenized_corpus
            for a, b in zip(pretoken, pretoken[1:])
        )
        
        # Filter out pairs that would recreate a pruned token
        valid_pairs = {
            pair: count for pair, count in pair_counts.items()
            if (pair[0] + pair[1]) not in pruned_tokens
        }
        
        if len(valid_pairs) == 0:
            break

        max_pair = max(valid_pairs, key=valid_pairs.get)
        pair_freq = valid_pairs[max_pair]
        a, b = max_pair
        new_token = a + b

        events.append(('merge', max_pair, new_token))
        vocab.add(new_token)

        # Check IoS on multi-character components
        for component in (a, b):
            if component not in base_alphabet and component in vocab:
                ios = pair_freq / token_counts[component]
                if ios >= tau:
                    vocab.remove(component)
                    pruned_tokens.add(component)  # Mark as permanently pruned
                    events.append(('remove', component))
                    print(f"--> [PickyBPE Pruned]: '{component}' (IoS = {ios:.2f}) when forming '{new_token}'")

        for pretoken in pretokenized_corpus:
            apply_merge(pretoken, max_pair)

    return list(vocab), events, list(pruned_tokens)
```

Full code: <https://colab.research.google.com/drive/1qNGiUcsvUS8OdHkb_s3epaZSdzV1w0GR?usp=sharing>

## Results

| | Standard BPE | PickyBPE ($\tau = 0.7$) | PickyBPE ($\tau = 0.9$) |
| --- | --- | --- | --- |
| Final Vocab Size | 150 | 150 | 150 |
| Tokens Pruned | 0 | 63 | 30 | 

PickyBPE pruned 63 tokens running on the training data. This granted PickyBPE's final vocabulary **meaningful tokens that didn't appear** on BPE's vocabulary. Such as ' different', ' information', ' intermediate', ' organizations', ' pair', ' process', ' redundant', ' representations', etc. See more in colab notebook.

## What I learned

In this reimplementation experience I've achieved deeper understanding about the Byte-pair Encoding algorithm. I've explored PickyBPE, which improves the vocabulary by pruning "junk" tokens, thus **clearing up space for longer and more meaningful tokens within the same parameter count**.

I encountered several challenges during this experiment. These helped me understand that the threshold $\tau=0.9$ ensures pruning token $a$ only if it appears almost exclusively in token $b$, not the other way around.
In contrast, versatile tokens that appear in multiple, distinct words (like 'com' may appear in 'communication', 'computational', 'committees', and 'complex'), distribute their occurrences across multiple distinct tokens. Their $\text{IoS}$ per word naturally stays low ($\tau \le 0.3$), and the token 'com' wouldn't get pruned.

This highlights the **design trade-off behind $\tau$**: setting it too low (e.g., $\tau \le 0.3$) would mistakenly prune legitimate, reusable prefixes, destroying subword sharing. At $\tau = 0.9$, PickyBPE selectively eliminates path-dependent tokens without turning the subword vocabulary into an overfitted whole-word dictionary.