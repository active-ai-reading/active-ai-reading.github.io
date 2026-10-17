---
title: "Reimplementing CLeq: what does 12.6% actually mean?"
description: I simulated the paper's measurement with a known amount of transfer. The metric is right at 0% and 100%, and generous in between.
paper: cross-lingual-knowledge-pretraining
role: coding
task: reimplement
by: [course-team]
example: true
---

## What I reimplemented

The paper's metric, CLeq, is estimated from one regression over all 2,048 fictive facts:

$$
\mathrm{acc}_A(f) = \alpha + \beta_A\, N_A(f) + \beta_B\, N_B(f) + \varepsilon,
\qquad
\mathrm{CLeq}[B \to A] = 100 \times \frac{\beta_B}{\beta_A}
$$

where $N_A(f)$ and $N_B(f)$ are how many times fact $f$ was seen in each language. Pretraining models is out of reach for a homework, but the *measurement* can be tested: generate accuracies where I **know** the true transfer, run the paper's estimator, and see what comes out.

**The setup mirrors the paper:** 16 groups of 128 facts, each group at one combination of $\{0, 20, 100, 1000\}$ exposures per language; 4-option multiple-choice questions (25% chance); a log-like learning curve, as the paper reports. "True transfer" $t$ means one foreign exposure is worth $t$ native ones, so a fact's accuracy is the learning curve evaluated at $N_A + t \cdot N_B$.

## The code

```python
LEVELS = [0, 20, 100, 1000]          # exposure counts used in the paper
K = 60.0                             # how quickly learning saturates (smaller = faster)
FACTS_PER_GROUP = 128                # 16 groups x 128 facts = 2,048 facts
CHANCE, CEIL = 0.25, 0.9             # 4-way multiple choice; best reachable accuracy
QUESTIONS_PER_FACT = 4               # held-out MCQs per fact

def learning_curve(effective_exposures, k=K):
    """Log-like acquisition: fast at first, then saturating."""
    return CHANCE + (CEIL - CHANCE) * np.log1p(effective_exposures / k) / np.log1p(1000 / k)

def simulate(transfer, rng):
    nA, nB = np.meshgrid(LEVELS, LEVELS, indexing="ij")
    nA = np.repeat(nA.ravel(), FACTS_PER_GROUP)
    nB = np.repeat(nB.ravel(), FACTS_PER_GROUP)
    p = np.clip(learning_curve(nA + transfer * nB), 0, 1)
    acc = rng.binomial(QUESTIONS_PER_FACT, p) / QUESTIONS_PER_FACT
    return nA, nB, acc

def cleq(nA, nB, acc):
    X = np.column_stack([np.ones_like(nA), nA, nB]).astype(float)
    alpha, beta_A, beta_B = np.linalg.lstsq(X, acc, rcond=None)[0]
    return 100 * beta_B / beta_A
```

Full script (runs in a second, needs only numpy): [cleq_sim.py]({{ '/assets/code/cleq_sim.py' | relative_url }})

## Results

200 simulated "pretraining runs" per row:

| True transfer | CLeq (mean) | CLeq (std across runs) |
| --- | --- | --- |
| 0% | 0.3% | 1.8% |
| 5% | 14.0% | 2.1% |
| 12.5% | 28.7% | 2.2% |
| 25% | 45.8% | 2.7% |
| 50% | 69.6% | 2.3% |
| 100% | 100.1% | 2.5% |

And how much it depends on the curve's shape, for true transfer of 5% / 12.5%:

| Saturation K | CLeq at 5% | CLeq at 12.5% |
| --- | --- | --- |
| 10 (saturates fast) | 22.8% | 38.0% |
| 60 | 14.0% | 28.7% |
| 300 (nearly linear) | 8.0% | 19.2% |

## What this means

1. **The endpoints are trustworthy.** No transfer gives ≈0%, perfect transfer ≈100%. The paper's central contrast, near-zero for disjoint tokens vs. clearly positive for shared ones, holds under this check.
2. **In between, linear CLeq is generous** when learning saturates. A fact seen 1000 times natively is near its ceiling, so native exposures look less valuable per unit, and the ratio favors the foreign slope. Under this model, a measured 12.6% would correspond to a true exposure-equivalence of roughly 2–8%, depending on the curve. So "12.6% of native learning efficiency" is best read as a **ranking** score, not a literal exchange rate.
3. **One run has about ±2 points of noise.** Differences like 0.9% vs 2.2% vs 2.5% (baseline vs code-switching vs alignment) are within a single standard deviation here.

## Caveats

This depends on my modeling choice: that transfer acts like "extra effective exposures" fed into one shared learning curve. Other models of transfer would give a different correction. The paper says it tried a curve-aware estimator and found the linear one more informative. Comparing the two on simulations like these would be a nice follow-up (see [five follow-ups]({{ '/posts/2026/follow-ups-worth-doing/' | relative_url }})).

## What I learned

Before trusting a metric, simulate it with a known answer. It takes an hour and tells you which differences you're allowed to read into.

Method from {% cite gaber2026crosslingual %}.
