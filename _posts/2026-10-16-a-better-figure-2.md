---
title: "A better Figure 2: the threshold the bar chart hides"
description: The paper's key soft-mapping result is a curve with a cliff. Drawn as bars, the cliff disappears.
paper: cross-lingual-knowledge-pretraining
role: visualization
task: redo-graph
by: [course-team]
example: true
chart:
  chartjs: true
---

## The original

{% include figure.liquid path="assets/img/papers/cross-lingual-knowledge-pretraining/figure2.png" class="img-fluid rounded z-depth-1" caption="Figure 2 of the paper (CC BY 4.0): CLeq for the English₁–English₂ clone setup under different conditions." %}

Figure 2 mixes two kinds of things in one bar chart: **conditions** (baseline, same data, same initialization) and **points on a dial** (soft-mapping at 20% and 99.9%, where a fraction *p* of each token pair's embedding is shared). The text's main claim about this experiment is a *sharp threshold*: "At 20% tying, generalization remains weak with CLeq = 8.6%; at 50% tying it jumps to 82.7%". But the 50% point, the one that shows the jump, is not in the figure.

The full sweep is in the appendix (the soft-mapping table), and it covers **two settings**: the clone languages, and English–WWT-Arabic. Plotted together, they tell a better story.

## The redesign

Each line is normalized by its own value at full sharing (p = 100%), so both fit on one axis: "how much of the achievable transfer do you get when sharing a fraction *p* of the embedding?" Hover a point for the raw CLeq.

```chartjs
{
  "type": "line",
  "data": {
    "labels": ["0%", "20%", "50%", "90%", "99%", "99.9%", "100%"],
    "datasets": [
      {
        "label": "English₁–English₂ (clone languages)",
        "data": [-2.6, 8.6, 82.7, 95.8, 99.1, 99.0, 100],
        "borderColor": "#2f6fde",
        "backgroundColor": "#2f6fde",
        "borderWidth": 3,
        "pointRadius": 5,
        "tension": 0
      },
      {
        "label": "English–WWT-Arabic (natural pair)",
        "data": [null, 7.9, 13.5, 76.2, 83.3, 81.0, 100],
        "borderColor": "#e8590c",
        "backgroundColor": "#e8590c",
        "borderWidth": 3,
        "pointRadius": 5,
        "tension": 0
      }
    ]
  },
  "options": {
    "responsive": true,
    "plugins": {
      "title": { "display": true, "text": "Share of the achievable transfer vs. fraction of embedding shared" },
      "legend": { "position": "bottom" }
    },
    "scales": {
      "x": { "title": { "display": true, "text": "Fraction p of each token pair's embedding that is tied (not to scale)" } },
      "y": { "min": -10, "max": 105, "title": { "display": true, "text": "% of CLeq at full sharing" } }
    }
  }
}
```

| p (tied) | 0% | 20% | 50% | 90% | 99% | 99.9% | 100% |
| --- | --- | --- | --- | --- | --- | --- | --- |
| En₁–En₂, raw CLeq | −2.6% | 8.6% | 82.7% | 95.8% | 99.1% | 99.0% | 100% |
| En–WWT-Ar, raw CLeq | — | 1.0% | 1.7% | 9.6% | 10.5% | 10.2% | 12.6% |

## What the new figure shows that the old one didn't

- **The cliff is real, and it's in a different place for the two settings.** Clone languages jump between 20% and 50% sharing. The natural pair is still at 13% of its ceiling at 50%, and only jumps between 50% and 90%. Natural languages need much more sharing before knowledge flows.
- **Reserving a few language-specific dimensions is cheap.** At p = 90% (96 free dimensions out of 960) the natural pair keeps 76% of the benefit, which supports the paper's "soft mapping" proposal for restoring language identity.
- **It invites the right next question:** where exactly between 50% and 90% is the WWT cliff, and why is it later?

## Design decisions

- **A line, not bars**, because *p* is a dial, not a set of categories.
- **Normalize each series** so a 12.6%-max curve and a 100%-max curve can share an axis. The raw numbers stay in the table and tooltips.
- **Conditions that aren't on the dial** (same data, same initialization) belong in a separate, small panel or table, not in the same bar list.
- **Honest axis:** the x-axis is evenly spaced but the values are not, so it says "not to scale". Plotting the number of free dimensions on a log axis would be a scale-true alternative; try it!

Data: the appendix soft-mapping table and Figure 2 of {% cite gaber2026crosslingual %}.
