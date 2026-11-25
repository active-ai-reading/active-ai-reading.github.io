---
title: "Papers worth knowing this week"
description: two papers ont the use of hidden representation on the training.
paper: llm-jepa
task: trending
by: [matan2001]
---

<!-- At least two papers, one sentence each, with a link. How you organize the rest is up to you. -->

<h3>
    <a href="https://arxiv.org/abs/2606.05753">
        Cosine Misleads: Auxiliary Losses Reshape Vision Language Models, Not Their Latents
    </a>
</h3>
<p>
    XiuYu Zhang, Junfeng Fang, Zhenkai Liang, 2026.
</p>
<p>
    This paper investigates whether improving the alignment between intermediate
    latent representations and their target visual embeddings actually improves
    vision-language model (VLM) performance. This directly addresses a concern
    raised by LLM-JEPA: forcing related representations to align does not
    necessarily benefit the model's original task and may even hurt its performance.
    Their findings suggest that auxiliary representation losses may
    influence performance by modifying the model's shared parameters rather
    than by improving the representations used for reasoning.
</p>

<h3>
    <a href="https://arxiv.org/abs/2511.05963">
        Next-Latent Prediction Transformers Learn Compact World Models
    </a>
</h3>
<p>
    Jayden Teoh, Manan Tomar, Kwangjun Ahn, Edward S. Hu, Tim Pearce,
    Pratyusha Sharma, Akshay Krishnamurthy, Riashat Islam, Alex Lamb,
    John Langford, 2026.
</p>
<p>
    This paper introduces NextLat, an auxiliary training objective that encourages
    Transformers to predict their next hidden state from the current hidden state
    and the next token. The goal is to encourage the model to maintain compact
    internal representations that capture information necessary for future
    predictions, rather than relying entirely on attention over previous tokens.
    The authors theoretically show that, under ideal conditions, these hidden
    states become sufficient for predicting future sequences. 
    This presents another approach to incorporating representation learning
    into a model's loss function, using the prediction of future hidden states
    rather than aligning representations of semantically related inputs.
</p>
