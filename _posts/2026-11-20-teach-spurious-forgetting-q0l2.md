---
title: "Transformer Feed-Forward Layers Store Memories"
description: How feed-forward layers store and retrieve learned associations.
paper: spurious-forgetting
task: teach
by: [NicolasRW]
---

## Why this matters

{% cite palit2026spurious --style _bibliography/narrative-author-year.csl %} studies how language models can lose access to previously learned facts without erasing them. This raises the question of how knowledge is represented inside a transformer.

{% cite geva2021ffn --style _bibliography/narrative-author-year.csl %} studied the role of feed-forward layers in language models. Although these layers account for two-thirds of a transformer's parameters, much of the early work focused on self-attention. They proposed that feed-forward layers behave like key-value memories, where individual neurons learn associations between patterns in the input and possible continuations. This interpretation comes directly from the structure of a standard feed-forward layer.

## The idea: Feed-forward layers as memories

A standard transformer feed-forward layer applies:

$$ \operatorname{FFN}(x)=f(xK^\top)V $$

Here, $x\in\mathbb{R}^{d}$ is the contextualized representation of a token, and $K,V\in\mathbb{R}^{d_m\times d}$ are learned weight matrices. We can rewrite this as:

$$ \operatorname{FFN}(x)=\sum_{i=1}^{d_m} \underbrace{f(x\cdot k_i)}{\text{activation}} \underbrace{v_i}{\text{value}} $$

This shows a simple interpretation: each of the 4096 neurons corresponds to a key-value pair. The key (k_i) determines when a memory should be activated, while the value (v_i) determines what information it contributes to the output. The activation provides a coefficient that controls how strongly the value influences the representation. The keys do not operate directly on individual words. They operate on contextualized token representations, which also contain information from the surrounding text. 

As an example, consider the input: "Comet served only briefly with the fleet, owing in large ..." One memory can recognize the pattern "owing in large" and contribute information that favors "part" as the next token. In fact, in layer 15, neuron 881, the value's most favored token was "part", and 92% of the 50 contexts that most strongly activated its key were followed by that token. However, not all memories recognize specific expressions. They also identified keys responding to broader patterns, including military contexts involving bases, references to television shows, and semantic relationships such as being "part of" something. This showed that keys could represent many levels of abstraction, from word sequences to more general properties.

To do test this, they studied a 16-layer transformer. They analyzed which examples activate each memory and what its corresponding value predicts. First, they studied the keys. They randomly selected 160 neurons and measured activations on prefixes from the training data. For each neuron, they got the 25 prefixes producing the highest activations and asked humans to identify patterns, finding that most could be explained by recognizable patterns. There was also a trend across layers, since lower layer keys mainly recognized shallow patterns, such as particular words or expressions, while higher layer keys detected semantic patterns. They also studied how removing different words affected the activations. Removing the final word caused a larger change than removing earlier words, but this became weaker in higher layers, since upper-layer keys depended more on context.

Then, they studied if the values encode information about which tokens should come next. Since each value is a vector in the model's hidden space, they projected it into the space using the output embedding matrix:

$$ p_i=\operatorname{softmax}(v_i E) $$

This gives a distribution over tokens for each value. They then checked if the tokens receiving high probabilities were also likely to follow the contexts that strongly activated the corresponding key. The agreement increased in higher layers. Although exact matches were relatively uncommon, the next tokens usually received higher rankings in the distributions.

Finally, they explain how memories combine. The output of a feed-forward layer is a weighted sum of many active values. In most of the examples across layers, the layer's top prediction differed from every individual memory's top prediction. This showed that predictions emerge from composing of many contributions.















