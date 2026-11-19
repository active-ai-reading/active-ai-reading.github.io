#!/usr/bin/env python3
"""Reproduce Palit et al. (2026), Figure 2 panel 1.

The model and gradients follow Equations (1), (2), (11), (14), and (15).
Only NumPy is required for training; the final SVG is written directly.
"""

import argparse
import csv
import json
import math
import os
import time

import numpy as np


ALPHAS = (0.0, 0.1, 0.25, 0.5)


def unit_rows(x):
    return x / np.linalg.norm(x, axis=1, keepdims=True)


def make_data(seed, alpha, d=128, n=128, vocab=32):
    rng = np.random.default_rng(seed)
    mu = rng.normal(size=d)
    mu /= np.linalg.norm(mu)
    own = unit_rows(rng.normal(size=(3 * n, d)))
    keys = math.sqrt(alpha) * mu + math.sqrt(1.0 - alpha) * own
    # A uses the first vocabulary half; B and B' use the second half.
    y_a = rng.integers(0, vocab // 2, size=n)
    y_b = rng.integers(vocab // 2, vocab, size=n)
    y_bp = rng.integers(vocab // 2, vocab, size=n)
    return rng, keys[:n], y_a, keys[n:2*n], y_b, keys[2*n:], y_bp


def forward(w1, w2, keys):
    h = keys @ w1.T
    norms = np.linalg.norm(h, axis=1, keepdims=True)
    x = math.sqrt(h.shape[1]) * h / np.maximum(norms, 1e-12)
    logits = x @ w2.T
    logits -= logits.max(axis=1, keepdims=True)
    probs = np.exp(logits)
    probs /= probs.sum(axis=1, keepdims=True)
    return probs, h, x, norms


def accuracy(w1, w2, keys, labels):
    return float(np.mean(np.argmax(forward(w1, w2, keys)[0], axis=1) == labels))


def sgd_step(w1, w2, keys, labels, lr):
    probs, h, x, norms = forward(w1, w2, keys)
    dz = probs.copy()
    dz[np.arange(len(labels)), labels] -= 1.0
    dz /= len(labels)
    # Save W2 for backprop because both matrices are updated simultaneously.
    dx = dz @ w2
    hhat = h / np.maximum(norms, 1e-12)
    dh = math.sqrt(h.shape[1]) / np.maximum(norms, 1e-12) * (
        dx - hhat * np.sum(dx * hhat, axis=1, keepdims=True)
    )
    grad_w2 = dz.T @ x
    grad_w1 = dh.T @ keys
    w1 -= lr * grad_w1
    w2 -= lr * grad_w2


def train_one(seed, alpha, args):
    rng, k_a, y_a, k_b, y_b, k_bp, y_bp = make_data(
        seed, alpha, args.dimension, args.facts, args.vocab
    )
    scale = 1.0 / math.sqrt(args.dimension)
    w1 = rng.normal(scale=scale, size=(args.dimension, args.dimension))
    w2 = rng.normal(scale=scale, size=(args.vocab, args.dimension))
    old_k = np.concatenate((k_a, k_b))
    old_y = np.concatenate((y_a, y_b))

    pre_steps = 0
    while pre_steps < args.max_pretrain_steps:
        idx = rng.choice(len(old_y), size=args.batch_size, replace=False)
        sgd_step(w1, w2, old_k[idx], old_y[idx], args.pretrain_lr)
        pre_steps += 1
        if pre_steps % args.pretrain_eval_every == 0:
            if (accuracy(w1, w2, k_a, y_a) >= 0.99 and
                    accuracy(w1, w2, k_b, y_b) >= 0.99):
                break
    pre_a = accuracy(w1, w2, k_a, y_a)
    pre_b = accuracy(w1, w2, k_b, y_b)
    if min(pre_a, pre_b) < 0.99:
        raise RuntimeError(
            f"pretraining failed: alpha={alpha}, seed={seed}, "
            f"A={pre_a:.3f}, B={pre_b:.3f}"
        )

    rows = []
    for step in range(args.finetune_steps + 1):
        if step % args.eval_every == 0:
            rows.append({
                "seed": seed, "alpha": alpha, "step": step,
                "accuracy_A": accuracy(w1, w2, k_a, y_a),
                "accuracy_Bprime": accuracy(w1, w2, k_bp, y_bp),
                "pretrain_steps": pre_steps,
                "pretrain_accuracy_A": pre_a,
                "pretrain_accuracy_B": pre_b,
            })
        if step < args.finetune_steps:
            idx = rng.choice(args.facts, size=args.batch_size, replace=False)
            sgd_step(w1, w2, k_bp[idx], y_bp[idx], args.finetune_lr)
    return rows


def aggregate(rows):
    groups = {}
    for row in rows:
        groups.setdefault((row["alpha"], row["step"]), []).append(row["accuracy_A"])
    out = []
    for (alpha, step), values in sorted(groups.items()):
        a = np.asarray(values)
        out.append({
            "alpha": alpha, "step": step, "mean_accuracy_A": float(a.mean()),
            "std_accuracy_A": float(a.std(ddof=1)) if len(a) > 1 else 0.0,
            "n_seeds": len(a),
        })
    return out


def svg_plot(summary, path):
    width, height = 760, 500
    left, right, top, bottom = 82, 25, 35, 70
    pw, ph = width-left-right, height-top-bottom
    max_step = max(r["step"] for r in summary)
    colors = {0.0: "#4c78a8", 0.1: "#f58518", 0.25: "#54a24b", 0.5: "#e45756"}
    def xp(x): return left + pw * x / max_step
    def yp(y): return top + ph * (1-y)
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:Arial,sans-serif;fill:#222}.tick{font-size:13px}.label{font-size:17px}.title{font-size:18px;font-weight:600}</style>',
        f'<text x="{width/2}" y="23" text-anchor="middle" class="title">Shared-key strength and old-fact recall</text>',
    ]
    for y in np.linspace(0, 1, 6):
        yy = yp(float(y))
        lines += [f'<line x1="{left}" y1="{yy:.1f}" x2="{width-right}" y2="{yy:.1f}" stroke="#ddd"/>',
                  f'<text x="{left-12}" y="{yy+5:.1f}" text-anchor="end" class="tick">{y:.1f}</text>']
    for x in range(0, max_step+1, 100):
        xx = xp(x)
        lines += [f'<line x1="{xx:.1f}" y1="{top}" x2="{xx:.1f}" y2="{height-bottom}" stroke="#eee"/>',
                  f'<text x="{xx:.1f}" y="{height-bottom+24}" text-anchor="middle" class="tick">{x}</text>']
    lines += [f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#222"/>',
              f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#222"/>',
              f'<text x="{left+pw/2}" y="{height-20}" text-anchor="middle" class="label">fine-tuning step</text>',
              f'<text x="22" y="{top+ph/2}" text-anchor="middle" class="label" transform="rotate(-90 22 {top+ph/2})">old facts accuracy (A)</text>']
    for alpha in ALPHAS:
        vals = [r for r in summary if r["alpha"] == alpha]
        pts = " ".join(f'{xp(r["step"]):.2f},{yp(r["mean_accuracy_A"]):.2f}' for r in vals)
        lines.append(f'<polyline points="{pts}" fill="none" stroke="{colors[alpha]}" stroke-width="3"/>')
    lx, ly = left+18, top+22
    for i, alpha in enumerate(ALPHAS):
        x = lx + i*150
        lines += [f'<line x1="{x}" y1="{ly}" x2="{x+28}" y2="{ly}" stroke="{colors[alpha]}" stroke-width="3"/>',
                  f'<text x="{x+36}" y="{ly+5}" class="tick">alpha = {alpha:g}</text>']
    lines.append('</svg>')
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seeds", default="0", help="e.g. 0 or 0-9 or 0,2,4")
    p.add_argument("--out-dir", default="results")
    p.add_argument("--dimension", type=int, default=128)
    p.add_argument("--vocab", type=int, default=32)
    p.add_argument("--facts", type=int, default=128)
    p.add_argument("--batch-size", type=int, default=32)
    p.add_argument("--pretrain-lr", type=float, default=0.1)
    # Calibrated in the one-seed pilot so B' reaches >=0.99 near step 200,
    # following Appendix B.1 (seed-0 crossings: steps 177--192).
    p.add_argument("--finetune-lr", type=float, default=0.02)
    p.add_argument("--max-pretrain-steps", type=int, default=20000)
    p.add_argument("--pretrain-eval-every", type=int, default=20)
    p.add_argument("--finetune-steps", type=int, default=500)
    p.add_argument("--eval-every", type=int, default=1)
    args = p.parse_args()
    if "-" in args.seeds:
        lo, hi = map(int, args.seeds.split("-"))
        seeds = list(range(lo, hi+1))
    else:
        seeds = [int(x) for x in args.seeds.split(",")]
    os.makedirs(args.out_dir, exist_ok=True)
    started = time.time()
    rows = []
    for seed in seeds:
        for alpha in ALPHAS:
            print(f"seed={seed} alpha={alpha:g}", flush=True)
            rows.extend(train_one(seed, alpha, args))
    summary = aggregate(rows)
    raw_csv = os.path.join(args.out_dir, "raw_curves.csv")
    with open(raw_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    sum_csv = os.path.join(args.out_dir, "summary_curves.csv")
    with open(sum_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=summary[0].keys()); w.writeheader(); w.writerows(summary)
    svg_plot(summary, os.path.join(args.out_dir, "figure2_panel1.svg"))
    metadata = vars(args).copy()
    metadata.update({"seeds_resolved": seeds, "alphas": ALPHAS,
                     "runtime_seconds": time.time()-started,
                     "numpy_version": np.__version__})
    with open(os.path.join(args.out_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"wrote {args.out_dir}; runtime={metadata['runtime_seconds']:.1f}s")


if __name__ == "__main__":
    main()
