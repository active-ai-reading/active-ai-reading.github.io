---
title: "explaing HC and mHC"
description: Can Transformers Learn Better Residual Connections?
paper: multi-stream-attention-residuals
role: learning
task: teach
by: [matan2001]
---

this essay will focus on Understanding Hyper-Connections(HC), why they become unstable, and how mHC and MSAR approach the problem differently.

Residual connections are among the most important components of modern Transformers. They allow information to flow through deep networks while helping gradients propagate during training.

However, ordinary residual connections have a simple design: every layer adds its output to one running hidden representation.

in the paper we read, two options are mentioned in trying to adress this problem.

[Hyper-Connections (HC)](https://arxiv.org/abs/2409.19606) (Zhu et al., 2024) proposes maintaining multiple residual representations instead of one. [Manifold-Constrained Hyper-Connections (mHC)](https://arxiv.org/abs/2512.24880) (Xie et al., 2025) improves this design by constraining how those representations interact, making training more stable.

To understand the differences, let's start with ordinary residual connections.

## The Problem With a Single Residual Stream

In a standard Transformer, each attention or MLP layer receives a hidden representation, performs a computation, and adds the result to its input.

We can write this as:

$$
h_{\ell+1}=h_\ell+f_\ell(h_\ell)
$$

Here, $h_\ell$ is the current hidden representation, while $f_\ell(h_\ell)$ is the new information produced by the layer.

If we expand the computation over several layers, the final representation becomes the initial representation plus all previous residual updates:

$$
h_L=h_0+\sum_{\ell=0}^{L-1}r_\ell
$$

where $r_\ell=f_\ell(h_\ell)$.

This design has an important advantage: information can travel through the network without having to pass through every nonlinear transformation.

But it also introduces a limitation. Every residual update is accumulated into the same vector.

A later layer receives this combined representation, rather than separately maintaining all the contributions that created it.

The original [Hyper-Connections paper](https://arxiv.org/abs/2409.19606) also discusses a related tradeoff between gradient propagation and representation similarity across deep layers. Standard PreNorm residual connections provide a strong gradient path, but successive hidden representations may become increasingly similar, limiting the benefit of additional depth.

This motivates a natural question:

**Instead of maintaining one residual representation, why not maintain several?**

## Hyper-Connections: Giving the Transformer Multiple Residual Streams

This is the central idea behind Hyper-Connections.

In an ordinary Transformer, each token carries one hidden representation of dimension $d$.

For example, if $d=1024$, every token has one vector containing 1,024 numbers at each layer.

HC introduces an expansion factor $n$.

If $n=4$, the model maintains four separate hidden vectors for each token:

- Stream 1: a 1024-dimensional vector.
- Stream 2: a 1024-dimensional vector.
- Stream 3: a 1024-dimensional vector.
- Stream 4: a 1024-dimensional vector.

Together, these form a residual state:

$$
X_\ell\in\mathbb R^{4\times1024}
$$

Importantly, this does **not** mean there are four separate Transformers. The attention or MLP computation still operates on one vector of the original hidden dimension.

Instead, HC learns how to read information from its four streams, process it, and distribute the result back into those streams.

### How Does One HC Layer Work?

Let's examine an example with four residual streams and a hidden dimension of 1024.

The current residual state is:

$$
X=
\begin{bmatrix}
x_1\\
x_2\\
x_3\\
x_4
\end{bmatrix}
$$

where every $x_i\in\mathbb R^{1\times1024}$.

Therefore:

$$
X\in\mathbb R^{4\times1024}
$$

The dimensions of all the variables are:

| Variable | Dimensions | Meaning |
|---|---|---|
| $X$ | $4\times1024$ | Four residual streams |
| $H^{\mathrm{pre}}$ | $1\times4$ | Reads from the streams |
| $h$ | $1\times1024$ | Input to the Transformer layer |
| $r=f(h)$ | $1\times1024$ | New residual update |
| $H^{\mathrm{res}}$ | $4\times4$ | Mixes the existing streams |
| $H^{\mathrm{post}}$ | $4\times1$ | Distributes the new update |
| $X_{\mathrm{next}}$ | $4\times1024$ | Updated residual streams |

These dimensions refer to one token position, omitting the batch and sequence dimensions.

Every HC layer performs three operations.

### Step 1: Read From the Streams

The model first combines the four streams into one input for the next Transformer computation.

Suppose the learned pre-mapping is:

$$
H^{\mathrm{pre}}=
\begin{bmatrix}
0.4&0.3&0.2&0.1
\end{bmatrix}
$$

This is a $1\times4$ matrix.

The input is calculated by:

$$
h=H^{\mathrm{pre}}X
$$

Checking dimensions:

$$
(1\times4)(4\times1024)=(1\times1024)
$$

The resulting vector is:

$$
h=0.4x_1+0.3x_2+0.2x_3+0.1x_4
$$

For a concrete numerical example, suppose the first coordinate of the four streams is:

$$
\begin{aligned}
x_1[1]&=2\\
x_2[1]&=6\\
x_3[1]&=4\\
x_4[1]&=8
\end{aligned}
$$

Then the first coordinate of the resulting input is:

$$
\begin{aligned}
h[1]
&=0.4(2)+0.3(6)+0.2(4)+0.1(8)\\
&=4.2
\end{aligned}
$$

The same weighted combination is applied to each of the other 1023 coordinates.

The resulting input $h$ is a complete 1024-dimensional vector.

The coefficients are controlled by the **pre-mapping**, denoted by $H^{\mathrm{pre}}$.

Rather than accepting one fixed running residual representation, each layer can learn which combination of the four streams it should process.

### Step 2: Apply the Transformer Computation

The layer now processes $h$ using its ordinary attention or MLP operation.

$$
r=f(h)
$$

Since $h$ has dimensions $1\times1024$, the residual update $r$ also has dimensions $1\times1024$.

Suppose, for our numerical example, the first coordinate of the update is:

$$
r[1]=10
$$

The other 1023 coordinates also contain values produced by the Transformer layer.

Notice that the actual Transformer computation has not fundamentally changed. We have only changed how its input was constructed.

### Step 3: Mix the Existing Streams and Write the New Information

HC now updates its four residual streams using two operations.

**First, mix information between the existing streams.**

Suppose the learned residual mixing matrix is:

$$
H^{\mathrm{res}}=
\begin{bmatrix}
0.8&0.2&0&0\\
0.3&0.7&0&0\\
0&0&0.9&0.1\\
0.1&0&0.2&0.7
\end{bmatrix}
$$

This matrix has dimensions $4\times4$.

The mixing operation is:

$$
X_{\mathrm{mixed}}=H^{\mathrm{res}}X
$$

Checking dimensions:

$$
(4\times4)(4\times1024)=(4\times1024)
$$

Using the first coordinate of each stream, the mixed values are:

$$
\begin{aligned}
\widetilde{x}_1[1]&=0.8(2)+0.2(6)=2.8\\
\widetilde{x}_2[1]&=0.3(2)+0.7(6)=4.8\\
\widetilde{x}_3[1]&=0.9(4)+0.1(8)=4.4\\
\widetilde{x}_4[1]&=0.1(2)+0.2(4)+0.7(8)=6.6
\end{aligned}
$$

This process happens across all 1024 coordinates.

**Second, distribute the new residual update into the streams.**

Suppose the post-mapping is:

$$
H^{\mathrm{post}}=
\begin{bmatrix}
0.1\\
0.2\\
0.3\\
0.4
\end{bmatrix}
$$

This is a $4\times1$ matrix.

The write operation is:

$$
H^{\mathrm{post}}r
$$

Checking dimensions:

$$
(4\times1)(1\times1024)=(4\times1024)
$$

So the resulting update can be added to the four existing streams.

For our first-coordinate example, where $r[1]=10$:

$$
\begin{aligned}
x_{1,\mathrm{new}}[1]&=2.8+0.1(10)=3.8\\
x_{2,\mathrm{new}}[1]&=4.8+0.2(10)=6.8\\
x_{3,\mathrm{new}}[1]&=4.4+0.3(10)=7.4\\
x_{4,\mathrm{new}}[1]&=6.6+0.4(10)=10.6
\end{aligned}
$$

The next Transformer layer receives four updated vectors, each containing 1024 values.

**This cycle repeats throughout the network.**

### What Has HC Actually Changed?

We can summarize the complete computation using three equations:

$$
h=H^{\mathrm{pre}}X
$$

$$
r=f(h)
$$

$$
X_{\mathrm{next}}
=H^{\mathrm{res}}X+H^{\mathrm{post}}r
$$

Here:

- **$H^{\mathrm{pre}}$** determines how the layer reads from the streams.
- **$H^{\mathrm{res}}$** determines how the existing streams exchange information.
- **$H^{\mathrm{post}}$** determines how the new layer output is written into the streams.

These mappings are learnable. HC includes both static variants, whose routing coefficients are learned but input-independent, and dynamic variants, whose coefficients also depend on the current representations.

This is a substantial change from ordinary residual connections, where the residual update is always added with coefficient one.

The result is that different streams can develop different representations, and each layer can use them differently.

There is also an important limitation: the streams are **continuously evolving memories**, not separate copies of individual historical layers. Information from earlier layers becomes incorporated into the current streams as they are repeatedly updated.

## Why Can HC Become Unstable?

The flexibility of HC comes at a cost.

The main difficulty lies in $H^{\mathrm{res}}$, the matrix responsible for mixing the residual streams.

Recall that HC updates its state using:

$$
X_{\mathrm{next}}
=H^{\mathrm{res}}X+H^{\mathrm{post}}r
$$

Let's temporarily ignore the new layer output and examine only the residual mixing operation:

$$
X_{\mathrm{next}}=H^{\mathrm{res}}X
$$

Suppose the matrix is:

$$
H^{\mathrm{res}}=
\begin{bmatrix}
1.2&0&0&0\\
0&0.8&0&0\\
0&0&1&0\\
0&0&0&1
\end{bmatrix}
$$

This is a $4\times4$ diagonal matrix.

It means the first stream is multiplied by 1.2, the second by 0.8, while the other two remain unchanged.

After one layer, those factors are relatively small.

But after 20 layers, assuming the same matrix is repeatedly applied:

$$
(H^{\mathrm{res}})^{20}=
\begin{bmatrix}
1.2^{20}&0&0&0\\
0&0.8^{20}&0&0\\
0&0&1&0\\
0&0&0&1
\end{bmatrix}
$$

- The first stream is multiplied by $1.2^{20}\approx38.3$.
- The second stream is multiplied by $0.8^{20}\approx0.012$.
- The third and fourth streams are unchanged by this mixing operation.

One stream has been amplified dramatically, while another has almost disappeared.

In actual HC models, the matrices are more complicated and can differ across layers and inputs. Nevertheless, the same underlying problem exists: **repeated multiplication by unconstrained matrices can cause signals and gradients to grow or shrink excessively.**

In the [mHC paper](https://arxiv.org/abs/2512.24880), the authors report this kind of instability in large-scale HC training. Their experiments show loss and gradient-norm instabilities associated with strong amplification through the residual mixing path.

So we face a tradeoff.

HC gives the model more flexibility, but the unconstrained connections between streams can make deep networks difficult to train.

Can we preserve the multiple streams while making their interactions safer?

## mHC: Constraining How Streams Interact

This motivates **Manifold-Constrained Hyper-Connections**, introduced by [DeepSeek](https://arxiv.org/abs/2512.24880).

mHC retains the central HC architecture:

- Multiple persistent residual streams.
- Learned read mappings.
- Learned write mappings.
- Learned mixing between streams.

The crucial difference is that **mHC constrains the residual mixing matrix $H^{\mathrm{res}}$**.

Instead of allowing arbitrary matrix entries, mHC requires $H^{\mathrm{res}}$ to be approximately *doubly stochastic*.

A doubly stochastic matrix satisfies three conditions:

1. Every entry is nonnegative.
2. Every row sums to one.
3. Every column sums to one.

Mathematically, for a matrix $P\in\mathbb R^{n\times n}$:

$$
P_{ij}\geq0
$$

$$
\sum_{j=1}^{n}P_{ij}=1
\qquad\text{for every }i
$$

$$
\sum_{i=1}^{n}P_{ij}=1
\qquad\text{for every }j
$$

For example, with four streams, consider:

$$
H^{\mathrm{res}}=
\begin{bmatrix}
0.8&0.2&0&0\\
0.2&0.8&0&0\\
0&0&0.75&0.25\\
0&0&0.25&0.75
\end{bmatrix}
$$

This is a valid $4\times4$ doubly stochastic matrix.

### Why Does This Help?

Consider the first coordinate of our four original streams:

$$
\begin{bmatrix}
2\\
6\\
4\\
8
\end{bmatrix}
$$

Applying the new mixing matrix gives:

$$
\begin{aligned}
\widetilde{x}_1[1]&=0.8(2)+0.2(6)=2.8\\
\widetilde{x}_2[1]&=0.2(2)+0.8(6)=5.2\\
\widetilde{x}_3[1]&=0.75(4)+0.25(8)=5\\
\widetilde{x}_4[1]&=0.25(4)+0.75(8)=7
\end{aligned}
$$

Notice what happened.

Each new stream is a weighted average of the previous streams.

More importantly, their combined value is preserved:

$$
2.8+5.2+5+7=20
$$

which equals the original sum:

$$
2+6+4+8=20
$$

The same preservation property holds for all 1024 coordinates, because the mixing matrix acts identically across the hidden dimension.

The streams are allowed to exchange information, but the mixing operation preserves their sum and therefore their average.

This is fundamentally different from unconstrained HC, where arbitrary coefficients could amplify the total signal.

### The Mathematical Advantage

A doubly stochastic matrix has spectral norm at most one:

$$
\boxed{\left\|H^{\mathrm{res}}\right\|_2\leq1}
$$

In other words, the residual mixing operation cannot increase the Frobenius norm of the stored state:

$$
\left\|H^{\mathrm{res}}X\right\|_F
\leq
\left\|X\right\|_F
$$

This property is also preserved when several exactly doubly stochastic matrices are multiplied together:

$$
\left\|
H_L^{\mathrm{res}}
H_{L-1}^{\mathrm{res}}
\cdots
H_1^{\mathrm{res}}
\right\|_2
\leq1
$$

Consequently, mHC can maintain controlled signal propagation through many residual-mixing operations.

Importantly, this does not mean that each stream remains unchanged or that information cannot be lost. Mixing can still make streams increasingly similar.

It also does not guarantee that every part of the neural network is stable. The attention, MLP, and write-back operations can still affect signal magnitude.

The guarantee concerns the residual mixing path.

### How Does mHC Enforce the Constraint?

The model cannot simply learn an arbitrary matrix and hope that it becomes doubly stochastic.

Instead, it uses the **Sinkhorn–Knopp algorithm**.

The procedure starts with learned matrix scores and repeatedly normalizes the rows and columns.

First, the scores are exponentiated to make their entries positive.

Then:

- Normalize the rows so each sums to one.
- Normalize the columns so each sums to one.
- Repeat the process.

The [mHC paper](https://arxiv.org/abs/2512.24880) uses 20 iterations as a practical approximation.

The resulting matrix is approximately doubly stochastic.

mHC also applies nonnegativity constraints to the read and write mappings, although those mappings do not have to be doubly stochastic themselves.

## How Is This Different From MSAR?

HC and mHC both maintain multiple residual streams that evolve across the entire Transformer.

[Attention Residuals (AttnRes)](https://arxiv.org/abs/2603.15031), introduced by the Kimi Team, takes a different approach. Instead of relying only on an evolving residual state, it gives each layer direct access to historical residual information through softmax attention over earlier layers or block summaries.

[MSAR](https://arxiv.org/abs/2610.13630) extends this mechanism to multiple retrieval streams.

It stores historical block summaries and constructs four contextual views using an identity transformation and causal convolutions of sizes 4, 8, and 12.

Each stream independently retrieves information from previous blocks using depth attention. The outputs are then fused into one representation for the next Transformer computation.

The most important difference is that **MSAR's multiple streams are temporary, while HC and mHC maintain persistent streams**.

| Property | HC | mHC | MSAR |
|---|---|---|---|
| Main idea | Multiple evolving residual states | Stable multiple evolving states | Retrieve historical residual information |
| Persistent streams | Multiple | Multiple | Single representation per stored source |
| Information exchange | Learned stream mixing | Constrained stream mixing | Depth attention |
| Stability mechanism | Unconstrained | Doubly stochastic residual matrix | Softmax retrieval |
| Contextual convolutions | No | No | Yes |
| Historical layer access | Indirect through current streams | Indirect through current streams | Explicit through stored block summaries |

This means the architectures make different choices about where to spend their resources.

HC and mHC increase the capacity of the information carried forward through the network.

MSAR instead retains information about earlier computations and increases the flexibility of retrieving it.

## References

1. **Zhu, D., et al. (2024).** *Hyper-Connections.* arXiv:2409.19606. [https://arxiv.org/abs/2409.19606](https://arxiv.org/abs/2409.19606)

2. **Xie, Z., et al. (2025).** *mHC: Manifold-Constrained Hyper-Connections.* arXiv:2512.24880. [https://arxiv.org/abs/2512.24880](https://arxiv.org/abs/2512.24880)
