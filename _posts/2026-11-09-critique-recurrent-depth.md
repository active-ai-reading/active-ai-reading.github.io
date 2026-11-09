
---
title: "Critique: Parameter-efficient, but is it compute-efficient?"
description: "A solid proof of concept at scale, but the comparisons do not control for compute, and the latent-space figures show structure rather than reasoning."
paper: recurrent-depth-latent-reasoning
role: research
task: critique
by: [Reuvenspitz]
---

## Summary of the claims

The paper {% cite geiping2025latent %} proposes a language model whose middle block is applied repeatedly in latent space before producing the next token. The main claims are:

1. **Recurrent depth can be trained at scale.** Using a shared recurrent block, randomly sampled iteration counts, and truncated backpropagation, the authors train a 3.5B parameter model on approximately 800B tokens.
2. **More iterations at test time improve performance**, especially on reasoning tasks such as GSM8K and ARC-Challenge, reaching a computation load equivalent to much larger models.
3. **No special Chain-of-Thought training data is required.** The model learns to use additional computation through standard next-token prediction, without explicitly supervised reasoning traces.
4. **The architecture naturally supports additional inference techniques**, including adaptive exits, KV-cache sharing, and potentially self-speculative decoding.
5. **Structured dynamics emerge in latent space**, including convergence patterns, orbits, and directional drifts, which the authors suggest may be related to internal reasoning mechanisms.

## Strengths

- **A convincing demonstration at scale.** The authors show that a recurrent-depth language model can be trained with billions of parameters and hundreds of billions of tokens. Increasing test-time recurrence substantially improves performance. On GSM8K CoT, the model achieves 42.08% flexible accuracy at 32 iterations (Table 2), compared with almost no success at a single iteration.
- **No explicit CoT supervision is required.** The model learns to benefit from additional computation during regular language-model training, without requiring labeled intermediate reasoning steps.
- **Interesting inference capabilities.** The experiments suggest that adaptive computation and KV-cache sharing can be applied without additional training. The possibility of self-speculative decoding is also interesting, although its practical speedup is not demonstrated.
- **Transparency and reproducibility.** The authors release their model, code, and training data. They also discuss failed training runs and the stability problems they encountered (Figure 5), which provides useful information for future research.

## Weaknesses

### 1. Parameters are matched, but compute is not

The fixed-depth baseline in Table 4 uses the same basic architecture with only one pass through the recurrent block and is trained on the same 180B tokens. However, at 32 iterations, the recurrent model has an effective depth of:

$$
2 + 4 \cdot 32 + 2 = 132
$$

compared with only 8 layers for the baseline. Therefore, the recurrent model uses substantially more training computation per token.

The authors acknowledge this issue, noting that their model consumes pretraining FLOPs comparable to a much larger standard Transformer. For example, a rough parameter-token estimate suggests a training compute budget comparable to, or potentially greater than, that of some larger models used in the comparisons. This is not an exact FLOP comparison, but it illustrates why parameter count alone can be misleading.

Interestingly, Table 4 also shows that at a single recurrence, where inference costs are more comparable, the recurrent model performs worse than the fixed-depth baseline (34.01% vs. 46.42% on ARC-E at 180B tokens). However, this comparison is also limited because the recurrent model was mainly trained with much greater depth.

I think the results demonstrate **parameter efficiency**, but do not establish **compute efficiency**. This does not invalidate the contribution, since reducing parameter count can be valuable for memory and communication costs. However, the distinction should be clearer.

A related limitation is the lack of a direct comparison with Chain-of-Thought at the same inference compute budget. The paper presents latent reasoning as an alternative or complement to verbalized reasoning, but does not establish when additional recurrent iterations are preferable to generating more reasoning tokens.

### 2. The latent-space analysis shows structure, not necessarily reasoning

Section 7 presents interesting patterns in the hidden-state trajectories, including orbits, convergence, and directional drifts. The authors suggest these might represent internal computational mechanisms.

However, these conclusions are based mainly on qualitative visualizations of selected tokens, projected onto a small number of PCA directions.

For example, the orbit observed for the token "3" in Figure 12 might be related to arithmetic processing, but the visualization alone does not establish that the model is actually performing an arithmetic operation through this trajectory.

The authors are generally careful in their wording, using expressions such as "could serve" and "suggests". Nevertheless, the connection between these geometric patterns and reasoning remains speculative.

A [reimplementation by another student in this course]({{ '/posts/2026/retracing-hidden-trajectories/' | relative_url }}) also illustrates how difficult it is to interpret these trajectories. Different contexts produce different patterns of convergence, but these observations do not directly establish what computations are taking place.

Moreover, the path-independence experiments investigate the effect of changing the initial state, rather than testing whether specific trajectories causally contribute to the final prediction.

## How it could have been improved

- **FLOP-matched baselines.** Compare the recurrent model with standard Transformers trained under the same total compute budget, using larger models, more training tokens, or greater fixed depth.
- **Recurrence vs. Chain-of-Thought.** Compare additional recurrent iterations against longer CoT generation or multiple sampled solutions under the same inference FLOP budget.
- **More systematic trajectory analysis.** Measure how frequently different patterns occur across tasks and tokens, and whether they correlate with correct predictions. For example, compare numerical tokens in arithmetic problems with identical tokens in ordinary text.
- **Causal interventions.** Modify or suppress particular directions in latent space during recurrence and measure their effect on performance. This could provide stronger evidence that the observed trajectories are functionally important rather than simply correlated with the task.

## Verdict

**Accept.**

I think the paper makes a meaningful contribution by demonstrating that recurrent-depth language models can be trained at scale and can benefit substantially from additional test-time computation. The training methodology, open release, and experimental results make it a valuable proof of concept.

However, the comparisons with larger models should be interpreted primarily in terms of parameter efficiency rather than compute efficiency. Similarly, the latent-space analysis should be viewed as exploratory rather than direct evidence of specific reasoning mechanisms.

**Is the direction worth pursuing?** Yes. I think recurrent depth is a promising approach to test-time computation, especially if future work can establish its advantages under equal compute budgets and provide stronger evidence about the computations performed in latent space.
