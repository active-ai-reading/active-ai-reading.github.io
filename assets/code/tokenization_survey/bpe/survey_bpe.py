"""Code 3.1, 3.2 and 3.3 of "Tokenization: A Survey for Modern NLP" (Section 3.1), as printed in the survey.

Only change: the PDF lost the indentation of two lines in Code 3.1 and Code 3.3; it is restored here.
The functions are otherwise copied unchanged (names, logic, tie-breaking).
"""
import collections, re


def pretokenize(sentence):
    """ A simple, example pretokenization function.
    "Hello, world!" -> [['H', 'e', 'l', 'l', 'o'], [','], [' ', 'w', 'o', 'r', 'l', 'd'], ['!']]
    """
    PRETOKEN_REGEX = re.compile(r" ?[^?,.;'! ]+|[?,.;'!]")
    return [list(pretoken) for pretoken in PRETOKEN_REGEX.findall(sentence)]


def apply_merge(sequence, pair):
    idx = 0
    a, b = pair

    while idx < len(sequence) - 1:
        if sequence[idx] == a and sequence[idx + 1] == b:
            sequence[idx : idx + 2] = [a + b]
        idx += 1


def bpe_training(corpus, target_vocabulary_size):                      # Code 3.1
    pretokenized_corpus = [
        pretoken for sentence in corpus for pretoken in pretokenize(sentence)
    ]

    # Seed the vocabulary with all unique characters in the corpus.
    vocab = sorted({c for pretoken in pretokenized_corpus for c in pretoken})
    merges = []

    # Repeat until we reach the target vocabulary size.
    while len(vocab) < target_vocabulary_size:
        pair_counts = collections.Counter(
            (a, b)
            for pretoken in pretokenized_corpus
            for a, b in zip(pretoken, pretoken[1:])
        )

        # If there are no more possible pairs (each pretoken is a single token), stop early.
        if len(pair_counts) == 0: break

        # Add the most common pair information to the vocab and update the corpus.
        max_pair = max(pair_counts, key=pair_counts.get)
        merges.append(max_pair)
        vocab.append(max_pair[0] + max_pair[1])

        for pretoken in pretokenized_corpus:
            apply_merge(pretoken, max_pair)
    return vocab, merges


def bpe_inference(sentence, merges):                                   # Code 3.2 (iterative)
    pretokenized_sequence = pretokenize(sentence)

    # Apply each merge in order to each pretoken independently.
    for merge in merges:
        for pretoken in pretokenized_sequence:
            apply_merge(pretoken, merge)

    # Return the final tokenized forms of all pretokens.
    return [
        token
        for pretoken in pretokenized_sequence
        for token in pretoken
    ]


def bpe_inference_priority(sentence, merges):                          # Code 3.3 (priority)
    # A token pair -> index mapping for fast lookup (this can be precomputed).
    ranks = {pair: rank for rank, pair in enumerate(merges)}

    def encode(pretoken):
        while len(pretoken) > 1:
            # Among all token bigrams, keep the ones that are in the merge list.
            possible_merges = [
                pair for pair in zip(pretoken, pretoken[1:]) if pair in ranks
            ]

            # If there are no candidate merges, end early.
            if len(possible_merges) == 0: break

            # Find the available merge that is earliest in the merge list.
            merge = min(possible_merges, key=ranks.get)

            apply_merge(pretoken, merge)
        return pretoken

    # Return the final tokenized forms of all pretokens.
    return [
        token
        for pretoken in pretokenize(sentence)
        for token in encode(pretoken)
    ]
