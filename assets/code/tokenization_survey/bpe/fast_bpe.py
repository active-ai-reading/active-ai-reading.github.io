"""Independent re-implementation of BPE training/inference, written WITHOUT looking at survey_bpe.py's loops.

Training: pretoken -> count dictionary (the first optimization the survey mentions) and pair counts
accumulated per unique pretoken. Tie-breaking matches the survey (first pair seen, in corpus order).
Inference: a left-to-right pass per merge, but only over pretokens that contain the pair (cached per word).
"""
import re
from collections import Counter

PRETOKEN = re.compile(r" ?[^?,.;'! ]+|[?,.;'!]")


def pretokens(text):
    return PRETOKEN.findall(text)


def merge_word(word, a, b):
    out, i, n = [], 0, len(word)
    while i < n:
        if i < n - 1 and word[i] == a and word[i + 1] == b:
            out.append(a + b); i += 2
        else:
            out.append(word[i]); i += 1
    return tuple(out)


def train(corpus_text, target_vocab):
    counts = Counter(pretokens(corpus_text))          # insertion order = first occurrence
    words = {w: tuple(w) for w in counts}
    vocab = sorted({c for w in counts for c in w})
    merges = []
    while len(vocab) < target_vocab:
        pairs = {}
        for w, seq in words.items():
            c = counts[w]
            for p in zip(seq, seq[1:]):
                pairs[p] = pairs.get(p, 0) + c
        if not pairs:
            break
        best = max(pairs, key=pairs.get)
        merges.append(best); vocab.append(best[0] + best[1])
        for w, seq in words.items():
            if best[0] in seq:
                words[w] = merge_word(seq, *best)
    return vocab, merges
