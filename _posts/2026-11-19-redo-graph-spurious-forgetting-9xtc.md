
---
title: "A better Figure 5"
description: "Removing one direction restores forgotten facts: a direct comparison of old-fact recall before and after the intervention."
paper: spurious-forgetting
task: redo-graph
by: [golombi]
chart:
  chartjs: true
---

## The original

[Figure 5 in the original paper](https://arxiv.org/pdf/2610.08718)

Figure 5 (middle) shows that removing the top singular direction of each weight update during finetuning can restore the model's ability to recall old facts.

The authors compare the original finetuned model with a model whose updates have their top singular direction removed. They also compare against removing a random direction as a control.

The problem is that the figure uses continuous curves, making it difficult to compare the exact improvement between methods. Readers must estimate the distance between curves and mentally calculate how much old-fact recall was recovered.

The most important result is not immediately obvious: **removing a single direction can recover a large fraction of the apparently forgotten knowledge, while removing a random direction has almost no effect.**

## The redesign

Instead of continuous curves, I use grouped bars to directly compare old-fact recall under the three conditions at two meaningful checkpoints.

The values come from Table 3 of the paper, which reports accuracy at step 80 (the trough) and step 400 for two types of new facts.

```chartjs
{
  "type": "bar",
  "data": {
    "labels": [
      ["Synthetic facts", "Step 80"],
      ["Synthetic facts", "Step 400"],
      ["Real entities", "Step 80"],
      ["Real entities", "Step 400"]
    ],
    "datasets": [
      {
        "label": "Original finetuning",
        "data": [28, 38, 73, 55],
        "backgroundColor": "#E76F51",
        "borderRadius": 4
      },
      {
        "label": "Top direction removed",
        "data": [77, 70, 88, 79],
        "backgroundColor": "#2A9D8F",
        "borderRadius": 4
      },
      {
        "label": "Random direction removed",
        "data": [28, 38, 73, 55],
        "backgroundColor": "#A8ADB5",
        "borderRadius": 4
      }
    ]
  },
  "options": {
    "responsive": true,
    "plugins": {
      "title": {
        "display": true,
        "text": "Removing One Direction Restores Forgotten Facts",
        "font": {
          "size": 18,
          "weight": "bold"
        },
        "padding": {
          "bottom": 18
        }
      },
      "subtitle": {
        "display": true,
        "text": "Old-fact recall (%) — higher is better",
        "padding": {
          "bottom": 15
        }
      },
      "legend": {
        "position": "bottom"
      },
      "tooltip": {
        "callbacks": {
          "label": "function(context) { return context.dataset.label + ': ' + context.parsed.y + '%'; }"
        }
      }
    },
    "scales": {
      "y": {
        "beginAtZero": true,
        "max": 100,
        "title": {
          "display": true,
          "text": "Old-fact recall (%)"
        },
        "ticks": {
          "stepSize": 20
        }
      },
      "x": {
        "grid": {
          "display": false
        }
      }
    }
  }
}
```

**Main takeaway:** At step 80, removing the top direction increases old-fact recall from 28% to 77% for synthetic facts, a gain of 49 percentage points. Removing a random direction produces no improvement.

The same intervention also improves recall for real entities, suggesting that some apparently forgotten knowledge remains accessible when the harmful update direction is removed.

*Caption:* Old-fact recall in OLMo 2 1B under three finetuning conditions. Bars show the reported mean accuracies at steps 80 and 400, using values from Table 3. The top-direction intervention restores substantial old-fact recall, unlike the random-direction control. The intervention also reduces new-fact learning accuracy, a tradeoff not shown here.

## What changed and why

- **Replaced curves with grouped bars:** Makes the differences between interventions visible without requiring the reader to estimate distances between lines.
- **Selected two meaningful checkpoints:** Step 80 captures the collapse, while step 400 shows whether the improvement persists later in training.
- **Used consistent colors:** Red represents ordinary finetuning, green represents the proposed intervention, and gray represents the random-direction control.
- **Used percentages instead of decimals:** Makes accuracy easier to interpret immediately.
- **Kept the random-direction control:** Shows that the improvement is specific to the top direction, rather than simply removing any direction.
- **Included both types of new facts:** Shows that the intervention helps for both synthetic individuals and real entities.
- **Focused on old-fact recall:** Removes distracting information so the reader can immediately understand the paper's central finding about recoverable forgetting.

The redesigned figure emphasizes the distinction between **knowledge being destroyed** and **knowledge becoming temporarily inaccessible**, which is the central idea of the paper.
