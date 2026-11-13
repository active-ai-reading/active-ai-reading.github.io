---
title: "Making the parameter cost of tokenization visible"
description: "Replacing Table 2.1 with a ranked bar chart makes differences easier to see and model families easier to compare."
paper: tokenization-survey
role: visualization
task: redo-graph
by: [Shueyr]
og_image: /assets/img/posts/tokenization-redo-graph/Table_2_1_redo_tokenization.jpg
chart:
  chartjs: true
---

## The original

{% include figure.liquid path="assets/img/papers/tokenization/table_2_1.png" class="img-fluid rounded z-depth-1" alt="Original Table 2.1 listing vocabulary sizes, hidden dimensions, embedding and output parameter counts, total parameters, and embedding percentages for fifteen models grouped by family." caption="Table 2.1 from Tokenization: A Survey for Modern NLP, p. 10." zoomable=true %}

Table 2.1 of *Tokenization: A Survey for Modern NLP* supports a point made in Section 2.2: **the vocabulary can account for a large share of a model's parameter budget, especially in smaller models.** The table lists vocabulary sizes, hidden dimensions, parameter counts, and embedding percentages for fifteen models, grouped by family.

The percentage column contains the comparison we need, but **the reader has to assemble the picture**: scan fifteen rows, mentally rank the percentages, remember the gaps, and look back at model sizes to interpret them. Every entry has the same visual weight, whether it represents almost 60% of a model or less than 1%.

The redesign replaces the table with a graph that makes these differences visible directly.

## The redesign

I focus on one question: **How much of each model's parameter budget goes to the embedding and output layers?** The bars show the paper's reported percentages on a shared axis starting at zero, sorted from largest to smallest. Model names stay horizontal, and colors keep families recognizable after sorting.

<style>
.tokenization-parameter-chart {
  overflow-x: auto;
}
.tokenization-parameter-chart pre {
  min-width: 640px;
  margin: 0;
  padding: 0;
  background: transparent;
}
.tokenization-parameter-chart .language-chartjs {
  display: block;
  position: relative;
  height: 780px;
  padding: 0;
  white-space: normal;
}
</style>

<div class="tokenization-parameter-chart" markdown="1" role="region" aria-label="Embedding and output parameter shares for fifteen models" tabindex="0">

```chartjs
{
  "type": "bar",
  "data": {
    "labels": [
      [
        "Gemma 4 E2B† (4.65B)",
        "59.80%"
      ],
      [
        "Gemma 4 E4B† (7.52B)",
        "47.15%"
      ],
      [
        "Qwen3.5 0.8B† (0.77B)",
        "32.90%"
      ],
      [
        "Qwen3.5 2B† (1.94B)",
        "26.18%"
      ],
      [
        "Qwen3.5 9B (9.20B)",
        "22.12%"
      ],
      [
        "Qwen3.5 4B† (4.33B)",
        "14.69%"
      ],
      [
        "Ministral 3 8B (8.49B)",
        "12.65%"
      ],
      [
        "Ministral 3 3B† (3.43B)",
        "11.74%"
      ],
      [
        "Ministral 3 14B (13.51B)",
        "9.94%"
      ],
      [
        "Qwen3.5 27B (27.32B)",
        "9.31%"
      ],
      [
        "Gemma 4 12B† (11.94B)",
        "8.43%"
      ],
      [
        "gpt-oss-20b (20.91B)",
        "5.54%"
      ],
      [
        "Gemma 4 31B† (30.70B)",
        "4.59%"
      ],
      [
        "Mistral Medium 3.5 (125.03B)",
        "2.58%"
      ],
      [
        "gpt-oss-120b (116.83B)",
        "0.99%"
      ]
    ],
    "datasets": [
      {
        "label": "Gemma 4 (|V| = 262k)",
        "data": [
          59.8,
          47.15,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          8.43,
          null,
          4.59,
          null,
          null
        ],
        "backgroundColor": "#2f80df",
        "grouped": false,
        "barPercentage": 0.8,
        "categoryPercentage": 0.9
      },
      {
        "label": "Qwen3.5 (|V| = 248k)",
        "data": [
          null,
          null,
          32.9,
          26.18,
          22.12,
          14.69,
          null,
          null,
          null,
          9.31,
          null,
          null,
          null,
          null,
          null
        ],
        "backgroundColor": "#9843a5",
        "grouped": false,
        "barPercentage": 0.8,
        "categoryPercentage": 0.9
      },
      {
        "label": "Mistral / Ministral (|V| = 131k)",
        "data": [
          null,
          null,
          null,
          null,
          null,
          null,
          12.65,
          11.74,
          9.94,
          null,
          null,
          null,
          null,
          2.58,
          null
        ],
        "backgroundColor": "#f58a0b",
        "grouped": false,
        "barPercentage": 0.8,
        "categoryPercentage": 0.9
      },
      {
        "label": "gpt-oss (|V| = 201k)",
        "data": [
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          null,
          5.54,
          null,
          null,
          0.99
        ],
        "backgroundColor": "#29a39f",
        "grouped": false,
        "barPercentage": 0.8,
        "categoryPercentage": 0.9
      }
    ]
  },
  "options": {
    "indexAxis": "y",
    "responsive": true,
    "maintainAspectRatio": false,
    "plugins": {
      "title": {
        "display": true,
        "text": "Embedding and output layers as a share of total parameters"
      },
      "legend": {
        "position": "bottom",
        "labels": {
          "boxWidth": 16,
          "padding": 16
        }
      },
      "tooltip": {
        "enabled": true
      }
    },
    "scales": {
      "x": {
        "min": 0,
        "max": 70,
        "ticks": {
          "stepSize": 10
        },
        "title": {
          "display": true,
          "text": "Embedding and output parameters (% of total)"
        }
      },
      "y": {
        "grid": {
          "display": false
        },
        "ticks": {
          "autoSkip": false,
          "font": {
            "size": 12
          }
        }
      }
    }
  }
}
```

</div>

*Parentheses give total parameters in billions. † denotes tied embeddings: the input and output layers share parameters. The legend gives each family's vocabulary size. Hover or tap a bar for its value; click a family in the legend to hide or show it. On narrow screens, scroll horizontally.*

## What the graph makes easier to see

- **Differences are visible at a glance.** Bar lengths let readers see how much the parameter shares differ without mentally comparing a column of numbers. Sorting makes the ranking clear and helps both large gaps and small differences stand out.
- **Colors make comparisons easier.** Models from the same family share a color, so readers can quickly find related models even when sorting places them apart. This makes it easier to compare models within a family and see how families compare with one another.

## Design decisions

- **Sort by percentage.** Readers can find the extremes and follow the ranking without constructing it themselves.
- **Focus on one metric.** Leaving out hidden dimensions and absolute embedding counts allows the users to focus on what's important.
- **Preserve family context with color.** Consistent colors reconnect related models after sorting.

A smaller share in this graph means fewer parameters allocated to these layers relative to the model's total; it does not by itself establish better model quality.

Data: Table 2.1, p. 10, shown above.
