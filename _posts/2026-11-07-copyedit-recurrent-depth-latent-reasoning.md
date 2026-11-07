---
title: "Copyediting the Introduction of Recurrent Depth"
description: "What is actually new about recurrent reasoning? Making the paper's contribution clear from the start."
paper: recurrent-depth-latent-reasoning
role: writing
task: copyedit
by: [Shueyr]
---

## What I changed and why

Although the introduction acknowledges that recurrent computation is an established idea, it does not clearly distinguish earlier work from this paper's contribution, leaving the detailed comparison until Section 8. I rewrote Section 1 to introduce the closest prior work before explaining what this paper adds: a concrete architecture and training procedure, a demonstration at scale, and measured improvements from additional inference-time computation. This makes the paper's contribution clearer before readers reach the methods and results.

## Before and after

<div class="before-after">
  <div class="before" markdown="1">
<span class="label">Before</span>

Humans naturally expend more mental effort solving some problems than others. While humans are capable of thinking over long time spans by verbalizing intermediate results and writing them down, a substantial amount of thought happens through complex, recurrent firing patterns in the brain, before the first word of an answer is uttered.

Early attempts at increasing the power of language models focused on scaling model size, a practice that requires extreme amounts of data and computation. More recently, researchers have explored ways to enhance the reasoning capability of models by scaling test time computation. The mainstream approach involves post-training on long chain-of-thought examples to develop the model's ability to verbalize intermediate calculations in its context window and thereby externalize thoughts.

However, the constraint that expensive internal reasoning must always be projected down to a single verbalized next token appears wasteful; it is plausible that models could be more competent if they were able to natively “think” in their continuous latent space. One way to unlock this untapped dimension of additional compute involves adding a recurrent unit to a model. This unit runs in a loop, iteratively processing and updating its hidden state and enabling computations to be carried on indefinitely. While this is not currently the dominant paradigm, this idea is foundational to machine learning and has been (re-)discovered in every decade, for example as recurrent neural networks, diffusion models, and as universal or looped transformers.

In this work, we show that depth-recurrent language models can learn effectively, be trained in an efficient manner, and demonstrate significant performance improvements under the scaling of test-time compute. Our proposed transformer architecture is built upon a latent depth-recurrent block that is run for a randomly sampled number of iterations during training. We show that this paradigm can scale to several billion parameters and over half a trillion tokens of pretraining data. At test-time, the model can improve its performance through recurrent reasoning in latent space, enabling it to compete with other open-source models that benefit from more parameters and training data. Additionally, we show that recurrent depth models naturally support a number of features at inference time that require substantial tuning and research effort in non-recurrent models, such as per-token adaptive compute, (self)-speculative decoding, and KV-cache sharing. We finish out our study by tracking token trajectories in latent space, showing that a number of interesting computation behaviors simply emerge with scale, such as the model rotating shapes in latent space for numerical computations.

On a more philosophical note, we hope that latent reasoning captures facets of human reasoning that defy verbalization, such as spatial thinking, physical intuition or (motor) planning. Over many iterations of the recurrent process, reasoning in a high-dimensional vector space would enable the deep exploration of multiple directions simultaneously, instead of linear thinking, leading to a system capable of exhibiting novel and complex reasoning behavior.

Scaling compute in this manner is not at odds with scaling through extended (verbalized) inference scaling (Shao et al., 2024), or scaling parameter counts in pretraining (Kaplan et al., 2020), we argue it may build a third axis on which to scale model performance.

  </div>
  <div class="after" markdown="1">
<span class="label">After</span>

Language models can allocate additional computation to difficult problems by generating intermediate reasoning tokens, as in chain-of-thought approaches. An alternative is to perform additional computation directly in the model's continuous latent space before predicting the next token. We investigate this approach through **recurrent depth**, in which a shared block of transformer layers is applied repeatedly to update a hidden state. This allows the model to increase its effective computational depth at inference time without increasing its number of parameters or generating additional intermediate tokens.

**Prior work.** Recurrent computation across transformer depth has been studied extensively. Universal Transformers (Dehghani et al., 2019) applied recurrence across transformer layers, while ALBERT (Lan et al., 2019) demonstrated parameter sharing across layers at scale, using a fixed number of layer applications. Subsequent work on "deep thinking" networks showed that randomized iteration counts and repeated input injection can enable learned algorithms to generalize to additional computation at inference time (Schwarzschild et al., 2021b; Bansal et al., 2022). Our architecture and training procedure build on these findings. Related studies have further investigated the theoretical properties and learning capabilities of looped transformers, primarily through theoretical and small-scale analyses (Giannou et al., 2023; Yang et al., 2024a; Fan et al., 2025).

Deep equilibrium models provide another perspective on iterative computation, using fixed-point formulations (Bai et al., 2019). In contrast, our training procedure explicitly unrolls a sampled number of recurrent iterations and truncates backpropagation through the recurrent block to the final steps. As we show in Section 7, the resulting latent trajectories exhibit a range of behaviors beyond simple convergence to fixed points.

Recent work has also explored latent reasoning by adapting pretrained language models. For example, Hao et al. (2024) train a pretrained transformer to reuse its final hidden state as an input, using reasoning chains to learn continuous intermediate computation. Our approach instead incorporates recurrence directly into the architecture during pretraining and optimizes a standard next-token prediction objective with variable recurrent depth. Unlike approaches that use reasoning chains to supervise latent computation, our method does not require a separate training curriculum for intermediate reasoning steps. However, our pretraining mixture does include instruction and mathematical reasoning data, as detailed in Section 4.1 and Appendix C.

**Our contribution.** Building on these earlier approaches, we investigate whether recurrent-depth language models can be trained at substantial scale and effectively exploit additional computation at inference time. Our contribution is not the introduction of recurrence itself, but rather a scalable architecture and training procedure, together with an empirical evaluation of their behavior and inference-time capabilities.

Our architecture consists of an input-processing prelude, a shared recurrent core, and an output-processing coda. At each iteration, the recurrent core updates the latent state while receiving the prelude's representation of the input. During training, we sample recurrence counts from a heavy-tailed distribution and backpropagate through at most the final eight recurrent iterations, reducing activation memory requirements (Section 3). We also identify normalization and initialization choices that are necessary for stable training at scale. In unsuccessful training runs, the model either collapsed its token representations or learned to ignore the recurrent state, preventing effective use of additional iterations (Section 4.3).

Our main contributions are threefold:

1. **Training at scale.** We train a 3.5B-parameter recurrent language model on approximately 800B tokens and release the training code, data, and model checkpoints. Our results demonstrate that variable-depth recurrence can be trained successfully at substantial language-model scale, extending earlier small-scale studies of looped transformers (Sections 3–4).
2. **Scaling test-time computation.** We evaluate the same model at different recurrence counts and show that additional iterations improve performance, with saturation depending on the task. Mathematical reasoning and coding tasks generally benefit from more iterations than tasks such as HellaSwag (Section 5). The model can operate at inference compute budgets comparable to those of fixed-depth models with approximately 50B parameters. We also compare against a non-recurrent baseline trained with the same data and training setup for 180B tokens. Although recurrence provides substantial improvements on harder tasks, the comparison is not FLOP-matched, since additional iterations increase computation.
3. **Inference capabilities and latent-state analysis.** We demonstrate per-token adaptive stopping and KV-cache sharing without additional training, and describe how recurrence can support continuous state reuse and self-speculative decoding (Section 6). We further analyze latent-state trajectories and identify several recurring patterns, including convergence, orbits, and directional drifts, providing insight into the model's iterative computation (Section 7).

Our results establish the feasibility of training recurrent-depth language models at scale and improving their performance through additional latent computation. Nevertheless, the model remains a proof of concept based on a single successful large-scale training run. Its relatively small parameter count should not be interpreted as an equivalent reduction in computational cost, since repeated application of the recurrent core increases the required FLOPs. Further work is needed to establish how recurrent depth compares with alternative approaches under matched compute budgets. We view recurrent depth as a complementary direction to parameter scaling and explicit chain-of-thought reasoning, offering an additional axis along which language-model computation can be scaled.

  </div>
</div>

## The general rule

**Present the relevant related work before stating the paper's contribution.** Make clear which ideas come from earlier work and credit their authors, so readers can identify what the paper adds without mistaking inherited ideas for new inventions.
