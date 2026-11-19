---
title: "Reproducing Spurious Forgetting: Shared Keys Hide Old Facts"
description: "A ten-seed reproduction of Figure 2"
paper: spurious-forgetting
role: coding
task: reimplement
by: [NathanAdda]
---

## What I reimplemented

I reproduced **Figure 2, panel 1** from [*When Forgetting is Not Catastrophic: On the Mechanics of Spurious Forgetting*](https://arxiv.org/abs/2610.08718).

The experiment studies how sharing structure between fact keys changes forgetting:

$$
k_i = \sqrt{\alpha}\,\mu + \sqrt{1-\alpha}\,e_i,
$$

where $\mu$ is shared by all facts and $e_i$ belongs only to fact $i$. A larger $\alpha$ means that different facts look more alike to the model.

I used the paper's setup: dimension 128, 32 output tokens, and 128 facts in each set. The model first learned old facts $A$ and $B$, then trained for 500 steps only on new facts $B'$. I measured accuracy on $A$ throughout, without replay, and averaged ten seeds.

## The code

The implementation is a small NumPy version of the paper's associative memory. This is the core of the experiment:

```python
# Build keys with a shared part and a fact-specific part.
keys = np.sqrt(alpha) * mu + np.sqrt(1 - alpha) * own_vectors

# Two linear layers with RMS normalization between them.
h = keys @ w1.T
x = np.sqrt(d) * h / np.linalg.norm(h, axis=1, keepdims=True)
probs = softmax(x @ w2.T)
```

I used a pretraining learning rate of 0.1. A one-seed pilot gave a fine-tuning rate of 0.02, which made the new facts reach 0.99 accuracy around step 200 as described in the paper.

- [Full reproduction script]({{ '/assets/code/spurious-forgetting-figure2-panel1/reproduce.py' | relative_url }})
- [Requirements]({{ '/assets/code/spurious-forgetting-figure2-panel1/requirements.txt' | relative_url }})
- [Per-seed curves]({{ '/assets/data/spurious-forgetting-figure2-panel1/raw_curves.csv' | relative_url }})
- [Mean and standard-deviation curves]({{ '/assets/data/spurious-forgetting-figure2-panel1/summary_curves.csv' | relative_url }})
- [Run metadata]({{ '/assets/data/spurious-forgetting-figure2-panel1/metadata.json' | relative_url }})

To rerun it:

```bash
cd assets/code/spurious-forgetting-figure2-panel1
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python reproduce.py \
  --seeds 0-9 \
  --out-dir ../../data/spurious-forgetting-figure2-panel1
cp ../../data/spurious-forgetting-figure2-panel1/figure2_panel1.svg \
  ../../img/posts/coding-nathan/figure2-panel1.svg
```

## Results

<img src="{{ '/assets/img/posts/coding-nathan/figure2-panel1.svg' | relative_url }}" alt="Old-fact accuracy over 500 fine-tuning steps for alpha 0, 0.1, 0.25, and 0.5. Alpha 0 forgets gradually, while alpha 0.5 collapses sharply, recovers, and then erodes." loading="lazy" style="display: block; width: 100%; max-width: 760px; height: auto; margin: 1rem auto;">

| $\alpha$ | Mean accuracy at step 0 | Trough (step, accuracy) | Step 200 | Step 500 |
|---:|---:|---:|---:|---:|
| 0 | 0.995 | (498, 0.565) | 0.806 | 0.565 |
| 0.1 | 0.996 | (500, 0.266) | 0.449 | 0.266 |
| 0.25 | 0.997 | (497, 0.261) | 0.319 | 0.261 |
| 0.5 | 0.996 | **(74, 0.118)** | 0.390 | 0.334 |

At $\alpha=0$, forgetting is gradual. At $\alpha=0.5$, accuracy quickly falls from 0.996 to 0.118, recovers to about 0.40, and then slowly declines again.

The shared part of the keys makes updates to $B'$ move many old representations in the same direction. This temporarily hides the old answers. As the model learns the individual new facts, RMS normalization helps undo part of that shared movement, so some old accuracy returns. The later decline comes from smaller fact-specific changes that are not undone.

## Comparison with the paper

The main pattern matches the paper: stronger sharing gives a faster collapse, while $\alpha=0$ gives ordinary gradual forgetting. The $\alpha=0.5$ curve also shows the expected recovery and later erosion.

The numbers are not an exact match. My recovery peaks around 0.40, and the intermediate curves end somewhat lower. The paper does not report all initialization and learning-rate details for this toy experiment, which could explain the difference.

I could inspect the [official repository](https://github.com/vedantpalit/spurious-forgetting-mechanics), but this environment could not clone or download its `toy/` files. The code here therefore follows the published equations rather than running the authors' JAX implementation.

## What I learned

The main takeaway for me is that low accuracy does not always mean the information was erased. With shared keys, the model can temporarily lose access to many facts at once and later recover them without seeing them again.

It was also useful to plot the full training trajectory. If I had measured only near step 74, I would have concluded that almost everything was forgotten. The recovery shows why that conclusion would be too strong.
