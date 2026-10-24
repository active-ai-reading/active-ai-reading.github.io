---
title: "A better Figure 2"
description: Figure 2 uses two ternary plots to select a model architecture, but the key tradeoff between memory and computation is hidden across separate panels
paper: matryoshka-lm-suites
role: visualization
task: redo-graph
by: [MatanBarTov]
chart:
  chartjs: true # enables ```chartjs code blocks. Also available: echarts, plotly, vega_lite (see the showcase)
---

## The original

{% include figure.liquid path="assets/img/papers/matryoshka-language-model-suites/figure2.png" class="img-fluid rounded z-depth-1" caption="Figure 2 of Matryoshka Language Model Suites: KV-cache memory and theoretical inference FLOPs for different layer allocations." %}

Figure 2 explores how to distribute **39 Transformer layers** among three nested model blocks (500M, 1.5B, and 3B parameters). Each point represents a possible layer allocation $(n_1,n_2,n_3)$, where $n_1+n_2+n_3=39$.

The authors use two ternary plots: one showing **KV-cache memory per token**, and another showing **theoretical inference FLOPs per token**. Their goal is to choose an architecture with approximately the same memory and computational requirements as a conventional 3B model: **266 KB/token and 5.54 GFLOPs/token**.

The authors select the configuration $(24,10,5)$, marked by a gold star.

The problem is that **the key result is a tradeoff between two resources, but the visualization separates them into two different plots**. Readers must understand ternary coordinates, locate the same configuration in both panels, interpret two color scales, and mentally combine the results.

This makes it difficult to answer the central question: *Which architectures achieve a good balance between memory and computation, and why was this particular configuration selected?*

## The redesign

I suggest replacing the two ternary plots with **a single 2D scatter plot**, where each point represents one feasible architecture:

- **X-axis:** KV-cache memory (KB/token).
- **Y-axis:** Theoretical inference computation (GFLOPs/token).
- **Dashed reference lines:** The Vanilla 3B model's memory and FLOPs.
- **Highlighted star:** The selected configuration $(24,10,5)$.
- **Tooltips:** The layer allocation $(n_1,n_2,n_3)$ and resource requirements of each architecture.

The intersection of the two dashed lines represents the Vanilla baseline. Points near this intersection have similar memory and computational requirements, while points to the bottom-left use fewer resources on both axes.

The following Chart.js implementation establishes the reference axes using the paper's reported values. The complete redesign would add the feasible architectures from Figure 2, reconstructed using the formulas in Appendix B.

```chartjs
{
  "type": "scatter",
  "data": {
    "datasets": [
      {
        "label": "Vanilla 3B baseline",
        "data": [{"x": 266, "y": 5.54}],
        "backgroundColor": "#222222",
        "borderColor": "#222222",
        "pointRadius": 8,
        "pointStyle": "crossRot"
      },
      {
        "label": "Vanilla KV-cache reference",
        "data": [
          {"x": 266, "y": 5.05},
          {"x": 266, "y": 6.05}
        ],
        "showLine": true,
        "borderColor": "#888888",
        "borderDash": [6, 5],
        "borderWidth": 1.5,
        "pointRadius": 0
      },
      {
        "label": "Vanilla FLOPs reference",
        "data": [
          {"x": 175, "y": 5.54},
          {"x": 355, "y": 5.54}
        ],
        "showLine": true,
        "borderColor": "#888888",
        "borderDash": [6, 5],
        "borderWidth": 1.5,
        "pointRadius": 0
      }
    ]
  },
  "options": {
    "responsive": true,
    "plugins": {
      "title": {
        "display": true,
        "text": "Finding the right architecture: KV cache vs. inference FLOPs"
      },
      "subtitle": {
        "display": true,
        "text": "Baseline reference; feasible architecture points to be added"
      },
      "legend": {
        "position": "bottom"
      }
    },
    "scales": {
      "x": {
        "type": "linear",
        "min": 175,
        "max": 355,
        "title": {
          "display": true,
          "text": "KV cache (KB per token)"
        }
      },
      "y": {
        "min": 5.05,
        "max": 6.05,
        "title": {
          "display": true,
          "text": "Theoretical inference FLOPs per token (G)"
        }
      }
    }
  }
}
```
In the completed visualization, all feasible configurations would appear as small, semi-transparent points, with the selected configuration highlighted by a gold star. Hovering over a point would reveal its exact layer allocation and corresponding resource costs.

## What the new figure shows that the old one didn't

- **The tradeoff becomes immediately visible.** Instead of mentally combining two ternary plots, readers can directly observe the relationship between memory requirements and computational cost. Architectures that save memory at the expense of computation, or vice versa, become easy to identify.
- **The baseline becomes a meaningful reference point.** The intersection of the dashed lines represents the conventional 3B model. Readers can immediately see which architectures are more or less expensive on either dimension.
- **The architectural choice becomes easier to justify.** The selected $(24,10,5)$ configuration can be highlighted relative to the baseline, clearly demonstrating how closely it matches both resource requirements.
- **Better configurations become easier to identify.** The new plot makes it easy to see which architectures use less memory and computation, and which require a tradeoff between the two.

## Design decisions

- **One scatter plot instead of two ternary plots**, because the central question is about balancing two resource metrics rather than visualizing the proportions of three layer groups.
- **Direct comparison with Vanilla**, using reference lines at 266 KB/token and 5.54 GFLOPs/token instead of separate color scales.
- **Highlight the selected configuration**, making the authors' final architectural decision easy to identify.
- **Interactive tooltips for layer allocations**, preserving the architectural information encoded by ternary coordinates without requiring readers to interpret three axes.

The original ternary plots are still valuable for understanding how changing the relative depths affects memory and computation. They could remain in the appendix for readers interested in the architectural search space.

Interestingly, **Appendix C (Figure 9) already uses a similar FLOPs-versus-KV-cache scatter plot** to compare total layer budgets of 28, 39, and 50. My proposal is to apply that more intuitive representation to the *within-39-layer allocation search* in Figure 2, where it would directly support the selection of the final architecture.

Data: Figure 2, Table 1, and Appendices B–D of *Matryoshka Language Model Suites* (Godey and Artzi, 2026), [arXiv:2608.09703](https://arxiv.org/abs/2608.09703).
