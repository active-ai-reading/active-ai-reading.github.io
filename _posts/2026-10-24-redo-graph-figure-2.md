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
        "label": "(4, 14, 21) | widths (2112, 2112, 2304)",
        "data": [
          {
            "x": 337.5,
            "y": 6.363
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(5, 13, 21) | widths (1984, 2112, 2304)",
        "data": [
          {
            "x": 335.0,
            "y": 6.2791
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(5, 14, 20) | widths (1984, 2112, 2304)",
        "data": [
          {
            "x": 334.25,
            "y": 6.252
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(5, 15, 19) | widths (1984, 2016, 2304)",
        "data": [
          {
            "x": 327.875,
            "y": 6.0347
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(6, 12, 21) | widths (1856, 2208, 2304)",
        "data": [
          {
            "x": 336.0,
            "y": 6.3272
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(6, 13, 20) | widths (1856, 2112, 2304)",
        "data": [
          {
            "x": 330.75,
            "y": 6.1409
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(6, 14, 19) | widths (1856, 2016, 2432)",
        "data": [
          {
            "x": 334.25,
            "y": 6.3173
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(6, 15, 18) | widths (1856, 2016, 2432)",
        "data": [
          {
            "x": 332.625,
            "y": 6.2581
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(6, 16, 17) | widths (1856, 1920, 2432)",
        "data": [
          {
            "x": 325.0,
            "y": 6.0055
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(6, 17, 16) | widths (1856, 1920, 2560)",
        "data": [
          {
            "x": 331.0,
            "y": 6.2739
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(7, 11, 21) | widths (1728, 2304, 2304)",
        "data": [
          {
            "x": 335.25,
            "y": 6.3312
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(7, 12, 20) | widths (1728, 2208, 2304)",
        "data": [
          {
            "x": 330.75,
            "y": 6.1648
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(7, 13, 19) | widths (1728, 2112, 2304)",
        "data": [
          {
            "x": 325.5,
            "y": 5.9785
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(7, 14, 18) | widths (1728, 2016, 2432)",
        "data": [
          {
            "x": 328.5,
            "y": 6.1355
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(7, 15, 17) | widths (1728, 2016, 2432)",
        "data": [
          {
            "x": 326.875,
            "y": 6.0763
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(7, 16, 16) | widths (1728, 1920, 2560)",
        "data": [
          {
            "x": 327.25,
            "y": 6.1634
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(7, 17, 15) | widths (1728, 1920, 2560)",
        "data": [
          {
            "x": 324.75,
            "y": 6.0716
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(7, 18, 14) | widths (1728, 1824, 2688)",
        "data": [
          {
            "x": 322.5,
            "y": 6.0864
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(7, 19, 13) | widths (1728, 1824, 2816)",
        "data": [
          {
            "x": 325.625,
            "y": 6.2673
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(7, 20, 12) | widths (1728, 1728, 2944)",
        "data": [
          {
            "x": 320.25,
            "y": 6.1975
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(7, 21, 11) | widths (1728, 1728, 2944)",
        "data": [
          {
            "x": 315.5,
            "y": 6.0157
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(8, 11, 20) | widths (1664, 2304, 2304)",
        "data": [
          {
            "x": 331.0,
            "y": 6.2013
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(8, 12, 19) | widths (1664, 2208, 2304)",
        "data": [
          {
            "x": 326.5,
            "y": 6.0349
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(8, 13, 18) | widths (1664, 2112, 2432)",
        "data": [
          {
            "x": 330.25,
            "y": 6.2103
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(8, 14, 17) | widths (1664, 2016, 2432)",
        "data": [
          {
            "x": 323.75,
            "y": 5.9863
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(8, 15, 16) | widths (1664, 2016, 2560)",
        "data": [
          {
            "x": 330.125,
            "y": 6.2668
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(8, 16, 15) | widths (1664, 1920, 2560)",
        "data": [
          {
            "x": 322.0,
            "y": 5.9937
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(8, 17, 14) | widths (1664, 1824, 2688)",
        "data": [
          {
            "x": 320.125,
            "y": 6.0199
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(8, 18, 13) | widths (1664, 1824, 2816)",
        "data": [
          {
            "x": 323.25,
            "y": 6.2008
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(8, 19, 12) | widths (1664, 1728, 2944)",
        "data": [
          {
            "x": 318.25,
            "y": 6.1419
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(8, 20, 11) | widths (1664, 1728, 2944)",
        "data": [
          {
            "x": 313.5,
            "y": 5.9601
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(8, 21, 10) | widths (1664, 1728, 3072)",
        "data": [
          {
            "x": 313.75,
            "y": 6.0373
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(9, 11, 19) | widths (1536, 2304, 2304)",
        "data": [
          {
            "x": 324.0,
            "y": 6.002
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(9, 12, 18) | widths (1536, 2208, 2432)",
        "data": [
          {
            "x": 328.5,
            "y": 6.1975
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(9, 13, 17) | widths (1536, 2112, 2432)",
        "data": [
          {
            "x": 322.75,
            "y": 5.9917
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(9, 14, 16) | widths (1536, 2016, 2560)",
        "data": [
          {
            "x": 324.25,
            "y": 6.1074
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(9, 15, 15) | widths (1536, 2016, 2560)",
        "data": [
          {
            "x": 322.125,
            "y": 6.0277
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(9, 16, 14) | widths (1536, 1920, 2688)",
        "data": [
          {
            "x": 321.0,
            "y": 6.0681
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(9, 17, 13) | widths (1536, 1920, 2816)",
        "data": [
          {
            "x": 324.5,
            "y": 6.2605
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(9, 18, 12) | widths (1536, 1824, 2944)",
        "data": [
          {
            "x": 320.25,
            "y": 6.2134
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(9, 19, 11) | widths (1536, 1824, 2944)",
        "data": [
          {
            "x": 315.875,
            "y": 6.0425
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(9, 20, 10) | widths (1536, 1728, 3200)",
        "data": [
          {
            "x": 314.0,
            "y": 6.1819
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(9, 21, 9) | widths (1536, 1728, 3200)",
        "data": [
          {
            "x": 308.25,
            "y": 5.9498
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(9, 22, 8) | widths (1536, 1632, 3456)",
        "data": [
          {
            "x": 302.25,
            "y": 5.9519
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(9, 23, 7) | widths (1536, 1632, 3712)",
        "data": [
          {
            "x": 302.125,
            "y": 6.0911
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(9, 24, 6) | widths (1536, 1632, 3840)",
        "data": [
          {
            "x": 297.0,
            "y": 5.9336
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(9, 25, 5) | widths (1536, 1536, 4352)",
        "data": [
          {
            "x": 289.0,
            "y": 6.0251
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(9, 26, 4) | widths (1536, 1536, 4736)",
        "data": [
          {
            "x": 284.0,
            "y": 5.979
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(9, 27, 3) | widths (1536, 1536, 5248)",
        "data": [
          {
            "x": 277.5,
            "y": 5.8778
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(9, 28, 2) | widths (1536, 1536, 6144)",
        "data": [
          {
            "x": 270.0,
            "y": 5.8133
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(10, 11, 18) | widths (1472, 2304, 2432)",
        "data": [
          {
            "x": 327.5,
            "y": 6.2078
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(10, 12, 17) | widths (1472, 2208, 2432)",
        "data": [
          {
            "x": 322.5,
            "y": 6.0221
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(10, 13, 16) | widths (1472, 2112, 2560)",
        "data": [
          {
            "x": 324.75,
            "y": 6.1561
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(10, 14, 15) | widths (1472, 2016, 2688)",
        "data": [
          {
            "x": 325.25,
            "y": 6.2466
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(10, 15, 14) | widths (1472, 2016, 2688)",
        "data": [
          {
            "x": 322.625,
            "y": 6.1454
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(10, 16, 13) | widths (1472, 1920, 2816)",
        "data": [
          {
            "x": 320.5,
            "y": 6.1565
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(10, 17, 12) | widths (1472, 1824, 2944)",
        "data": [
          {
            "x": 316.625,
            "y": 6.1208
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(10, 18, 11) | widths (1472, 1824, 3072)",
        "data": [
          {
            "x": 317.75,
            "y": 6.2336
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(10, 19, 10) | widths (1472, 1728, 3200)",
        "data": [
          {
            "x": 310.75,
            "y": 6.1002
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(10, 20, 9) | widths (1472, 1728, 3328)",
        "data": [
          {
            "x": 309.5,
            "y": 6.1213
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(10, 21, 8) | widths (1472, 1728, 3456)",
        "data": [
          {
            "x": 307.25,
            "y": 6.0973
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(10, 22, 7) | widths (1472, 1632, 3712)",
        "data": [
          {
            "x": 299.25,
            "y": 6.0198
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(10, 23, 6) | widths (1472, 1632, 3968)",
        "data": [
          {
            "x": 297.125,
            "y": 6.0668
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(10, 24, 5) | widths (1472, 1632, 4224)",
        "data": [
          {
            "x": 293.0,
            "y": 6.0089
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(10, 25, 4) | widths (1472, 1536, 4736)",
        "data": [
          {
            "x": 281.5,
            "y": 5.9174
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(10, 26, 3) | widths (1472, 1536, 5248)",
        "data": [
          {
            "x": 275.0,
            "y": 5.8162
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(10, 27, 2) | widths (1472, 1536, 6144)",
        "data": [
          {
            "x": 267.5,
            "y": 5.7517
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(11, 10, 18) | widths (1408, 2400, 2432)",
        "data": [
          {
            "x": 325.25,
            "y": 6.1869
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(11, 11, 17) | widths (1408, 2304, 2432)",
        "data": [
          {
            "x": 321.0,
            "y": 6.023
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(11, 12, 16) | widths (1408, 2208, 2560)",
        "data": [
          {
            "x": 324.0,
            "y": 6.177
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(11, 13, 15) | widths (1408, 2112, 2688)",
        "data": [
          {
            "x": 325.25,
            "y": 6.2858
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(11, 14, 14) | widths (1408, 2016, 2688)",
        "data": [
          {
            "x": 317.75,
            "y": 6.0198
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(11, 15, 13) | widths (1408, 2016, 2816)",
        "data": [
          {
            "x": 321.625,
            "y": 6.2243
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(11, 16, 12) | widths (1408, 1920, 2944)",
        "data": [
          {
            "x": 318.5,
            "y": 6.2029
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(11, 17, 11) | widths (1408, 1824, 3072)",
        "data": [
          {
            "x": 313.625,
            "y": 6.1316
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(11, 18, 10) | widths (1408, 1824, 3200)",
        "data": [
          {
            "x": 313.75,
            "y": 6.2055
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(11, 19, 9) | widths (1408, 1728, 3328)",
        "data": [
          {
            "x": 305.75,
            "y": 6.0302
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(11, 20, 8) | widths (1408, 1728, 3456)",
        "data": [
          {
            "x": 303.5,
            "y": 6.0062
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(11, 21, 7) | widths (1408, 1728, 3584)",
        "data": [
          {
            "x": 300.25,
            "y": 5.934
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(11, 22, 6) | widths (1408, 1632, 3968)",
        "data": [
          {
            "x": 293.75,
            "y": 5.986
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(11, 23, 5) | widths (1408, 1632, 4224)",
        "data": [
          {
            "x": 289.625,
            "y": 5.9281
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(11, 24, 4) | widths (1408, 1632, 4608)",
        "data": [
          {
            "x": 285.5,
            "y": 5.9142
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(11, 25, 3) | widths (1408, 1536, 5376)",
        "data": [
          {
            "x": 273.5,
            "y": 5.8883
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(11, 26, 2) | widths (1408, 1536, 6272)",
        "data": [
          {
            "x": 265.5,
            "y": 5.795
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(11, 27, 1) | widths (1408, 1536, 8064)",
        "data": [
          {
            "x": 254.0,
            "y": 5.6099
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(12, 9, 18) | widths (1408, 2400, 2432)",
        "data": [
          {
            "x": 321.375,
            "y": 6.066
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(12, 10, 17) | widths (1408, 2304, 2560)",
        "data": [
          {
            "x": 326.0,
            "y": 6.2768
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(12, 11, 16) | widths (1408, 2208, 2560)",
        "data": [
          {
            "x": 320.875,
            "y": 6.0845
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(12, 12, 15) | widths (1408, 2112, 2688)",
        "data": [
          {
            "x": 322.5,
            "y": 6.2065
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(12, 13, 14) | widths (1408, 2112, 2688)",
        "data": [
          {
            "x": 320.25,
            "y": 6.118
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(12, 14, 13) | widths (1408, 2016, 2816)",
        "data": [
          {
            "x": 319.25,
            "y": 6.1577
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(12, 15, 12) | widths (1408, 1920, 2944)",
        "data": [
          {
            "x": 316.5,
            "y": 6.1483
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(12, 16, 11) | widths (1408, 1920, 2944)",
        "data": [
          {
            "x": 312.5,
            "y": 5.9889
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(12, 17, 10) | widths (1408, 1824, 3200)",
        "data": [
          {
            "x": 312.125,
            "y": 6.1625
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(12, 18, 9) | widths (1408, 1824, 3328)",
        "data": [
          {
            "x": 311.25,
            "y": 6.1945
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(12, 19, 8) | widths (1408, 1728, 3456)",
        "data": [
          {
            "x": 302.25,
            "y": 5.9741
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(12, 20, 7) | widths (1408, 1728, 3712)",
        "data": [
          {
            "x": 302.5,
            "y": 6.1237
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(12, 21, 6) | widths (1408, 1632, 3968)",
        "data": [
          {
            "x": 292.875,
            "y": 5.9642
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(12, 22, 5) | widths (1408, 1632, 4224)",
        "data": [
          {
            "x": 288.75,
            "y": 5.9063
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(12, 23, 4) | widths (1408, 1632, 4608)",
        "data": [
          {
            "x": 284.625,
            "y": 5.8924
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(12, 24, 3) | widths (1408, 1536, 5376)",
        "data": [
          {
            "x": 273.0,
            "y": 5.8762
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(12, 25, 2) | widths (1408, 1536, 6272)",
        "data": [
          {
            "x": 265.0,
            "y": 5.7829
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(12, 26, 1) | widths (1408, 1536, 8064)",
        "data": [
          {
            "x": 253.5,
            "y": 5.5978
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(13, 9, 17) | widths (1344, 2400, 2560)",
        "data": [
          {
            "x": 322.625,
            "y": 6.2271
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(13, 10, 16) | widths (1344, 2304, 2560)",
        "data": [
          {
            "x": 318.25,
            "y": 6.0572
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(13, 11, 15) | widths (1344, 2208, 2688)",
        "data": [
          {
            "x": 320.625,
            "y": 6.1999
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(13, 12, 14) | widths (1344, 2112, 2688)",
        "data": [
          {
            "x": 314.25,
            "y": 5.9655
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(13, 13, 13) | widths (1344, 2112, 2816)",
        "data": [
          {
            "x": 318.5,
            "y": 6.1827
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(13, 14, 12) | widths (1344, 2016, 2944)",
        "data": [
          {
            "x": 316.5,
            "y": 6.1898
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(13, 15, 11) | widths (1344, 1920, 3072)",
        "data": [
          {
            "x": 312.75,
            "y": 6.1448
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(13, 16, 10) | widths (1344, 1920, 3072)",
        "data": [
          {
            "x": 308.25,
            "y": 5.9608
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(13, 17, 9) | widths (1344, 1824, 3328)",
        "data": [
          {
            "x": 306.375,
            "y": 6.0782
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(13, 18, 8) | widths (1344, 1824, 3456)",
        "data": [
          {
            "x": 304.5,
            "y": 6.0652
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(13, 19, 7) | widths (1344, 1728, 3712)",
        "data": [
          {
            "x": 298.0,
            "y": 6.0183
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(13, 20, 6) | widths (1344, 1728, 3968)",
        "data": [
          {
            "x": 296.25,
            "y": 6.0756
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(13, 21, 5) | widths (1344, 1632, 4352)",
        "data": [
          {
            "x": 287.125,
            "y": 5.9995
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(13, 22, 4) | widths (1344, 1632, 4736)",
        "data": [
          {
            "x": 282.5,
            "y": 5.9631
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(13, 23, 3) | widths (1344, 1632, 5248)",
        "data": [
          {
            "x": 276.375,
            "y": 5.8716
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(13, 24, 2) | widths (1344, 1536, 6400)",
        "data": [
          {
            "x": 262.25,
            "y": 5.814
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(13, 25, 1) | widths (1344, 1536, 8192)",
        "data": [
          {
            "x": 250.25,
            "y": 5.5917
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(14, 9, 16) | widths (1280, 2496, 2560)",
        "data": [
          {
            "x": 317.75,
            "y": 6.1353
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(14, 10, 15) | widths (1280, 2304, 2688)",
        "data": [
          {
            "x": 317.5,
            "y": 6.1651
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(14, 11, 14) | widths (1280, 2208, 2816)",
        "data": [
          {
            "x": 318.875,
            "y": 6.2795
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(14, 12, 13) | widths (1280, 2208, 2816)",
        "data": [
          {
            "x": 316.5,
            "y": 6.1817
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(14, 13, 12) | widths (1280, 2112, 2944)",
        "data": [
          {
            "x": 315.25,
            "y": 6.2072
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(14, 14, 11) | widths (1280, 2016, 3072)",
        "data": [
          {
            "x": 312.25,
            "y": 6.1787
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(14, 15, 10) | widths (1280, 1920, 3200)",
        "data": [
          {
            "x": 307.5,
            "y": 6.0948
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(14, 16, 9) | widths (1280, 1920, 3328)",
        "data": [
          {
            "x": 307.0,
            "y": 6.1384
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(14, 17, 8) | widths (1280, 1824, 3456)",
        "data": [
          {
            "x": 299.125,
            "y": 5.9413
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(14, 18, 7) | widths (1280, 1824, 3712)",
        "data": [
          {
            "x": 299.75,
            "y": 6.1017
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(14, 19, 6) | widths (1280, 1728, 3968)",
        "data": [
          {
            "x": 291.25,
            "y": 5.9626
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(14, 20, 5) | widths (1280, 1728, 4224)",
        "data": [
          {
            "x": 287.5,
            "y": 5.915
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(14, 21, 4) | widths (1280, 1632, 4736)",
        "data": [
          {
            "x": 277.875,
            "y": 5.8604
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(14, 22, 3) | widths (1280, 1632, 5376)",
        "data": [
          {
            "x": 273.25,
            "y": 5.9121
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(14, 23, 2) | widths (1280, 1632, 6272)",
        "data": [
          {
            "x": 265.625,
            "y": 5.8285
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(14, 24, 1) | widths (1280, 1536, 8320)",
        "data": [
          {
            "x": 246.5,
            "y": 5.5789
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(15, 9, 15) | widths (1280, 2400, 2688)",
        "data": [
          {
            "x": 316.875,
            "y": 6.1777
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(15, 10, 14) | widths (1280, 2304, 2688)",
        "data": [
          {
            "x": 312.0,
            "y": 5.9863
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(15, 11, 13) | widths (1280, 2208, 2816)",
        "data": [
          {
            "x": 312.875,
            "y": 6.0782
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(15, 12, 12) | widths (1280, 2112, 2944)",
        "data": [
          {
            "x": 312.0,
            "y": 6.1169
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(15, 13, 11) | widths (1280, 2016, 3072)",
        "data": [
          {
            "x": 309.375,
            "y": 6.101
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(15, 14, 10) | widths (1280, 2016, 3200)",
        "data": [
          {
            "x": 310.25,
            "y": 6.1986
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(15, 15, 9) | widths (1280, 1920, 3328)",
        "data": [
          {
            "x": 304.5,
            "y": 6.0728
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(15, 16, 8) | widths (1280, 1920, 3456)",
        "data": [
          {
            "x": 303.0,
            "y": 6.0713
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(15, 17, 7) | widths (1280, 1824, 3712)",
        "data": [
          {
            "x": 297.625,
            "y": 6.0477
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(15, 18, 6) | widths (1280, 1824, 3840)",
        "data": [
          {
            "x": 293.25,
            "y": 5.9114
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(15, 19, 5) | widths (1280, 1728, 4352)",
        "data": [
          {
            "x": 288.25,
            "y": 6.0601
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(15, 20, 4) | widths (1280, 1728, 4608)",
        "data": [
          {
            "x": 282.0,
            "y": 5.8684
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(15, 21, 3) | widths (1280, 1632, 5376)",
        "data": [
          {
            "x": 271.875,
            "y": 5.8793
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(15, 22, 2) | widths (1280, 1632, 6272)",
        "data": [
          {
            "x": 264.25,
            "y": 5.7957
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(15, 23, 1) | widths (1280, 1632, 8064)",
        "data": [
          {
            "x": 253.125,
            "y": 5.6203
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(16, 8, 15) | widths (1216, 2592, 2688)",
        "data": [
          {
            "x": 314.5,
            "y": 6.2094
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(16, 9, 14) | widths (1216, 2400, 2816)",
        "data": [
          {
            "x": 314.375,
            "y": 6.2454
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(16, 10, 13) | widths (1216, 2304, 2816)",
        "data": [
          {
            "x": 309.0,
            "y": 6.0314
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(16, 11, 12) | widths (1216, 2208, 2944)",
        "data": [
          {
            "x": 308.875,
            "y": 6.0908
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(16, 12, 11) | widths (1216, 2112, 3072)",
        "data": [
          {
            "x": 307.0,
            "y": 6.0938
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(16, 13, 10) | widths (1216, 2112, 3200)",
        "data": [
          {
            "x": 308.25,
            "y": 6.204
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(16, 14, 9) | widths (1216, 2016, 3328)",
        "data": [
          {
            "x": 303.25,
            "y": 6.0948
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(16, 15, 8) | widths (1216, 1920, 3456)",
        "data": [
          {
            "x": 296.5,
            "y": 5.9239
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(16, 16, 7) | widths (1216, 1920, 3712)",
        "data": [
          {
            "x": 297.5,
            "y": 6.0959
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(16, 17, 6) | widths (1216, 1824, 3968)",
        "data": [
          {
            "x": 290.125,
            "y": 5.9801
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(16, 18, 5) | widths (1216, 1824, 4224)",
        "data": [
          {
            "x": 286.75,
            "y": 5.9434
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(16, 19, 4) | widths (1216, 1728, 4736)",
        "data": [
          {
            "x": 278.25,
            "y": 5.9091
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(16, 20, 3) | widths (1216, 1728, 5248)",
        "data": [
          {
            "x": 272.5,
            "y": 5.828
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(16, 21, 2) | widths (1216, 1632, 6400)",
        "data": [
          {
            "x": 259.875,
            "y": 5.7975
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(16, 22, 1) | widths (1216, 1632, 8192)",
        "data": [
          {
            "x": 248.25,
            "y": 5.5849
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(17, 7, 15) | widths (1216, 2688, 2688)",
        "data": [
          {
            "x": 311.75,
            "y": 6.1553
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(17, 8, 14) | widths (1216, 2496, 2816)",
        "data": [
          {
            "x": 312.75,
            "y": 6.2287
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(17, 9, 13) | widths (1216, 2400, 2816)",
        "data": [
          {
            "x": 308.125,
            "y": 6.0389
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(17, 10, 12) | widths (1216, 2304, 2944)",
        "data": [
          {
            "x": 308.75,
            "y": 6.1207
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(17, 11, 11) | widths (1216, 2208, 3072)",
        "data": [
          {
            "x": 307.625,
            "y": 6.1444
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(17, 12, 10) | widths (1216, 2112, 3200)",
        "data": [
          {
            "x": 304.75,
            "y": 6.1086
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(17, 13, 9) | widths (1216, 2016, 3328)",
        "data": [
          {
            "x": 300.125,
            "y": 6.012
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(17, 14, 8) | widths (1216, 2016, 3456)",
        "data": [
          {
            "x": 299.0,
            "y": 6.0226
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(17, 15, 7) | widths (1216, 1920, 3712)",
        "data": [
          {
            "x": 294.75,
            "y": 6.0252
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(17, 16, 6) | widths (1216, 1824, 3968)",
        "data": [
          {
            "x": 287.75,
            "y": 5.9209
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(17, 17, 5) | widths (1216, 1824, 4224)",
        "data": [
          {
            "x": 284.375,
            "y": 5.8842
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(17, 18, 4) | widths (1216, 1728, 4736)",
        "data": [
          {
            "x": 276.25,
            "y": 5.8609
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(17, 19, 3) | widths (1216, 1728, 5376)",
        "data": [
          {
            "x": 272.0,
            "y": 5.9229
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(17, 20, 2) | widths (1216, 1728, 6144)",
        "data": [
          {
            "x": 263.75,
            "y": 5.7353
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(17, 21, 1) | widths (1216, 1632, 8192)",
        "data": [
          {
            "x": 246.625,
            "y": 5.547
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(18, 7, 14) | widths (1152, 2688, 2816)",
        "data": [
          {
            "x": 308.5,
            "y": 6.2123
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(18, 8, 13) | widths (1152, 2592, 2816)",
        "data": [
          {
            "x": 305.0,
            "y": 6.06
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(18, 9, 12) | widths (1152, 2400, 2944)",
        "data": [
          {
            "x": 303.375,
            "y": 6.0409
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(18, 10, 11) | widths (1152, 2304, 3072)",
        "data": [
          {
            "x": 303.0,
            "y": 6.087
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(18, 11, 10) | widths (1152, 2208, 3200)",
        "data": [
          {
            "x": 300.875,
            "y": 6.0719
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(18, 12, 9) | widths (1152, 2112, 3328)",
        "data": [
          {
            "x": 297.0,
            "y": 5.9942
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(18, 13, 8) | widths (1152, 2112, 3456)",
        "data": [
          {
            "x": 296.25,
            "y": 6.0174
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(18, 14, 7) | widths (1152, 2016, 3712)",
        "data": [
          {
            "x": 292.75,
            "y": 6.0366
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(18, 15, 6) | widths (1152, 1920, 3968)",
        "data": [
          {
            "x": 286.5,
            "y": 5.947
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(18, 16, 5) | widths (1152, 1920, 4224)",
        "data": [
          {
            "x": 283.5,
            "y": 5.9218
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(18, 17, 4) | widths (1152, 1824, 4736)",
        "data": [
          {
            "x": 276.125,
            "y": 5.9109
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(18, 18, 3) | widths (1152, 1824, 5248)",
        "data": [
          {
            "x": 270.75,
            "y": 5.8406
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(18, 19, 2) | widths (1152, 1728, 6272)",
        "data": [
          {
            "x": 258.25,
            "y": 5.7141
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(18, 20, 1) | widths (1152, 1728, 8192)",
        "data": [
          {
            "x": 248.0,
            "y": 5.6282
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(19, 7, 13) | widths (1152, 2688, 2816)",
        "data": [
          {
            "x": 302.0,
            "y": 6.001
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(19, 8, 12) | widths (1152, 2496, 2944)",
        "data": [
          {
            "x": 301.5,
            "y": 6.0194
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(19, 9, 11) | widths (1152, 2400, 3072)",
        "data": [
          {
            "x": 301.875,
            "y": 6.0896
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(19, 10, 10) | widths (1152, 2304, 3200)",
        "data": [
          {
            "x": 300.5,
            "y": 6.0969
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(19, 11, 9) | widths (1152, 2208, 3328)",
        "data": [
          {
            "x": 297.375,
            "y": 6.0399
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(19, 12, 8) | widths (1152, 2112, 3584)",
        "data": [
          {
            "x": 296.5,
            "y": 6.1604
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(19, 13, 7) | widths (1152, 2016, 3712)",
        "data": [
          {
            "x": 289.375,
            "y": 5.949
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(19, 14, 6) | widths (1152, 2016, 3968)",
        "data": [
          {
            "x": 288.75,
            "y": 6.0408
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(19, 15, 5) | widths (1152, 1920, 4352)",
        "data": [
          {
            "x": 283.0,
            "y": 6.0346
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(19, 16, 4) | widths (1152, 1824, 4736)",
        "data": [
          {
            "x": 273.5,
            "y": 5.8469
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(19, 17, 3) | widths (1152, 1824, 5376)",
        "data": [
          {
            "x": 269.625,
            "y": 5.9198
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(19, 18, 2) | widths (1152, 1728, 6400)",
        "data": [
          {
            "x": 257.0,
            "y": 5.7774
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(19, 19, 1) | widths (1152, 1728, 8192)",
        "data": [
          {
            "x": 245.75,
            "y": 5.5751
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(20, 6, 13) | widths (1088, 2880, 2944)",
        "data": [
          {
            "x": 302.0,
            "y": 6.2451
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(20, 7, 12) | widths (1088, 2688, 2944)",
        "data": [
          {
            "x": 296.5,
            "y": 5.9937
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(20, 8, 11) | widths (1088, 2592, 3072)",
        "data": [
          {
            "x": 298.0,
            "y": 6.1014
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(20, 9, 10) | widths (1088, 2400, 3200)",
        "data": [
          {
            "x": 294.375,
            "y": 6.0078
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(20, 10, 9) | widths (1088, 2304, 3328)",
        "data": [
          {
            "x": 292.0,
            "y": 5.9732
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(20, 11, 8) | widths (1088, 2208, 3584)",
        "data": [
          {
            "x": 291.875,
            "y": 6.1143
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(20, 12, 7) | widths (1088, 2112, 3712)",
        "data": [
          {
            "x": 285.5,
            "y": 5.9218
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(20, 13, 6) | widths (1088, 2112, 3968)",
        "data": [
          {
            "x": 285.25,
            "y": 6.0263
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(20, 14, 5) | widths (1088, 2016, 4352)",
        "data": [
          {
            "x": 280.25,
            "y": 6.0366
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(20, 15, 4) | widths (1088, 1920, 4736)",
        "data": [
          {
            "x": 271.5,
            "y": 5.8636
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(20, 16, 3) | widths (1088, 1920, 5248)",
        "data": [
          {
            "x": 266.5,
            "y": 5.8049
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(20, 17, 2) | widths (1088, 1824, 6400)",
        "data": [
          {
            "x": 256.125,
            "y": 5.8181
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(20, 18, 1) | widths (1088, 1824, 8192)",
        "data": [
          {
            "x": 245.25,
            "y": 5.6267
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(21, 6, 12) | widths (1088, 2880, 2944)",
        "data": [
          {
            "x": 294.75,
            "y": 6.0056
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(21, 7, 11) | widths (1088, 2688, 3072)",
        "data": [
          {
            "x": 294.75,
            "y": 6.0378
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(21, 8, 10) | widths (1088, 2592, 3200)",
        "data": [
          {
            "x": 295.25,
            "y": 6.1068
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(21, 9, 9) | widths (1088, 2400, 3328)",
        "data": [
          {
            "x": 290.625,
            "y": 5.9713
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(21, 10, 8) | widths (1088, 2304, 3584)",
        "data": [
          {
            "x": 291.25,
            "y": 6.1348
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(21, 11, 7) | widths (1088, 2208, 3712)",
        "data": [
          {
            "x": 285.625,
            "y": 5.963
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(21, 12, 6) | widths (1088, 2112, 3968)",
        "data": [
          {
            "x": 281.25,
            "y": 5.9214
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(21, 13, 5) | widths (1088, 2016, 4352)",
        "data": [
          {
            "x": 276.625,
            "y": 5.9444
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(21, 14, 4) | widths (1088, 2016, 4736)",
        "data": [
          {
            "x": 273.5,
            "y": 5.9528
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(21, 15, 3) | widths (1088, 1920, 5376)",
        "data": [
          {
            "x": 264.75,
            "y": 5.868
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(21, 16, 2) | widths (1088, 1824, 6400)",
        "data": [
          {
            "x": 253.25,
            "y": 5.7495
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(21, 17, 1) | widths (1088, 1824, 8192)",
        "data": [
          {
            "x": 242.375,
            "y": 5.5581
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(22, 6, 11) | widths (1088, 2880, 3072)",
        "data": [
          {
            "x": 293.0,
            "y": 6.0498
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(22, 7, 10) | widths (1088, 2688, 3200)",
        "data": [
          {
            "x": 292.0,
            "y": 6.0432
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(22, 8, 9) | widths (1088, 2496, 3328)",
        "data": [
          {
            "x": 288.5,
            "y": 5.9452
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(22, 9, 8) | widths (1088, 2400, 3584)",
        "data": [
          {
            "x": 289.875,
            "y": 6.1329
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(22, 10, 7) | widths (1088, 2304, 3712)",
        "data": [
          {
            "x": 285.0,
            "y": 5.9834
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(22, 11, 6) | widths (1088, 2208, 3968)",
        "data": [
          {
            "x": 281.375,
            "y": 5.9626
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(22, 12, 5) | widths (1088, 2112, 4352)",
        "data": [
          {
            "x": 277.5,
            "y": 6.0044
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(22, 13, 4) | widths (1088, 2016, 4736)",
        "data": [
          {
            "x": 269.875,
            "y": 5.8607
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(22, 14, 3) | widths (1088, 2016, 5248)",
        "data": [
          {
            "x": 265.25,
            "y": 5.814
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(22, 15, 2) | widths (1088, 1920, 6272)",
        "data": [
          {
            "x": 255.0,
            "y": 5.737
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(22, 16, 1) | widths (1088, 1824, 8320)",
        "data": [
          {
            "x": 240.0,
            "y": 5.5698
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(23, 6, 10) | widths (1024, 2880, 3200)",
        "data": [
          {
            "x": 284.5,
            "y": 5.9556
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(23, 7, 9) | widths (1024, 2688, 3456)",
        "data": [
          {
            "x": 287.0,
            "y": 6.1698
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(23, 8, 8) | widths (1024, 2592, 3584)",
        "data": [
          {
            "x": 285.0,
            "y": 6.1323
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(23, 9, 7) | widths (1024, 2400, 3840)",
        "data": [
          {
            "x": 281.375,
            "y": 6.1111
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(23, 10, 6) | widths (1024, 2304, 4096)",
        "data": [
          {
            "x": 278.0,
            "y": 6.0943
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(23, 11, 5) | widths (1024, 2208, 4352)",
        "data": [
          {
            "x": 271.875,
            "y": 5.946
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(23, 12, 4) | widths (1024, 2112, 4864)",
        "data": [
          {
            "x": 267.0,
            "y": 5.991
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(23, 13, 3) | widths (1024, 2112, 5376)",
        "data": [
          {
            "x": 262.25,
            "y": 5.9304
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(23, 14, 2) | widths (1024, 2016, 6272)",
        "data": [
          {
            "x": 251.25,
            "y": 5.7267
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(23, 15, 1) | widths (1024, 1920, 8320)",
        "data": [
          {
            "x": 237.0,
            "y": 5.5742
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(24, 5, 10) | widths (1024, 3072, 3328)",
        "data": [
          {
            "x": 286.0,
            "y": 6.1866
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(24, 6, 9) | widths (1024, 2880, 3456)",
        "data": [
          {
            "x": 285.0,
            "y": 6.1774
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(24, 7, 8) | widths (1024, 2688, 3584)",
        "data": [
          {
            "x": 281.5,
            "y": 6.0644
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(24, 8, 7) | widths (1024, 2496, 3840)",
        "data": [
          {
            "x": 279.0,
            "y": 6.0807
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(24, 9, 6) | widths (1024, 2400, 4096)",
        "data": [
          {
            "x": 276.375,
            "y": 6.0881
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(24, 11, 4) | widths (1024, 2208, 4736)",
        "data": [
          {
            "x": 264.875,
            "y": 5.858
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(24, 12, 3) | widths (1024, 2112, 5376)",
        "data": [
          {
            "x": 258.0,
            "y": 5.8212
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(24, 13, 2) | widths (1024, 2016, 6400)",
        "data": [
          {
            "x": 248.375,
            "y": 5.7466
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(24, 14, 1) | widths (1024, 2016, 8192)",
        "data": [
          {
            "x": 238.25,
            "y": 5.5789
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(25, 5, 9) | widths (1024, 3072, 3456)",
        "data": [
          {
            "x": 281.5,
            "y": 6.1284
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(25, 6, 8) | widths (1024, 2880, 3584)",
        "data": [
          {
            "x": 279.5,
            "y": 6.072
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(25, 7, 7) | widths (1024, 2688, 3712)",
        "data": [
          {
            "x": 275.0,
            "y": 5.9087
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(25, 8, 6) | widths (1024, 2496, 4096)",
        "data": [
          {
            "x": 274.0,
            "y": 6.0576
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(25, 9, 5) | widths (1024, 2400, 4352)",
        "data": [
          {
            "x": 269.375,
            "y": 5.9559
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(25, 10, 4) | widths (1024, 2304, 4736)",
        "data": [
          {
            "x": 264.0,
            "y": 5.8741
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(25, 11, 3) | widths (1024, 2208, 5376)",
        "data": [
          {
            "x": 257.875,
            "y": 5.858
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(25, 12, 2) | widths (1024, 2112, 6400)",
        "data": [
          {
            "x": 249.0,
            "y": 5.8023
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(25, 13, 1) | widths (1024, 2016, 8320)",
        "data": [
          {
            "x": 234.875,
            "y": 5.5626
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(27, 4, 8) | widths (960, 3456, 3584)",
        "data": [
          {
            "x": 267.25,
            "y": 5.9657
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(27, 5, 7) | widths (960, 3072, 3840)",
        "data": [
          {
            "x": 266.25,
            "y": 5.9867
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(27, 6, 6) | widths (960, 2880, 4096)",
        "data": [
          {
            "x": 264.75,
            "y": 6.0127
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(27, 7, 5) | widths (960, 2688, 4352)",
        "data": [
          {
            "x": 259.75,
            "y": 5.8729
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(27, 8, 4) | widths (960, 2592, 4736)",
        "data": [
          {
            "x": 256.25,
            "y": 5.8528
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(27, 9, 3) | widths (960, 2400, 5504)",
        "data": [
          {
            "x": 250.125,
            "y": 5.9044
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(27, 10, 2) | widths (960, 2304, 6400)",
        "data": [
          {
            "x": 241.25,
            "y": 5.7455
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(27, 11, 1) | widths (960, 2208, 8320)",
        "data": [
          {
            "x": 228.625,
            "y": 5.5454
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(28, 4, 7) | widths (960, 3360, 3840)",
        "data": [
          {
            "x": 262.5,
            "y": 5.9513
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(28, 5, 6) | widths (960, 3072, 4096)",
        "data": [
          {
            "x": 261.0,
            "y": 5.9596
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(28, 6, 5) | widths (960, 2880, 4352)",
        "data": [
          {
            "x": 257.5,
            "y": 5.8765
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(28, 7, 4) | widths (960, 2688, 4864)",
        "data": [
          {
            "x": 254.5,
            "y": 5.9507
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(28, 8, 3) | widths (960, 2496, 5504)",
        "data": [
          {
            "x": 247.5,
            "y": 5.8699
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(28, 9, 2) | widths (960, 2400, 6400)",
        "data": [
          {
            "x": 239.375,
            "y": 5.7352
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(28, 10, 1) | widths (960, 2304, 8320)",
        "data": [
          {
            "x": 227.5,
            "y": 5.5575
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(29, 3, 7) | widths (960, 3744, 3968)",
        "data": [
          {
            "x": 261.125,
            "y": 6.1179
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(29, 4, 6) | widths (960, 3360, 4096)",
        "data": [
          {
            "x": 257.25,
            "y": 5.9242
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(29, 5, 5) | widths (960, 3072, 4480)",
        "data": [
          {
            "x": 256.25,
            "y": 6.0169
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(29, 6, 4) | widths (960, 2880, 4864)",
        "data": [
          {
            "x": 252.25,
            "y": 5.9542
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(29, 7, 3) | widths (960, 2688, 5504)",
        "data": [
          {
            "x": 246.75,
            "y": 5.923
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(29, 8, 2) | widths (960, 2496, 6400)",
        "data": [
          {
            "x": 236.75,
            "y": 5.7007
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(29, 9, 1) | widths (960, 2400, 8320)",
        "data": [
          {
            "x": 225.625,
            "y": 5.5471
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(31, 3, 5) | widths (896, 3840, 4480)",
        "data": [
          {
            "x": 241.0,
            "y": 5.8636
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(31, 4, 4) | widths (896, 3456, 4864)",
        "data": [
          {
            "x": 238.5,
            "y": 5.8317
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(31, 5, 3) | widths (896, 3072, 5632)",
        "data": [
          {
            "x": 234.5,
            "y": 5.9051
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(31, 6, 2) | widths (896, 2880, 6528)",
        "data": [
          {
            "x": 227.0,
            "y": 5.758
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(31, 7, 1) | widths (896, 2688, 8448)",
        "data": [
          {
            "x": 215.0,
            "y": 5.5291
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(32, 2, 5) | widths (896, 4416, 4608)",
        "data": [
          {
            "x": 236.5,
            "y": 5.9205
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(32, 3, 4) | widths (896, 3840, 4992)",
        "data": [
          {
            "x": 235.0,
            "y": 5.9182
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(32, 4, 3) | widths (896, 3360, 5632)",
        "data": [
          {
            "x": 230.5,
            "y": 5.8659
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(32, 5, 2) | widths (896, 3072, 6528)",
        "data": [
          {
            "x": 223.0,
            "y": 5.7011
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(32, 6, 1) | widths (896, 2880, 8448)",
        "data": [
          {
            "x": 212.5,
            "y": 5.5289
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(33, 2, 4) | widths (896, 4416, 5120)",
        "data": [
          {
            "x": 230.0,
            "y": 5.9546
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(33, 3, 3) | widths (896, 3744, 5632)",
        "data": [
          {
            "x": 225.375,
            "y": 5.7922
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(33, 4, 2) | widths (896, 3360, 6656)",
        "data": [
          {
            "x": 220.0,
            "y": 5.7825
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(33, 5, 1) | widths (896, 3072, 8576)",
        "data": [
          {
            "x": 209.0,
            "y": 5.5543
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(34, 2, 3) | widths (896, 4416, 5760)",
        "data": [
          {
            "x": 221.0,
            "y": 5.8728
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(34, 3, 2) | widths (896, 3744, 6656)",
        "data": [
          {
            "x": 214.875,
            "y": 5.7088
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(34, 4, 1) | widths (896, 3360, 8576)",
        "data": [
          {
            "x": 205.0,
            "y": 5.5151
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(36, 1, 2) | widths (832, 5664, 7040)",
        "data": [
          {
            "x": 194.125,
            "y": 5.688
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(36, 2, 1) | widths (832, 4512, 8960)",
        "data": [
          {
            "x": 187.25,
            "y": 5.5502
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "(37, 1, 1) | widths (832, 5664, 9216)",
        "data": [
          {
            "x": 178.375,
            "y": 5.4701
          }
        ],
        "backgroundColor": "rgba(70,113,155,0.45)",
        "borderColor": "rgba(70,113,155,0.5)",
        "pointRadius": 3,
        "pointHoverRadius": 7
      },
      {
        "label": "Vanilla 3B (paper Figure 2 reference)",
        "data": [
          {
            "x": 266,
            "y": 5.54
          }
        ],
        "backgroundColor": "#1d1d1d",
        "pointStyle": "rectRot",
        "pointRadius": 8,
        "pointHoverRadius": 10
      },
      {
        "label": "Chosen Matryoshka (24, 10, 5) | widths (1024, 2304, 4352)",
        "data": [
          {
            "x": 271,
            "y": 5.9622
          }
        ],
        "backgroundColor": "#eab308",
        "borderColor": "#854d0e",
        "borderWidth": 2,
        "pointStyle": "star",
        "pointRadius": 12,
        "pointHoverRadius": 14
      },
      {
        "label": "Vanilla memory reference",
        "data": [
          {
            "x": 266,
            "y": 5.2
          },
          {
            "x": 266,
            "y": 6.45
          }
        ],
        "showLine": true,
        "borderColor": "rgba(35,35,35,0.5)",
        "borderDash": [
          6,
          5
        ],
        "pointRadius": 0
      },
      {
        "label": "Vanilla FLOPs reference",
        "data": [
          {
            "x": 170,
            "y": 5.54
          },
          {
            "x": 350,
            "y": 5.54
          }
        ],
        "showLine": true,
        "borderColor": "rgba(35,35,35,0.5)",
        "borderDash": [
          6,
          5
        ],
        "pointRadius": 0
      }
    ]
  },
  "options": {
    "responsive": true,
    "plugins": {
      "title": {
        "display": true,
        "text": "Matryoshka architecture sweep: KV cache vs. inference FLOPs"
      },
      "subtitle": {
        "display": true,
        "text": "Reconstructed from Appendix B equations (not digitized Figure 2 coordinates)"
      },
      "legend": {
        "display": false
      },
      "tooltip": {
        "enabled": true
      }
    },
    "scales": {
      "x": {
        "type": "linear",
        "min": 170,
        "max": 350,
        "title": {
          "display": true,
          "text": "KV cache (KB per token, bf16)"
        }
      },
      "y": {
        "min": 5.2,
        "max": 6.45,
        "title": {
          "display": true,
          "text": "Theoretical inference GFLOPs per token"
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
