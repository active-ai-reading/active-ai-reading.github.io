---
title: "A better Figure 1"
description: removing redundancy.
paper: spurious-forgetting
task: redo-graph
by: AdamJaber03
chart:
  chartjs: true # enables ```chartjs code blocks. Also available: echarts, plotly, vega_lite (see the showcase)
---

## The original

<img width="1632" height="427" alt="image" src="https://github.com/user-attachments/assets/64e5b870-814e-47dd-aa71-c4d9273d18c5" />


## The redesign

<img width="1895" height="788" alt="spurious_forgetting_fig" src="https://github.com/user-attachments/assets/9522e717-4937-4857-95ed-69702bb04bd3" />

## What changed and why

In the original figure, the scenario where you fine-tune on C, which is derived from both A and B, is treated separately from fine-tuning on B`. I find this to be redundant, as if we choose A to be the empty set, we get the same thing. Moreover, the current design results in a very boring right side of the figure. I drop this and focus on the main effect in the left side figure.


By removing C we can get rid of the part in the middle as B` being derived from B is intuitive enough.

Removed the B` line; found it to be unnecessary to convey the forgetting dynamics.

Added a small faded area explaining that the model has already been trained on A and B but this is not the focus.

Since the lines are simple, having the A and B letters on them rather than a legend looks better to me

The erosion effect is shared between the two lines, and so having it labeled on the A line seemed confusing; removed it.
