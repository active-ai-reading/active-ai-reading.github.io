---
title: "Writing about the points that matter."
description: One sentence that makes people want to click.
paper: matryoshka-lm-suites # the filename of the paper in _papers/, without .md
role: writing
task: key-points # abstract | copyedit | key-points   (see the roles page)
by: [NathanAdda]
---

<!-- Keep the sections that fit your task, delete the rest. -->

For key-points: list the 3 points most readers should leave with, where the paper currently says them, and how they could be emphasized better (title? figure 1? first sentence of the intro?).

## Point 1 - The Matryoshka architecture and how it is built.
The main contribution of the paper is a new approach to creating language model suites. Instead of training multiple independent models of different sizes, the authors introduce the Matryoshka architecture, in which smaller sub-models are nested within larger ones, sharing parameters while retaining their own widths, depths, and the ability to be deployed independently.

In their experiments, the authors construct a suite of three models of increasing sizes (500M, 1.5B, and 3B parameters). The 1.5B model builds upon the 500M model by reusing its Transformer layers and adding new layers with additional parameters. Similarly, the 3B model contains the 1.5B model and extends it with further layers. This means that all three models are part of a single nested architecture, allowing them to be trained jointly in one training run, rather than training each model separately.

### Where is this point currently emphasized?

The main idea is introduced in the abstract, which provides a clear and concise explanation of the nested architecture while also highlighting its advantages, such as reducing the total parameter count of the suite.

The introduction further develops this idea, particularly in the first paragraph of page 2, where the authors explain how larger models are built by adding parameters to smaller ones, rather than training each model independently.

Figure 1a also illustrates the nested architecture, showing the different sub-model sizes and their outputs.

Finally, Section 2 (Method) provides a more mathematical explanation of the architecture, introducing the parameter nesting relationship and the inter-model junction mechanism that allows sub-models with different hidden dimensions to be connected.

### How could this point be emphasized better?

Although the abstract and introduction communicate the main idea effectively, I think Figure 1a could be improved to make the architecture easier to understand at first glance.

One possibility would be to show a side-by-side comparison between a traditional suite, consisting of three independent models, and a Matryoshka suite. The Matryoshka diagram could explicitly display the Transformer layers belonging to each sub-model, how their outputs are passed to the next stage, and where each sub-model produces its predictions. This would make the parameter sharing and nesting structure more intuitive.

Additionally, the explanation of the inter-model junction in Section 2 could be clearer about where the fresh input embeddings come from. In particular, the authors could explicitly state that these embeddings are obtained from the original input tokens using learned embedding parameters, and that they provide the additional dimensions needed by the next sub-model. A small diagram illustrating this process could make the mechanism easier to follow.

## Point 2 - More efficient speculative decoding

Another important contribution of the paper is improving speculative decoding efficiency. Because the smaller sub-models (used as drafts) and the larger model (used as the verifier) share parameters and are part of the same architecture, they can be jointly trained using knowledge distillation. This encourages the draft and verifier to produce more similar predictions.

This improved agreement allows the verifier to accept more draft tokens, making text generation faster. Additionally, since the draft model is nested within the verifier, they can share their KV cache instead of maintaining separate caches, reducing memory overhead and redundant computation. Together, these advantages lead to higher throughput, with the authors reporting a 26% improvement compared to Vanilla speculative decoding in one experimental configuration.

### Where is this point currently emphasized?

It is briefly mentionned in the abstract, where it is said that they improved the througput by 14-26%.
Also in the introduction where they reference this improvement and in Section 2 where they go more into detail about how the shared parameters, the KV cache sharing and the improved agreement between draft and verifier improve speculative decoding efficiency. With Fig 4 and 5 that shows the improvements.

### How could this point be emphasized better?

I think the graphs from Figure 4 really show well the improvement done in a good way, by showing the token-level agreement (Fig 4.c) and graphs in Fig 5 that represent the accepted length from the draft proposal with two different methods greedy and nucleus.
Generally, I think the authors explained well how it improved speculative decoding and showed relevant figures.
However, they could help the reader link between Figures 4 and 5 to understand more easily how improved agreement leads to higher acceptance rates and ultimately contributes to higher throughput.

## Point 3 - More efficient training while maintaining performance

One other important contribution from this paper is that while training this Matryoshka suite they succeeded in maintaining the performance compared to models trained independently while reducing training costs by 36%.
Because the sub-models are nested in the bigger models and share parameters, they can be trained at the same time in one pass instead of training each model separately.
There is a difference in performance of a maximum of 0.5% for each model size in average benchmark accuracy.

### Where is this point currently emphasized?

It is mentionned in the abstract, where they mentionned the 36% reduction in training compute while keeping the performance.
There is also a graph in Figure 1b showing the 36% improvement, and in section 3 with table 2 and figure 3 that shows that they achieve almost the same perplexity and accuracy while needing less training compute.

### How could this point be emphasized better?

I think the authors emphasized the contributions in a good way. With Figure 1.b showing us the 36% reduction in training compute while keeping same level validation perplexity. And on top of that, Table 2 and Figure 2 gives us evidence that Matryoshka achieves similar performance with less training compute.

## The general rule

What rule did you apply that others could use in their own writing? (e.g. "Lead with the finding, not the method.")

I think diving deep in the paper and really taking the time to read it and understand the most you can in the time given is 80% of the work, then going over what you noted to yourself during the reading to see what maybe seemed more important to you during reading.

<!-- For key-points: list the 3 points most readers should leave with, where the paper currently says them, and how they could be emphasized better (title? figure 1? first sentence of the intro?). -->
