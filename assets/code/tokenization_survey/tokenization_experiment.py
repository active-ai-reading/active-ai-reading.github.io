
#!/usr/bin/env python3
"""Compare MaxMatch and PathPiece tokenization.

Reproduces Example 3.3 from Tokenization: A Survey for Modern NLP,
then runs a new exhaustive synthetic experiment.

Requires: Python 3.9+ and matplotlib
"""

from itertools import product
import csv

PAPER_TEXT = "abcdefg"
PAPER_VOCAB = set("abcdefg") | {"abc", "abcd", "bcdef", "defg"}

BENCHMARK_VOCAB = {
    "a", "b", "aa", "aaa", "aaaa", "ab", "aba", "abab",
    "bab", "baba", "baab", "bbab", "abb", "bbbb",
}

MAX_LENGTH = 10


def maxmatch(text, vocabulary):
    """Greedily select the longest available prefix."""
    vocabulary = set(vocabulary)
    if not text:
        return []

    max_token_length = max(map(len, vocabulary))
    result = []
    i = 0

    while i < len(text):
        for size in range(
            min(max_token_length, len(text) - i), 0, -1
        ):
            token = text[i:i + size]
            if token in vocabulary:
                result.append(token)
                i += size
                break
        else:
            raise ValueError(
                f"No vocabulary token covers index {i}"
            )

    return result


def pathpiece(text, vocabulary):
    """Find minimum-token segmentation with dynamic programming."""
    vocabulary = set(vocabulary)
    if not text:
        return []

    max_token_length = max(map(len, vocabulary))
    n = len(text)

    best = [float("inf")] * (n + 1)
    next_token = [None] * (n + 1)
    best[n] = 0

    for i in range(n - 1, -1, -1):
        for size in range(
            min(max_token_length, n - i), 0, -1
        ):
            tok = text[i:i + size]

            if tok in vocabulary and 1 + best[i + size] < best[i]:
                best[i] = 1 + best[i + size]
                next_token[i] = tok

    if best[0] == float("inf"):
        raise ValueError("Text cannot be segmented")

    result = []
    i = 0

    while i < n:
        token = next_token[i]
        result.append(token)
        i += len(token)

    return result


def main():
    # Part 1: Reproduce the paper's example
    greedy = maxmatch(PAPER_TEXT, PAPER_VOCAB)
    optimal = pathpiece(PAPER_TEXT, PAPER_VOCAB)

    assert greedy == ["abcd", "e", "f", "g"]
    assert optimal == ["abc", "defg"]

    print("PAPER EXAMPLE")
    print("Input:", PAPER_TEXT)
    print("MaxMatch:", " | ".join(greedy), f"({len(greedy)} tokens)")
    print("PathPiece:", " | ".join(optimal), f"({len(optimal)} tokens)")

    # Part 2: New synthetic experiment
    rows = []
    example_failures = []

    for length in range(1, MAX_LENGTH + 1):
        num_strings = 0
        failures = 0
        greedy_total = 0
        optimal_total = 0
        extra_total = 0

        for chars in product("ab", repeat=length):
            text = "".join(chars)

            g = maxmatch(text, BENCHMARK_VOCAB)
            p = pathpiece(text, BENCHMARK_VOCAB)

            assert "".join(g) == "".join(p) == text
            assert len(p) <= len(g)

            num_strings += 1
            greedy_total += len(g)
            optimal_total += len(p)
            extra_total += len(g) - len(p)

            if len(g) > len(p):
                failures += 1
                if len(example_failures) < 5:
                    example_failures.append((text, g, p))

        rows.append({
            "length": length,
            "number_of_strings": num_strings,
            "greedy_suboptimal_count": failures,
            "greedy_suboptimal_percent": 100 * failures / num_strings,
            "mean_maxmatch_tokens": greedy_total / num_strings,
            "mean_pathpiece_tokens": optimal_total / num_strings,
            "mean_extra_tokens": extra_total / num_strings,
        })

    # Save numerical results
    with open("tokenization_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("\nNEW SYNTHETIC EXPERIMENT")
    print("Vocabulary:", ", ".join(sorted(BENCHMARK_VOCAB)))

    for r in rows:
        print(
            f"Length {r['length']:2d}: "
            f"{r['greedy_suboptimal_count']:4d} / "
            f"{r['number_of_strings']:4d} suboptimal "
            f"({r['greedy_suboptimal_percent']:.2f}%)"
        )

    print("\nFirst five counterexamples:")
    for text, g, p in example_failures:
        print(
            f"{text}: MaxMatch={'|'.join(g)}, "
            f"PathPiece={'|'.join(p)}"
        )

    all_strings = sum(r["number_of_strings"] for r in rows)
    all_failures = sum(r["greedy_suboptimal_count"] for r in rows)

    print(
        f"\nOverall: {all_failures}/{all_strings} "
        f"({100 * all_failures / all_strings:.2f}%) "
        "greedy segmentations are suboptimal."
    )

    # Part 3: Generate graph
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 4.6))

    ax.plot(
        [r["length"] for r in rows],
        [r["greedy_suboptimal_percent"] for r in rows],
        marker="o",
        linewidth=2,
    )

    ax.set(
        xlabel="String length (characters)",
        ylabel="Strings where MaxMatch uses more tokens (%)",
        title="Greedy vs. shortest-path tokenization",
    )

    ax.set_xticks(range(1, MAX_LENGTH + 1))
    ax.set_ylim(bottom=0)
    ax.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig("tokenization_comparison.png", dpi=180)
    plt.close(fig)

    print(
        "\nSaved: tokenization_results.csv, "
        "tokenization_comparison.png"
    )


if __name__ == "__main__":
    main()
