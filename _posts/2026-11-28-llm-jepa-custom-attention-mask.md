---
title: "Reimplementing the LLM-JEPA Custom Attention Mask"
description: Reimplementing the block-causal attention mask and verifying that it prevents information leakage between text and code representations.
paper: llm-jepa
task: reimplement
by: [NettaShemesh103]
---

## What I reimplemented

I reimplemented the custom attention mask proposed in Section 3.2 of the LLM-JEPA paper. The authors use this mask to process text and code within the same context window while preventing attention between the two sequences.

To test the mechanism without training a large language model, I implemented a single scaled dot-product self-attention layer in PyTorch using synthetic token embeddings. Each input contained four text tokens and three code tokens, with an embedding dimension of 16.

I modified only the text tokens and measured the resulting change in the code representations under standard causal attention and custom attention. I also compared joint processing with the custom mask against processing the two sequences separately. The experiment was repeated across 30 random seeds.

## The code

```python
import torch

T, C = 4, 3


def additive_mask(k):
    mask = torch.zeros((k, k), dtype=torch.float64)
    mask[torch.triu(torch.ones(k, k), diagonal=1) == 1] = -torch.inf
    return mask


regular = additive_mask(T + C)

custom = torch.full_like(regular, -torch.inf)
custom[:T, :T] = additive_mask(T)
custom[T:, T:] = additive_mask(C)
```

The custom mask creates two independent causal attention blocks. Cross-sequence attention scores are set to negative infinity, resulting in zero attention weights after softmax.

Full code: [Jupyter Notebook](https://github.com/active-ai-reading/active-ai-reading.github.io/blob/main/assets/img/posts/llm-jepa-custom-attention-mask/jepa_attention_experiment.ipynb)

## Results

{% include figure.liquid path="assets/img/posts/llm-jepa-custom-attention-mask/jepa_attention_results.png" class="img-fluid rounded" caption="Standard and custom attention weights (one representative run), and mean maximum representation differences across 30 random seeds." %}

The first two heatmaps show the attention weights for one representative run. Under standard causal attention, code tokens can attend to text tokens. Under the custom mask, these cross-sequence attention weights are zero.

The bar chart reports the mean maximum absolute difference in output representations across 30 random seeds.

| Experiment | Mean maximum absolute difference |
| --- | ---: |
| Standard mask: text modified | 1.587614 |
| Custom mask: text modified | 0.000000 |
| Custom mask vs. separate processing | 0.000000 |

The results match the expected behavior described in Section 3.2. Modifying the text affected the code representations under standard causal attention, but not under the custom mask. Joint processing with the custom mask also produced identical outputs to separate processing for both sequences in this experimental setup.

The paper does not report numerical results for this specific test, so a direct numerical comparison is not possible. This experiment validates the masking mechanism in a simplified setting rather than reproducing the full LLM-JEPA training procedure.

## What I learned

I learned how additive attention masks control information flow inside a Transformer and how setting attention scores to negative infinity prevents unwanted interactions between sequences.

The experiment helped me understand how the authors obtain independent text and code representations in one additional forward pass for the JEPA loss, reducing the total number of forward passes in their implementation from three to two.

A simplified experiment can validate the correctness of a specific mechanism without expensive LLM training. However, because I used synthetic embeddings and a single attention layer without positional encodings, I did not verify actual runtime savings, full-model equivalence, or improvements in downstream accuracy.
