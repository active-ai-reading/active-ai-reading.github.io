---
title: "A better Figure 3"
description: A schematic of the three phases of finetuning, with and without normalization, showing where the old and the new facts land and which ones are answered.
paper: spurious-forgetting
role: visualization
task: redo-graph
by: yak0v
og_image: /assets/img/posts/spurious-forgetting-phases/phases.png
---

{% include figure.liquid path="assets/img/posts/spurious-forgetting-phases/phases.png" class="img-fluid rounded" caption="Old facts (circles) and new facts (triangles) during finetuning. Blue marks a fact that is answered, orange a fact that is not. Hollow shapes mark where each fact has to be to be answered. Schematic, the counts are illustrative." %}

## How to read it

Each hidden state is drawn in two dimensions. The horizontal position is the shared direction, which decides whether the old answers or the new answers win. The vertical position is the fact's own part, which picks its answer within that region. A fact is answered when it sits on its own spot.

## The three phases

Before finetuning, the old facts sit on their spots and the new facts are unknown.

In the collapse, the new facts all answer in the same region, so their errors agree and add up to one push that moves every hidden state the same way. The old facts are carried into the wrong region together. Some new facts already reach their spots.

In the recovery, each new fact learns its own part. With normalization the length of every hidden state is fixed, so a long shared shift leaves less room for the own parts. Once the new facts depend on their own parts, the shift is pulled back and most old facts return to their region. Without normalization nothing pulls the shift back, and the old facts stay out.

In the erosion, single old facts drift off their own spots. This slow loss is specific to each fact and is the part of the forgetting that does not come back.

The old facts were never erased. During the collapse they moved as one group and kept their own parts, which is why the recovery needs no replay of old data.
