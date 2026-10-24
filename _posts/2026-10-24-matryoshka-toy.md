---
title: "Three models in one: a toy Matryoshka suite vs. three separate models"
description: "One nested transformer with three exits, trained once, against three separate models of matched size. The shape of the paper's result holds at toy scale."
paper: matryoshka-lm-suites
role: coding
task: reimplement
by: [liadber]
---

## What I reimplemented

The paper's core experiment, at toy scale: train **one** transformer with three exit points, where the small model is the first layers of the medium one and the medium is the first layers of the large one, and compare each exit against a **separate** model of the same depth and parameter count. Same text, same number of steps.

I did not reproduce the paper's numbers (36% less compute, 14% faster decoding, perplexity within ±1.4%). Those come from 0.5B–3B models on billions of tokens. What a toy can test is the *mechanism* and the *shape* of the result: does each nested exit reach the quality of a separate model of the same size?

**The setup.** There was no time to train on real text, so the text is generated from a small grammar. The first version was too easy — every model reached the same loss almost at once, and there was nothing to compare. For model size to matter, the sentences have to require memory over distance, so the grammar has two long-range dependencies: subject–verb agreement across a relative clause ("the dog that the drivers help **smiles**" — the verb goes with *dog*, not *drivers*) and a name copied from the start of a sentence to its end ("liad says that … , said liad"). Character-level, 28 symbols, context of 96 characters — a whole sentence fits in the window. The suite: 2 layers at width 64 → +2 at width 128 → +2 at width 256. The baselines: three models with the same depth as each exit, width chosen so the parameter count matches the exit's cumulative count (the paper's Table 1 does the same). 1,500 steps each, CPU, about 24 minutes in total.

## The code

Everything from section 2 of the paper is in two functions. The forward pass is one loop: each block adds its layers at a wider width, and between blocks sits the junction.

```python
def forward(self, token_ids):
    logits_per_exit = []
    hidden = None
    for exit_index, stack in enumerate(self.stacks):
        fresh_embedding = stack.embed(token_ids)        # embedding at this block's width
        if hidden is None:
            block_input = fresh_embedding
        else:                                           # --- inter-model junction ---
            previous_width = hidden.size(-1)
            new_dimensions = fresh_embedding[..., previous_width:]   # only the NEW columns
            if self.rescale:                            # match the previous output's norm
                hidden = hidden * (new_dimensions.norm(dim=-1, keepdim=True)
                                   / (hidden.norm(dim=-1, keepdim=True) + 1e-6))
            block_input = torch.cat([hidden, new_dimensions], dim=-1)   # concat(õ_m, e_{m+1})
        hidden = stack.blocks(block_input)              # this block's extra layers
        logits_per_exit.append(self.lm_heads[exit_index](self.final_norms[exit_index](hidden)))
    return logits_per_exit                              # three tables of logits from ONE pass
```

The loss is a sum over exits of cross-entropy against the text, plus distillation from the largest exit for the smaller ones. `detach()` is the paper's `stop_grad`: the teacher's table is a constant, so the large model is never pulled toward the small ones.

```python
def matryoshka_loss(logits_per_exit, targets, alpha=0.3):
    teacher_probs = F.softmax(logits_per_exit[-1].detach(), dim=-1)   # stop_grad(σ(l^M))
    total_loss = 0.0
    for exit_index, logits in enumerate(logits_per_exit):
        cross_entropy = F.cross_entropy(logits.view(-1, VOCAB_SIZE), targets.view(-1))
        is_largest = exit_index == len(logits_per_exit) - 1
        if not is_largest:
            distillation = -(teacher_probs * F.log_softmax(logits, dim=-1)).sum(-1).mean()
            total_loss = total_loss + (1 - alpha) * cross_entropy + alpha * distillation
        else:
            total_loss = total_loss + cross_entropy        # the largest exit has no teacher
    return total_loss
```

Full code (one file, runs on CPU), the results file and the figure: [github.com/liadber/matryoshka-toy](https://github.com/liadber/matryoshka-toy)

## Results

{% include figure.liquid path="assets/img/posts/matryoshka-toy/curves.png" class="img-fluid rounded z-depth-1" caption="Validation loss during training. Dashed: three separate models. Solid: the three exits of one nested model. The medium and large pairs sit on top of each other; the small nested exit trails its twin for most of training and nearly closes the gap at the end." %}

**Quality, per size** (validation cross-entropy per character, lower is better):

| size | separate | nested | gap |
|---|---|---|---|
| small | 0.345 | 0.358 | +3.8% |
| medium | 0.325 | 0.327 | +0.6% |
| large | 0.315 | 0.318 | +1.2% |

The paper reports every size within ±1.4% of its separately trained twin. In the toy, the medium and large exits land in that range; the small exit is 3.8% behind. The direction is the same across all three — nested is slightly worse, never better — and the smallest pays the most. The difference is probably a matter of scale: here the small exit is 2 of the 6 layers, and those 2 layers also have to serve the medium and large exits; in the paper's suite the smallest model is 24 of 39 layers.

**Parameters and time.** The three separate models total 2.82M parameters; the nested model that contains all three has 2.15M (24% fewer). This is arithmetic, not a finding: the saving follows from the shapes (the paper's suite saves 38% for the same reason). Training all three separately took 812 s; the nested model took 620 s, also 24% less — the compute saving the paper reports (36%) comes from the same place.

**Agreement** (how often two models pick the same next character — what speculative decoding needs):

| pair | separate | nested |
|---|---|---|
| small / medium | 90.2% | 91.1% |
| medium / large | 91.7% | **94.7%** |
| small / large | 90.1% | 90.4% |

The paper's section 3.2.2 says nested models agree with each other more than independently trained ones, and that this is what makes a non-tiny draft useful. The toy shows the same thing, and in the same place: the biggest gain is for the medium/large pair (+3 points), which is exactly the pair the paper builds its speculative decoding on (500M drafting for 3B). The medium exit is literally part of the large one and was distilled from it; two separate models share only the training text.

**What I did not test.** Speculative decoding itself (the 14–26% throughput gain) — that is an inference-engineering project of its own. And the paper's claim that removing the norm matching in the junction degrades perplexity; the code has a `--no-rescale` flag for exactly that experiment, which I did not get to run before class.

## What I learned

**A baseline that fails is not a result for you.** My first run compared each exit to a separate model with the same depth *and width* as the exit — more parameters than the exit actually uses, and not what the paper does. The large baseline also failed to converge (its loss ended *above* the medium one's). That run showed the nested large model "20% better". A number that big in your favor should be the first thing you distrust; the fix was a parameter-matched baseline, a lower learning rate with warmup, and gradient clipping.

**The junction is two lines.** Rescale, concatenate. Section 2 of the paper spends a page on it — notation, `stop_grad`, the distillation formula — and the implementation of all of it is shorter than this paragraph. What matters is not the code but the reason for the two lines: transformer outputs are much larger than embeddings, and without matching the norms the first channels destabilize.

**A toy can test shape, not size.** Whether nesting costs the small model anything at 3B is a question about 3B. What the toy shows is that the mechanism works as the paper describes: one model, three exits, all three close to the quality of separate models — with 24% fewer parameters.
