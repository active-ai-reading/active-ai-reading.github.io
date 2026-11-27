---
# Copy to _posts/YYYY-MM-DD-short-title.md  and fill in. Delete these comment lines.
title: "Copyediting LLM-JEPA's 3.1 section"
description: Simpler explanation of the LLM-JEPA main points
paper: llm-jepa # the filename of the paper in _papers/, without .md
task: copyedit # abstract | copyedit | key-points   (see the roles page)
by: shachar731945
---

## What I changed and why

I think the description of "Pred(Enc(Text))" is not correct since the input is not just the text (its the text plus prediction tokens), and that the "Pred function" is not really a function but just taking the last hidden_state of the last layer, just as Enc does for Code but not for Text in a confusing manner.
I'll change that to make it cleaner and more understandable.

## Before and after

<div class="before-after">
  <div class="before"><span class="label">Before</span>
    <h4>3.1 The LLM-JEPA Objective</h4>
    <p>Throughout this section, we will use Text and Code as concrete examples of having different views of the same underlying knowledge. It should be clear to the reader that our proposed LLM-JEPA objective handles different types of views similarly.</p>
    <p>The construction of our LLM-JEPA objective relies on two principles. First, we must preserve the generative capabilities of LLMs and we therefore start with the $\mathcal{L}_{\text{LLM}}$ from eq. (1). Second, we aim to improve the abstraction capabilities of LLMs using the joint embedding prediction task. On top of $\mathcal{L}_{\text{LLM}}$, we then propose to add the well-established JEPA objective leading to the complete loss $\mathcal{L}$ defined as</p>
    <div style="overflow-x: auto; margin: 0.75em 0;">
    $$\mathcal{L}_{\text{LLM-JEPA}} = \underbrace{\sum_{\ell=2}^{L} \mathcal{L}_{\text{LLM}}(\text{Text}_{1:\ell-1}, \text{Text}_\ell)}_{\text{generative capabilities (LLM)}} + \underbrace{\lambda \times d(\text{Pred}(\text{Enc}(\text{Text})), \text{Enc}(\text{Code}))}_{\text{abstraction capabilities (JEPA)}}, \qquad (2)$$
    </div>
    <p>where $\lambda \ge 0$ is an hyperparameter balancing the contribution of the two terms, $\text{Pred}$ and $\text{Enc}$ are the predictor and encoder networks respectively, and $d$ is a metric of choice, e.g., the $\ell_2$ distance. Let’s now precisely describe each of those components.</p>
    <p><strong>The encoder.</strong> We use the <code>hidden_state</code> of the last token from the last layer as the embedding of an input sequence–as commonly done for LLM probing. We pack both Text and Code into a single context window, applying an attention mask to ensure they do not reference each other. Implementation-wise, most HuggingFace transformers support an additive attention mask, where setting entry $(i, j) = -\infty$ prevents token $j$ from attending to token $i$ (for $i &lt; j$). Using this mechanism, we implement LLM-JEPA with only one additional forward pass. This introduces extra cost during training, but not during inference—see section 6 for further discussion.</p>
    <p><strong>The metric.</strong> When it comes comparing embeddings, it is now widely accepted in vision to leverage the cosine similarity. We thus propose to do the same for LLM-JEPA.</p>
    <p><strong>The predictor.</strong> We leverage the auto-regressive nature of LLM and their internal self-attention to define a <em>tied-weights predictor</em>. By introducing a special token <code>[PRED]</code> at the end of a given input, we allow for further nonlinear processing of the input hereby producing $\text{Pred}(\cdot)$ at the final embedding of the last layer. By reusing the internal weights of the LLM for the prediction task, we greatly reduce the training overhead and architectural design choices. Practically, we append $k \in \{0, \dots, K\}$ predictor tokens to an input prompt and use the embedding of the last predictor token to be $\text{Pred}(\text{Enc}(\cdot))$. When $k = 0$, the predictor is trivial, i.e., $\text{Pred}(x) = x$.</p>
  </div>
  <div class="after"><span class="label">After</span>
    <h4>3.1 The LLM-JEPA Objective</h4>
    <p>In order to conserve the generative capabilities of LLMs and improve their abstraction capabilities using the joint embedding prediction task, we propose to add the well-established JEPA objective leading to the complete loss $\mathcal{L}$ defined as</p>
    <div style="overflow-x: auto; margin: 0.75em 0;">
    $$\mathcal{L}_{\text{LLM-JEPA}} = \underbrace{\sum_{\ell=2}^{L} \mathcal{L}_{\text{LLM}}(\text{Text}_{1:\ell-1}, \text{Text}_\ell)}_{\text{generative capabilities (LLM)}} + \underbrace{\lambda \times d(\text{Enc}(\text{Text} + \text{[PRED]}), \text{Enc}(\text{Code}))}_{\text{abstraction capabilities (JEPA)}}, \qquad (2)$$
    </div>
    <p>where $\lambda \ge 0$ is an hyperparameter balancing the contribution of the two terms, $\text{Enc}$ is the encoder network, $\text{[PRED]}$ are the added semantic tokens for the JEPA objective, and $d$ is a metric of choice, e.g., the $\ell_2$ distance. Let’s now precisely describe each of those components.</p>
    <p><strong>The predictor.</strong> We leverage the auto-regressive nature of LLM and their internal self-attention to define a <em>tied-weights predictor</em>.
    By introducing special tokens $\text{[PRED]}$ at the end of a given input, we allow for further nonlinear processing of the input hereby producing additional embeddings at the last layer. By reusing the internal weights of the LLM for the prediction task, we greatly reduce the training overhead and architectural design choices. Practically, we append $k \in \{0, \dots, K\}$ predictor tokens to an input prompt and use the embedding of the last predictor token to be $\text{Enc}(\cdot)$. When $k = 0$, the predictor is trivial, giving us the last embedding of the last token of encoded input.</p>
    <p><strong>The encoder.</strong> We use the <code>hidden_state</code> of the last token from the last layer as the embedding of an input sequence–as commonly done for LLM probing, where the last token for the $\text{Text} + \text{[PRED]}$ is the $K$-th $\text{[PRED]}$ token. We pack both Text and Code into a single context window, applying an attention mask to ensure they do not reference each other. Implementation-wise, most HuggingFace transformers support an additive attention mask, where setting entry $(i, j) = -\infty$ prevents token $j$ from attending to token $i$ (for $i &lt; j$). Using this mechanism, we implement LLM-JEPA with only one additional forward pass. This introduces extra cost during training, but not during inference—see section 6 for further discussion.</p>
    <p><strong>The metric.</strong> When it comes comparing embeddings, it is now widely accepted in vision to leverage the cosine similarity. We thus propose to do the same for LLM-JEPA.</p>
  </div>
</div>

### The general rule

First reading the article I got confused by the notation of the Pred(Enc(Text)). Only after further reading I understood the method and how confusing this notation is.
Therefore, I tried to think what would be the simplest way to explain the method, without assuming any prior knowledge or context by the reader.
In other words, I tried to assume the reader hasn't read paragraphs coming after the equation before reading the equation, I don't want a reader going back and forth in his reading to understand the methodology, further reading should just expand and sharpen the reader's understanding.
