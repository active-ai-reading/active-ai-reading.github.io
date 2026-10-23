---
title: "Visualizing the core idea of Matryoshka LM Suites"
description: "One figure that shows how three separate models become one nested model, and where the savings come from."
paper: matryoshka-lm-suites
role: visualization
task: key-visual
by: [Tomeratia]
---

## Core idea:

The core idea of the paper ([Godey and Artzi, 2026](https://arxiv.org/abs/2608.09703)) is explained in Section 2 and in Figure 1(a). Usually, a model suite (here 500M, 1.5B and 3B parameters) is trained as separate models. The paper nests the small models inside the large one and trains all of them together in a single run.

The idea is spread over three places. The structure (what is shared) is in the text of Section 2. The mechanism that connects the sub-models, the junction, appears only in Equation 1. The numbers behind the savings are in Table 1. A new reader has to combine all three to understand why this works and why it is cheaper.

## The figure:

<img width="1672" height="940" alt="figure" src="https://github.com/user-attachments/assets/23d3ce80-27f6-4e68-b42c-fd6f0df2ca3e" />


**How to read it.**

- **Left panel:** a standard suite. Three independent models, each with its own embedding and LM head, trained in three separate runs. The total is 5.2B parameters.
- **Right panel:** a Matryoshka suite. One stack of three blocks (24, +10 and +5 layers). The blue block is exactly the 500M model. Blue plus orange is the 1.5B model. All three blocks together are the 3B model. Each sub-model has its own LM head, so it can be detached and used alone. The total is 3.2B parameters (Table 1 of the paper).
- **Bottom panel:** the junction. The output of sub-model m is rescaled to match the norm of the new token embedding, and then it is concatenated with that embedding. The embedding fills the extra channels that the wider sub-model m+1 needs. This adds no new parameters. In the paper's ablation at 200M scale, removing the rescaling costs about 0.2 validation perplexity, and filling the new channels with zeros costs about 0.54.

The figure shows the parameter count: 3.2B instead of 5.2B (about 38% fewer). The paper's "36% less training compute" is a separate measurement of training cost, so the two numbers are close but not the same.
