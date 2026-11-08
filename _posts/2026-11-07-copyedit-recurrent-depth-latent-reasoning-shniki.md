---
title: "A Scalable Recurrent Architecture - Rewritten for Easier Understanding"
description: Rewriting the section 3.1 explaining the macro of the latent recurrent-depth model.
paper: recurrent-depth-latent-reasoning
role: writing
task: copyedit
by: [shniki]
---

## What I changed and why

The main problem I had with the original text was that it had many equations without an in-depth explanation of each. Making it the readers responsibility to cross-reference with the figure.

As for the structure of the text, I personally would prefer having the motivation prior to the actual architecture. This helps understanding the reasons for such architecture choices and creates a more natural reading flow. Furthermore I try to include subtitles and lists whenever is possible to avoid large text blobs.


## Before and after

<div class="before-after">
<script src="https://jsdelivr.net" id="MathJax-script" async></script>
    <div class="before"><span class="label">Before</span>
    <section id="section-3-1" class="paper-section">
    <h3>3.1. Macroscopic Design</h3>
    <p>
        The model is primarily structured around decoder-only transformer blocks (Vaswani et al., 2017; Radford et al., 2019). However these blocks are structured into three functional groups, the prelude \(P\), which embeds the input data into a latent space using multiple transformer layers, then the core recurrent block \(R\), which is the central unit of recurrent computation modifying states \(\mathbf{s} \in \mathbb{R}^{n \times h}\), and finally the coda \(C\), which un-embeds from latent space using several layers and also contains the prediction head of the model. The core block is set between the prelude and coda blocks, and by looping the core we can put an indefinite amount of verses in our song.
    </p> 
    <p>
        Given a number of recurrent iterations \(r\), and a sequence of input tokens \(\mathbf{x} \in V^{n}\) these groups are used in the following way to produce output probabilities \(\mathbf{p} \in \mathbb{R}^{n \times |V|}\)
    </p>
    <!-- Display Math Block -->
    <div class="math-block" style="text-align: center; margin: 1.5em 0;">
        \[
        \begin{aligned}
            \mathbf{e} &= P(\mathbf{x}) \\
            \mathbf{s}_0 &\sim \mathcal{N}(0, \sigma^2 \mathbf{I}_{n \cdot h}) \\
            \mathbf{s}_i &= R(\mathbf{e}, \mathbf{s}_{i-1}) \quad \text{for } i \in \{1, \dots, r\} \\
            \mathbf{p} &= C(\mathbf{s}_r)
        \end{aligned}
        \]
    </div>
    <p>
        where \(\sigma\) is some standard deviation for initializing the random state. This process is shown in Figure 2. Given an initial random state \(\mathbf{s}_0\), the model repeatedly applies the core block \(R\), which accepts the latent state \(\mathbf{s}_{i-1}\) and the embedded input \(\mathbf{e}\) and outputs a new latent state \(\mathbf{s}_i\). After finishing all iterations, the coda block processes the last state and produces the probabilities of the next token.
    </p>
    <p>
        This architecture is based on deep thinking literature, where it is shown that injecting the latent inputs \(\mathbf{e}\) in every step (Bansal et al., 2022) and initializing the latent vector with a random state stabilizes the recurrence and promotes convergence to a steady state independent of initialization, i.e. path independence (Anil et al., 2022).
    </p>
    <p>
        <strong>Motivation for this Design.</strong> This recurrent design is the minimal setup required to learn stable iterative operators. A good example is gradient descent of a function \(E(x, y)\), where \(x\) may be the variable of interest and \(y\) the data. Gradient descent on this function starts from an initial random state, here \(x_0\), and repeatedly applies a simple operation (the gradient of the function it optimizes), that depends on the previous state \(x_k\) and data \(y\). Note that we need to use \(y\) in every step to actually optimize our function. Similarly we repeatedly inject the data \(\mathbf{e}\) in our set-up in every step of the recurrence. If \(\mathbf{e}\) was provided only at the start, e.g. via \(\mathbf{s}_0 = \mathbf{e}\), then the iterative process would not be stable<sup>1</sup>, as its solution would depend only on its boundary conditions.
    </p>
    <p>
        The structure of using several layers to embed input tokens into a hidden latent space is based on empirical results analyzing standard fixed-depth transformers (Skean et al., 2024; Sun et al., 2024; Kaplan et al., 2024). This body of research shows that the initial and the end layers of LLMs are noticeably different, whereas middle layers are interchangeable and permutable. For example, Kaplan et al. (2024) show that within a few layers standard models already embed sub-word tokens into single concepts in latent space, on which the model then operates.
    </p>
    </section>
    </div>
    <div class="after"><span class="label">After</span>
    <h3>3.1. Macroscopic Design</h3>
    <p>
        The model suggests 3 new functional groups: prelude \(P\), the core recurrent block \(R\), and coda \(C\). While keeping the stucture primarily around decoder-only transformer blocks (Vaswani et al., 2017; Radford et al., 2019). The core block is set between the prelude and coda blocks. And by looping the core we can put an indefinite amount of "verses".
    </p>
    <h4>The idea behind the 3 groups.</h4> 
    <p>
        <ul>
            <li>
            \(P\), the <i>prelude</i>, embeds the input data into a latent space using multiple transformer layers.
            </li>
            <li>
            \(R\), the <i>core recurrent block</i>, is the central unit. It's responsible for recurrent computation modifying states \(\mathbf{s} \in \mathbb{R}^{n \times h}\).
            </li>
            <li>
            \(C\), the <i>coda</i>, has 2 main responsibilities. It un-embeds from latent space using several layers and contains the prediction head of the model.
            </li>
        </ul>
    </p>
    <h4>Motivation for this Design.</h4>
    <p>
    The minimal setup required for learn stable iterative operators includes the following.
    <ul>
        <li>
        An initial starting state (a random starting point, \(s_0\)).
        </li>
        <li>
        A previous state to build upon (\(s_{i-1}\)).
        </li>
        <li>
        The input data (\(e\)) injected at every single step.
        </li>
    </ul>
    A good example is gradient descent of a function \(E(x, y)\), where \(x\) may be the variable of interest and \(y\) the data. Gradient descent on this function starts from an initial random state, here \(x_0\), and repeatedly applies a simple operation (the gradient of the function it optimizes), that depends on the previous state \(x_k\) and data \(y\). Note that we need to use \(y\) in every step to actually optimize our function.
    </p>
    <h4>The formal architecture.</h4>
    <p>
        Given a number of recurrent iterations \(r\), and a sequence of input tokens \(\mathbf{x} \in V^{n}\) these groups are used in the following way to produce output probabilities \(\mathbf{p} \in \mathbb{R}^{n \times |V|}\). As shown in Figure 2.
    </p>
    <p>
       <ul>
            <li>
            The prelude produces the embedded input data \(\mathbf{e} = P(\mathbf{x})\).
            </li>
            <li>
            The initial random state \(s_0\) is drawn from some standard deviation \(\sigma\) distributed normally.
            \(\mathbf{s}_0 \sim \mathcal{N}(0, \sigma^2 \mathbf{I}_{n \cdot h})\)
            </li>
            <li>
            The <i>core recurrent block</i> repeatedly produces a new state \(s_i\) while still using the original embedded input data \(\mathbf{e}\).
            \(\mathbf{s}_i = R(\mathbf{e}, \mathbf{s}_{i-1}) \quad \text{for } i \in \{1, \dots, r\}\).
            </li>
            <li>
            The coda produces the final output probabilities for predicting the next token from the last state. \(\mathbf{p} = C(\mathbf{s}_r)\).
            </li>
        </ul>
    </p>
    <p>
    Notice we repeatedly inject the data \(\mathbf{e}\) in our set-up in every step of the recurrence. Similarly to what's mentioned in the motivation.
    If \(\mathbf{e}\) was provided only at the start, e.g. via \(\mathbf{s}_0 = \mathbf{e}\), then the iterative process would not be stable<sup>1</sup>, as its solution would depend only on its boundary conditions.
    </p>
    <p>
        This architecture is based on deep thinking literature, where it is shown that injecting the latent inputs \(\mathbf{e}\) in every step (Bansal et al., 2022) and initializing the latent vector with a random state stabilizes the recurrence and promotes convergence to a steady state independent of initialization, i.e. path independence (Anil et al., 2022).
    </p>
    <h4>The inspiration for the architecture.</h4>
    <p>
        The structure of using several layers to embed input tokens into a hidden latent space is based on empirical results analyzing standard fixed-depth transformers (Skean et al., 2024; Sun et al., 2024; Kaplan et al., 2024). This body of research shows that the initial and the end layers of LLMs are noticeably different, whereas middle layers are interchangeable and permutable. For example, Kaplan et al. (2024) show that within a few layers standard models already embed sub-word tokens into single concepts in latent space, on which the model then operates.
    </p>
    </div>
</div>

## The general rule

The general rules I used in my writing were "known before new" (mention known concepts before introducing new ones), "anchor the reader before adding weight" (establish the main concept immediately, such as in the initial sentence or title), and "one core claim per paragraph".
