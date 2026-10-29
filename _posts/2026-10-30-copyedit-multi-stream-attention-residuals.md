---
title: "Making the MSAR methods section easier to follow"
description: A table of operations and dimensions helps readers follow the architecture without losing track.
paper: multi-stream-attention-residuals
role: writing
task: copyedit
by: [NicolasRW]
---
## What I changed and why

I propose adding a table of operations and dimensions to the methods section to help readers trace the computation

MSAR involves contextual expansions that combine token positions, depth attention that combines earlier sources, and stream fusion that combines the retrieved views. Following these operations requires keeping track of what each index refers to and what shape each intermediate representation has.

Figure 2 shows the overall scheme, but it does not provide all the information needed to follow each transformation. A table showing the operations alongside their input and output dimensions makes the computation easier to follow.

I also write operations directly, avoiding additional symbols such as $E_{i,r}$, $\phi$, $q_l^{(r)}$, and $k_i^{(r)}$, because I think this makes it easier to keep track of each term.

## Before and after

**Before**

> The expanded streams serve as distinct depth-attention heads, each associated with a different contextual scale. For each target layer, we perform depth attention independently within each stream, aggregating the corresponding source representations across depth:

The retrieval is then defined in Eqs. (11)–(12). The next subsection begins:

> The retrieved streams $Z_l$ must be fused into a single input for the target layer.

Equations (13)–(14) define that fusion. The proposed addition brings these steps, together with source expansion, into one view.

**After**

Add the following table:

### MSAR architecture

Token index $t$ is omitted except where neighboring positions are explicitly used.

| Stage | Operation | Input shape(s) | Output shape |
|---|---|---|---|
| **Collect sources** | $v_0=h_1$<br>$v_i=f_i(h_i)$, $1\le i<l$ | $S$ vectors of size $d$ | $S\times d$ |
| **Expand sources** | $v_{i,t}^{(0)}=v_{i,t}$<br>$v_{i,t}^{(r)}=\sum_{\delta=0}^{\kappa_r-1}c_{i,r,\delta}\odot v_{i,t-\delta}$<br>$r=1,2,3$; $\kappa_r=4,8,12$ | Sources: $S\times d$<br>Each filter: $d$ | $S\times m\times d$ |
| **Score sources** | $s_i^{(r)}=(w_l^{(r)})^\top\mathrm{RMSNorm}(v_i^{(r)})$ | Keys: $S\times m\times d$<br>Queries: $m\times d$ | $S\times m$ |
| **Normalize over sources** | $\alpha_{i\to l}^{(r)}=\dfrac{\exp(s_i^{(r)})}{\sum_{j=0}^{l-1}\exp(s_j^{(r)})}$ | $S\times m$ | $S\times m$ |
| **Retrieve across depth** | $z_l^{(r)}=\sum_{i=0}^{l-1}\alpha_{i\to l}^{(r)}v_i^{(r)}$<br>Stack the $m$ vectors as rows of $Z_l$ | Values: $S\times m\times d$<br>Weights: $S\times m$ | $m\times d$ |
| **Flatten and normalize** | $u_l=\mathrm{RMSNorm}(\mathrm{Flatten}(Z_l))$ | $m\times d$ | $1\times(md)$ |
| **Compute gates** | Projection + scale + bias → sigmoid<br>Produces $H_l^{\mathrm{pre}}$ | $1\times(md)$ | $1\times m$ |
| **Form input** | $h_l=(H_l^{\mathrm{pre}}Z_l)^\top$ | $Z_l$: $m\times d$<br>$H_l^{\mathrm{pre}}$: $1\times m$ | $d$ |
| **Compute output** | $v_l=f_l(h_l)$ | $d$ per token | $d$ per token |

### Block MSAR
Use block summaries rather than individual layer outputs. To do so, partition consecutive layers into blocks $B_1,\ldots,B_N$.
For layer $l\in B_n$, use:
| Source | Definition | Shape per token |
|---|---|---|
| **Embedding** | $b_0=h_1$ | $d$ |
| **Completed blocks** | $b_j=\sum_{i\in B_j}v_i$<br>$j=1,\ldots,n-1$ | $d$ each |
| **Current partial** | $b_n^{<l}=\sum_{i\in B_n,\ i<l}v_i$ | $d$ |

Apply the same operations to these sources.

## The general rules

1. Explain operations alongside their dimensions. In this way, the reader can follow how one stage's output becomes the next stage's input.
2. Make the axis of the operation explicit, since we have token positions, depth, and streams 

