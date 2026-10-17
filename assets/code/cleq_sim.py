"""Simulate the CLeq estimator of Gaber et al. (2026), arXiv:2609.19291.

We generate fictive-fact accuracies with a KNOWN cross-lingual transfer value,
estimate CLeq exactly as the paper does (ratio of OLS slopes), and compare.
Run: python cleq_sim.py   (needs numpy)
"""
import numpy as np

LEVELS = [0, 20, 100, 1000]          # exposure counts used in the paper
K = 60.0                             # how quickly learning saturates (smaller = faster)
FACTS_PER_GROUP = 128                # 16 groups x 128 facts = 2,048 facts
CHANCE, CEIL = 0.25, 0.9             # 4-way multiple choice; best reachable accuracy
QUESTIONS_PER_FACT = 4               # held-out MCQs per fact

def learning_curve(effective_exposures, k=K):
    """Log-like acquisition: fast at first, then saturating."""
    return CHANCE + (CEIL - CHANCE) * np.log1p(effective_exposures / k) / np.log1p(1000 / k)

def simulate(transfer, rng):
    """transfer = true value of one foreign exposure relative to a native one."""
    nA, nB = np.meshgrid(LEVELS, LEVELS, indexing="ij")
    nA = np.repeat(nA.ravel(), FACTS_PER_GROUP)
    nB = np.repeat(nB.ravel(), FACTS_PER_GROUP)
    p = np.clip(learning_curve(nA + transfer * nB), 0, 1)
    acc = rng.binomial(QUESTIONS_PER_FACT, p) / QUESTIONS_PER_FACT
    return nA, nB, acc

def cleq(nA, nB, acc):
    """CLeq(B->A) = 100 * beta_B / beta_A from acc = a + beta_A*nA + beta_B*nB."""
    X = np.column_stack([np.ones_like(nA), nA, nB]).astype(float)
    alpha, beta_A, beta_B = np.linalg.lstsq(X, acc, rcond=None)[0]
    return 100 * beta_B / beta_A

rng = np.random.default_rng(0)
print(f"{'true transfer':>14} | {'CLeq mean':>9} | {'CLeq std':>8}")
for t in [0.0, 0.05, 0.125, 0.25, 0.5, 1.0]:
    est = [cleq(*simulate(t, rng)) for _ in range(200)]
    print(f"{100*t:13.1f}% | {np.mean(est):8.1f}% | {np.std(est):7.1f}%")
