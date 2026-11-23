"""Minimal associative memory from Palit et al., "When Forgetting Is Not Catastrophic" (2026), §3.1 and App. B.1.

A NumPy re-implementation used for the "One shared lift, two consequences" visualization.
It reproduces the size of the common shift s(t) of the old facts' hidden states during fine-tuning
(the purple curve), together with recall of the old facts A and of the new facts B'.

Model:  k_i = sqrt(alpha) mu + sqrt(1 - alpha) e_i      keys share the unit vector mu
        h = k W,   x = RMS(h) = sqrt(d) h / ||h||,   z = x U,   p = softmax(z)
Data:   d = 128, 32 answer tokens split 16 / 16, 128 facts in each of A (first half),
        B (second half) and the new facts B' (second half), alpha = 0.5.
Train:  minibatch SGD (batch 32) on A and B until both are recalled with accuracy >= 0.99,
        then on B' alone, at a learning rate that brings B' to 0.99 around step 200.

Usage:  python minimal_model.py            # with RMS normalization (the paper's model)
        python minimal_model.py --no-norm  # same run without normalization: the shift never retracts
Prints JSON: {"step": 4, "s": [...], "acc_A": [...], "acc_new": [...]} sampled every 4 steps.
"""
import argparse
import json

import numpy as np

D, V, N = 128, 32, 128
HALF_A = np.arange(0, V // 2)
HALF_B = np.arange(V // 2, V)


def build_data(seed, alpha):
    r = np.random.default_rng(1000 + seed)
    mu = r.normal(size=D)
    mu /= np.linalg.norm(mu)

    def keys(n):
        e = r.normal(size=(n, D))
        e /= np.linalg.norm(e, axis=1, keepdims=True)
        return np.sqrt(alpha) * mu[None] + np.sqrt(1 - alpha) * e

    A = (keys(N), HALF_A[r.integers(0, len(HALF_A), N)])
    B = (keys(N), HALF_B[r.integers(0, len(HALF_B), N)])
    new = (keys(N), HALF_B[r.integers(0, len(HALF_B), N)])
    return A, B, new


def forward(p, k, norm):
    h = k @ p["W"]
    x = h / np.linalg.norm(h, axis=-1, keepdims=True) * np.sqrt(D) if norm else h
    return x @ p["U"], h, x


def softmax(z):
    z = z - z.max(-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(-1, keepdims=True)


def sgd_step(p, k, v, lr, norm):
    z, h, x = forward(p, k, norm)
    dz = softmax(z)
    dz[np.arange(len(v)), v] -= 1
    dz /= len(v)
    dU = x.T @ dz
    dx = dz @ p["U"].T
    if norm:  # backprop through x = sqrt(d) h / ||h||
        r = np.linalg.norm(h, axis=-1, keepdims=True)
        hh = h / r
        dh = np.sqrt(D) / r * (dx - (dx * hh).sum(-1, keepdims=True) * hh)
    else:
        dh = dx
    return {"W": p["W"] - lr * (k.T @ dh), "U": p["U"] - lr * dU}


def accuracy(p, k, v, norm):
    return float((forward(p, k, norm)[0].argmax(-1) == v).mean())


def init_params(seed):
    r = np.random.default_rng(seed + 77)
    return {"W": r.normal(size=(D, D)) / np.sqrt(D), "U": r.normal(size=(D, V)) / np.sqrt(D)}


def pretrain(seed, norm, A, B, cap=20000):
    k = np.concatenate([A[0], B[0]])
    v = np.concatenate([A[1], B[1]])
    for lr in [0.5, 0.3, 0.2, 0.1, 0.05]:
        rng = np.random.default_rng(seed)
        p = init_params(seed)
        for t in range(cap):
            i = rng.integers(0, len(k), 32)
            p = sgd_step(p, k[i], v[i], lr, norm)
            if t % 100 == 0 and min(accuracy(p, *A, norm), accuracy(p, *B, norm)) >= 0.99:
                return p, lr
    raise SystemExit("pretraining did not reach 0.99")


def steps_to_learn(p, new, lr, norm, seed, cap=600):
    rng = np.random.default_rng(seed + 5)
    for t in range(cap):
        if t % 5 == 0 and accuracy(p, *new, norm) >= 0.99:
            return t
        i = rng.integers(0, N, 32)
        p = sgd_step(p, new[0][i], new[1][i], lr, norm)
    return cap + 1


def matched_lr(p0, new, base, norm, seed, target=200):
    """Bisect the fine-tuning rate so that the new facts reach 0.99 around step `target`."""
    lo, hi = base / 8, base * 8
    for _ in range(14):
        mid = np.sqrt(lo * hi)
        if steps_to_learn(p0, new, mid, norm, seed) > target:
            lo = mid
        else:
            hi = mid
    return np.sqrt(lo * hi)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--alpha", type=float, default=0.5)
    ap.add_argument("--steps", type=int, default=800)
    ap.add_argument("--every", type=int, default=4)
    ap.add_argument("--no-norm", action="store_true", help="remove the RMS normalization")
    a = ap.parse_args()
    norm = not a.no_norm

    A, B, new = build_data(a.seed, a.alpha)
    p, lr = pretrain(a.seed, norm, A, B)
    lr_ft = matched_lr(p, new, lr / 13.33, norm, a.seed)
    mean0 = forward(p, A[0], norm)[1].mean(0)        # old facts' mean hidden state before fine-tuning

    out = {"step": a.every, "s": [], "acc_A": [], "acc_new": []}
    rng = np.random.default_rng(a.seed + 5)
    for t in range(a.steps + 1):
        if t % a.every == 0:
            shift = forward(p, A[0], norm)[1].mean(0) - mean0   # common shift of the old facts
            out["s"].append(round(float(np.linalg.norm(shift)), 4))
            out["acc_A"].append(round(accuracy(p, *A, norm), 4))
            out["acc_new"].append(round(accuracy(p, *new, norm), 4))
        i = rng.integers(0, N, 32)
        p = sgd_step(p, new[0][i], new[1][i], lr_ft, norm)   # fine-tune on the new facts only
    print(json.dumps(out))


if __name__ == "__main__":
    main()
