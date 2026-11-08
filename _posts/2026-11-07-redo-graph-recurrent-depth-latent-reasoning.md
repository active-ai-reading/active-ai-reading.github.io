---
title: "A better Figure <N>"
description: What the new figure makes obvious that the old one didn't.
paper: recurrent-depth-latent-reasoning
role: visualization
task: redo-graph
by: sprinzak
chart:
  chartjs: true # enables ```chartjs code blocks. Also available: echarts, plotly, vega_lite (see the showcase)
---

## The original

[Figure 5 of Geiping et al.'s *Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach*](https://arxiv.org/pdf/2502.05171v2#page=6) compares three training runs of the 3.5B recurrent-depth model: two failed attempts ("Bad Run 1" and "Bad Run 2") and the final run ("Main"). It has three plots side by side:

- **Left:** training loss.
- **Middle:** the correlation of hidden states across the tokens of a sequence. A value of 1.0 means every token has the same hidden state, so the representation has collapsed.
- **Right:** validation perplexity, measured at 1, 4, 8, 16, 32 and 64 test-time recurrences.

The point of the figure is in the text of the paper, not in the figure itself:

- Bad Run 1 collapses right away and stalls.
- Bad Run 2 recovers from the collapse, but learns to ignore the recurrent state, so more recurrences don't help.
- The Main run never collapses and keeps improving with more recurrences.

The right plot is the hardest to read. It has 3 runs × 6 recurrence depths = 18 lines, and the depths are told apart only by line style. Because the lines of the failed runs lie on top of each other, the reader has to trust the caption that they overlap.

## The redesign

![Redrawn Figure 5 with one validation-perplexity panel per training run.](/assets/img/posts/recurrent-depth-figure5/fig5-redo.png)

*(a) Training loss. (b) Hidden-state correlation; the bold line is a 15-point moving average of the raw curve (faint). (c) Validation perplexity for 1 to 64 recurrences; thick coloured line = 1 recurrence, thin dark lines = 4 to 64.*

*A scalable version is also available: [open the SVG](/assets/img/posts/recurrent-depth-figure5/fig5-redo.svg).*

The right plot is now three small plots, one per run, and run names are written next to the curves instead of in a legend. In each small plot the 1-recurrence line is thick and the 4 to 64 recurrence lines are thin, dark, and drawn on top of it.

## What changed and why

- **One panel per run in the right plot.** This is the important change. When the thin lines sit exactly on the thick one, you can see that extra recurrences do nothing. This is the case for both failed runs. In the Main run the lines split: at the end of training 1 recurrence gives a perplexity of about 89 and 16 recurrences give about 7.7, roughly 11× lower. From 8 recurrences on the curves are nearly identical.
- **Direct labels instead of a legend.** Each run keeps the same colour in all three plots, and its name is written next to its curve.
- **A dashed ρ = 1 line in the hidden-state plot.** It marks total collapse. Bad Run 1 sits on it for its whole life. Bad Run 2 stays on it for about 160 steps and then drops.
- **Smoothing in the hidden-state plot.** The raw curves are very noisy, so the bold line is a 15-point moving average and the faint line is the raw data. The original does not smooth this plot. The raw curve also shows a short spike to about 0.89 around step 8 in the Main run, which the average flattens out.
- **Smaller changes.** Plain tick labels (10, 100, 1000) instead of exponents on the y-axes, a colourblind-safe palette, and almost no text on the plot itself.

The important change is the first one. The original makes the reader work out from 18 lines that the failed runs gain nothing from recurrence, while the redesign shows it at a glance.

## Caveats

- The data was read from the vector graphics in the paper's PDF (calibrated against the axis ticks), not re-run. It is as accurate as what the paper shows.
- The curves end at about step 7,300, although the original caption says the plot covers the first 10,000 steps.
- In the original, Bad Run 1's correlation is a flat line at 1.0, and it is redrawn that way.

