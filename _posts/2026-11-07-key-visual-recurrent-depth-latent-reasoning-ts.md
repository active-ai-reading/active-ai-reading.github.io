---
title: "Visualizing a core idea"
description: Do the recurrent iterations stand for reasoning?
paper: recurrent-depth-latent-reasoning
role: visualization
task: key-visual
by: [TalSokolov]
chart:
  chartjs: true # enables ```chartjs code blocks. Also available: echarts, plotly, vega_lite (see the showcase)
---

Throughout the paper, the authors frame depth recurrence as a mechanism for implicit latent reasoning.
Computational depth should then reflect the complexity of the required reasoning, rather than improving accuracy.

This is reflected in their design choices: 
* Training data - composed of relatively heavy reasoning domains.
* Training mechanisms - randomizing the depth, decoupling it from the direct accuracy metrics. 

Here I visualize 3 points from the paper emphasizing the depth as a reasoning mechanism:


## 1. "the recurrent model outperforms its baseline with an especially pronounced advantage on harder tasks"
### (5.3 Where does recurrence help most?)

Figure 7 shows that tasks that require more reasoning take more iterations to saturate the performance.
Tables 1 and 4 include similar relevant evaluations that can be visualised in a similar plot:

<img width="790" height="740" alt="relative_comparison_plot" src="https://github.com/user-attachments/assets/9247b892-7efe-4196-924e-8214d1a1123b" />
Blue shades are simple tasks, and green shades are tasks requiring more reasoning.
Reading the text, I was expecting the trends to show a later convergence for reasoning demanding tasks than the simple ones, but this is not as convincing.

## 2. "when more context is given, the model can reason about more information in context,..., mirroring generalization improvements shown for recurrence"
### (Recurrence and Context)

In Figure 9 they show that as the model gets more shots (examples of the task), the accuracy saturates later, maybe indicating the model uses the examples as part of a complex reasoning. 
Table 4 compares closed book to open book tasks, in a similar context of open book allowing the preference reasoning over memorization.

<img width="3867" height="2968" alt="closed_vs_open_with_difference" src="https://github.com/user-attachments/assets/97c97533-08e0-4e85-bc53-99af121e22ce" />
Score shows performance (%). The model improves in an open-book scenario, showing similar improvement to other open source models.

## 3. "...the model exiting earlier on high school mathematics, but taking on average 3.5 steps more on moral scenarios"
### (6.1. Zero-Shot Adaptive Compute at Test-Time)

Using the model for adaptive compute, they use a convergence metric to allow early exit.
The idea is that simpler tasks, that require less reasoning, should converge and exit earlier.
Figure 10 shows the distribution of steps to exit on different tasks, where simple tasks like high school math exit earlier than heavy reasoning tasks like moral scenarios.

Focusing on the peak of the density functions, it's simpler to see that Continuous Chain-of-Thought (6.3) has little contribution, 
but the effect of the task domain is clear.
<img width="3245" height="1767" alt="early_exit" src="https://github.com/user-attachments/assets/9d62da12-a356-479d-af3f-cabee0920a8f" />
