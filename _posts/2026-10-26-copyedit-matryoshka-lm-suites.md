
---
title: "Copyediting Speculative Decoding Throughput in Matryoshka Language Model Suites"
description: "Why a larger draft model can slow down speculative decoding—and how Matryoshka changes that trade-off."
paper: matryoshka-lm-suites
role: writing
task: copyedit
by: [dan22333]
---

## What I changed and why

I copyedited Section 3.2.3, *Speculative Decoding Throughput*. The original section presents the experimental setup before revealing its most interesting finding: conventional speculative decoding with a relatively large draft model provides little benefit, whereas Matryoshka significantly improves throughput. I reorganized the section to lead with that finding, explain the underlying mechanisms, and place the experimental details afterward, while preserving the paper's technical claims and quantitative results.

## Before and after

<div class="before-after">
  <div class="before"><span class="label">Before</span>

### 3.2.3 Speculative Decoding Throughput

We measure speculative decoding throughput on an NVIDIA A100 GPU using the 500M sub-model as draft and the 3B sub-model as verifier, under both greedy and nucleus (p = 0.9) sampling. The 500M / 3B size ratio (1:6) is large by literature standards, where draft models are typically one to two orders of magnitude smaller than the verifier [Leviathan et al., 2023, Zhou et al., 2024, Li et al., 2024a]. Each run uses prompts streamed from FineWeb-Edu truncated to 1,024 tokens, and generates 512 new tokens per prompt, sampled with temperature 0.4. The maximum batch size that can fit the 80GB VRAM in such a setup is 64 for the Vanilla pair and 102 for the Matryoshka pair. The Matryoshka setup fits a larger batch in the same KV-cache budget thanks to the shared draft/verifier cache. A larger batch size allows for faster drafts relative to verification steps, as it reduces the bandwidth latency. Each metric is averaged over roughly 1M generated tokens.

Figure 5 shows that the Matryoshka pair achieves higher accepted length than the Vanilla pair across most draft lengths in the nucleus case (+5% in average), which directly reflects the agreement-rate gap in Figure 4c. The higher acceptance translates to higher throughput: at a draft length of 6, Matryoshka reaches 2,650 tokens/s in greedy mode against 2,100 for Vanilla (a 26% speedup), and the gain is preserved under nucleus sampling. Crucially, the Vanilla 500M–3B pair barely beats plain autoregressive inference and is actually slower under nucleus sampling. At this size ratio, the draft-side KV cache and drafting FLOPs do not amortize against the acceptance rate.

  </div>
  <div class="after"><span class="label">After</span>

### 3.2.3 Speculative Decoding Throughput

Speculative decoding typically relies on draft models much smaller than the verifier, since larger drafts can cost more to run than the verification steps they save. In our experiments, a conventional 500M-draft / 3B-verifier pair (1:6 size ratio) barely outperforms autoregressive decoding and is slower under nucleus sampling. Matryoshka reverses this trade-off: with a draft length of 6, it achieves 2,650 tokens/s compared with 2,100 tokens/s for the independently trained pair under greedy decoding—a 26% throughput improvement. The advantage also holds under nucleus sampling (Figure 5).

Two properties explain this improvement. First, the nested architecture allows the draft and verifier to share their KV cache, reducing memory requirements and supporting larger batches. On an NVIDIA A100 with 80GB of memory, Matryoshka supports a batch size of 102, compared with 64 for the conventional pair. Second, jointly trained sub-models exhibit greater prediction agreement (Figure 4c). Under nucleus sampling, Matryoshka achieves approximately 5% longer accepted sequences on average across most draft lengths (Figure 5), improving verification efficiency.

We evaluate both approaches using a 500M draft and 3B verifier under greedy and nucleus sampling (p = 0.9). Prompts are drawn from FineWeb-Edu and truncated to 1,024 tokens, with 512 tokens generated per prompt and a sampling temperature of 0.4. Results are averaged over approximately one million generated tokens.

Together, KV-cache reuse and higher token acceptance make larger draft models practical for speculative decoding, even when conventional draft-verifier pairs offer little or no speedup.

  </div>
</div>

## The general rule

**Lead with the finding, explain the mechanism, then provide the experimental details.**

In a results section, readers should first understand *what was discovered and why it matters*. The mechanisms and supporting evidence should follow. Experimental settings are essential for reproducibility, but presenting them before the main result can bury the key contribution. Organize scientific writing around the insight readers should remember, rather than the order in which experiments were conducted.
