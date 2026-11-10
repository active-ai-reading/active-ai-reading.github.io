"""Runs E1-E4 of the BPE reimplementation. Usage: python run_experiments.py [N_MERGES_FOR_SURVEY_TRAINER]
Needs pride.txt and frankenstein.txt (Project Gutenberg ebooks 1342 and 84, plain text) in the current folder."""
import json, random, re, sys, time
from collections import Counter
import survey_bpe as S
import fast_bpe as F

def body(path):
    t = open(path, encoding="utf-8").read().replace("\r", "")
    a = t.index("*** START"); a = t.index("\n", a)
    b = t.index("*** END")
    return " ".join(t[a:b].split())

train_text = body("pride.txt")      # Pride and Prejudice
test_text = body("frankenstein.txt")  # Frankenstein, never seen in training
print("train chars", len(train_text), "pretokens", len(F.pretokens(train_text)), "unique", len(set(F.pretokens(train_text))))
print("test chars", len(test_text), "pretokens", len(F.pretokens(test_text)), "unique", len(set(F.pretokens(test_text))))
R = {}

# ---- E1: survey Code 3.1 vs independent trainer: identical merges? -----------------------------------
N_PAPER = int(sys.argv[1]) if len(sys.argv) > 1 else 300
sents = [train_text]  # one "sentence": Code 3.1 pretokenizes it itself
# alphabet size first, so that target size = alphabet + N_PAPER merges
alpha = len({c for w in F.pretokens(train_text) for c in w})
t0 = time.time()
vocab_s, merges_s = S.bpe_training(sents, alpha + N_PAPER)
t_paper = time.time() - t0
t0 = time.time()
vocab_f, merges_f = F.train(train_text, alpha + N_PAPER)
t_fast = time.time() - t0
same = merges_s == merges_f
print(f"E1 alphabet={alpha}  merges: survey={len(merges_s)} fast={len(merges_f)}  identical={same}  "
      f"time survey={t_paper:.1f}s fast={t_fast:.2f}s")
first_diff = next((i for i, (a, b) in enumerate(zip(merges_s, merges_f)) if a != b), None)
R["E1"] = dict(alphabet=alpha, n_merges=N_PAPER, identical=same, first_diff=first_diff,
               seconds_survey=t_paper, seconds_fast=t_fast, first_merges=[a + b for a, b in merges_s[:25]])
print("first merges:", [a + b for a, b in merges_s[:25]])

# ---- E2: Code 3.2 vs Code 3.3 vs independent encoder on held-out text and random strings ---------------
def fast_encode(word, ranks):
    seq = tuple(word)
    while len(seq) > 1:
        c = [(ranks[p], p) for p in zip(seq, seq[1:]) if p in ranks]
        if not c: break
        seq = F.merge_word(seq, *min(c)[1])
    return list(seq)

ranks_s = {p: i for i, p in enumerate(merges_s)}
words = sorted(set(F.pretokens(test_text)))
mism_32_33 = mism_fast = 0
for w in words:
    a = S.bpe_inference(w, merges_s); b = S.bpe_inference_priority(w, merges_s); c = fast_encode(w, ranks_s)
    mism_32_33 += a != b; mism_fast += a != c
rng = random.Random(0)
chars = sorted({c for w in F.pretokens(train_text) for c in w})
rand_words = ["".join(rng.choice("abcdeh ") for _ in range(rng.randint(1, 30))) for _ in range(5000)]
mism_rand = 0
for w in rand_words:
    if not w.strip(): continue
    mism_rand += S.bpe_inference(w, merges_s) != S.bpe_inference_priority(w, merges_s)
print(f"E2 held-out unique words={len(words)}  Code3.2!=Code3.3: {mism_32_33}  Code3.2!=independent: {mism_fast}  "
      f"random strings (5000) Code3.2!=3.3: {mism_rand}")
R["E2"] = dict(words=len(words), mism_32_33=mism_32_33, mism_independent=mism_fast, random=len(rand_words), mism_random=mism_rand)

# ---- E3: time of Code 3.2 vs 3.3 as the merge list grows ----------------------------------------------------
M_MAX = 4000
alpha_f = alpha
_, merges_big = F.train(train_text, alpha_f + M_MAX)
print("trained", len(merges_big), "merges with the fast trainer")
sample = " ".join(F.pretokens(test_text)[:3000])
rows = []
for m in [100, 250, 500, 1000, 2000, 4000]:
    mm = merges_big[:m]
    t0 = time.time(); a = S.bpe_inference(sample, mm); ti = time.time() - t0
    t0 = time.time(); b = S.bpe_inference_priority(sample, mm); tp = time.time() - t0
    assert a == b
    rows.append(dict(merges=m, iterative_s=ti, priority_s=tp, ratio=ti / tp, tokens=len(a)))
    print(f"E3 merges={m:5d}  Code3.2={ti:7.3f}s  Code3.3={tp:7.3f}s  ratio={ti/tp:6.1f}x  tokens={len(a)}")
R["E3"] = rows

# ---- E4: does BPE find "linguistically meaningful units"? (survey intuition) + compression ------------------
test_words = F.pretokens(test_text)
tot_chars = sum(len(w) for w in test_words)
curve = []
for m in [0, 50, 100, 250, 500, 1000, 2000, 4000]:
    ranks = {p: i for i, p in enumerate(merges_big[:m])}
    cache = {}
    n = 0
    for w in test_words:
        if w not in cache: cache[w] = len(fast_encode(w, ranks))
        n += cache[w]
    curve.append(dict(merges=m, tokens=n, chars_per_token=tot_chars / n, tokens_per_word=n / len(test_words)))
    print(f"E4 merges={m:5d}  tokens={n:7d}  chars/token={tot_chars/n:.2f}  tokens/word={n/len(test_words):.2f}")
R["E4"] = curve
suffixes = ["ing", "ed", "ly", "er", "tion", "ness", "ment", "ous", "ing,", "'s"]
found = {}
for s in suffixes:
    for i, (a, b) in enumerate(merges_big):
        if a + b == s:
            found[s] = i + 1; break
print("E4 merge number at which common suffix/affix tokens appear:", found)
R["E4_suffix_merge_rank"] = found
sp = [i + 1 for i, (a, b) in enumerate(merges_big) if (a + b).startswith(" ") and len(a + b) > 1]
whole = [(a + b) for (a, b) in merges_big[:300] if (a + b).startswith(" ") and len(a + b) >= 4]
print("E4 first 25 merges that form a word with leading space:", whole[:25])
R["E4_whole_words_first"] = whole[:25]

# who-is-first in an example sentence
ex = "The unbelievably unfriendly creatures were running quickly."
for m in [100, 500, 2000, 4000]:
    print(f"E4 example @{m} merges:", S.bpe_inference_priority(ex, merges_big[:m]))
R["E4_example"] = {m: S.bpe_inference_priority(ex, merges_big[:m]) for m in [100, 500, 2000, 4000]}
json.dump(R, open("results.json", "w"), indent=1, ensure_ascii=False)
