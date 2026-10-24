---
title: "Reimplementing a speculative decoding throughput test, shown in Figure 5a"
description: I implemented a speculative decoding throughput performance test, running the 500M model as a draft model and the full 3B model as the verifier, examining a speedup against a baseline
paper: Matryoshka Language Model Suites
role: coding
task: reimplement
by: [TalSokolov]
---

## What I reimplemented

The paper claims to improve the throughput of speculative decoding, using the 500M model as a draft model and the full 3B model as the verifier.
Throughput is measured as the output tokens per second, and is examined as a function of the draft length (the draft generates a sequence of length \gamma tokens).
See the Speculative Decoding chapter in the paper, and Figure 5a.

The key idea is that once a smaller, cheaper compute sub model (the draft) generates a sequence of length gamma based on a prefix, 
the verifier can verify the total [prefix + draft_sequence] in a single forward pass.
Testing the gamma tokens, while the verifier agrees with the draft, the output accumulates through concatenation.
Once the verifier disagrees with a draft token, the accumulation stops, "correcting" the final token with a token already calculated by the verifier though the single pass.
The complete, whether corrected or fully accumulated, step output is then again fed to the draft as the new prefix.

The draft's faster performance + single pass of the verifier should accelerate the throughput compared to the verifier alone.
Here is an implementation to test this, similar to Figure 5a.

As Matryoshka is a suite of nested models, the complete model serves as the source for all sub models (https://huggingface.co/nthngdy/matryoshka-3B)

## The code

```python
import time 
import torch 
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "nthngdy/matryoshka-3B"
DEVICE = "cuda"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision="3B_35B", trust_remote_code=True)

# load the matryoshka-3B
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    revision="3B_35B",
    trust_remote_code=True,
    torch_dtype=torch.float16,
    attn_implementation="sdpa",
    device_map="auto"
).eval()

@torch.no_grad()
def greedy_generate(model, input_ids, max_new_tokens, tag=None):
    generated = input_ids.clone()
    for _ in range(max_new_tokens):
        if tag is not None:
            logits = model.forward_up_to(tag, generated).logits
        else:
            logits = model(generated).logits
        next_token = logits[:, -1, :].argmax(dim=-1, keepdim=True)
        generated = torch.cat([generated, next_token], dim=-1)
        if next_token.item() == tokenizer.eos_token_id:
            break
    return generated

@torch.no_grad()
def speculative_generate(model, input_ids, max_new_tokens, gamma, draft_tag="500M"):
    generated = input_ids.clone()
    total_new = 0

    while total_new < max_new_tokens:
        ctx_len = generated.shape[1]

        # Draft
        draft_tokens = []
        draft_input = generated.clone()
        for _ in range(gamma):
            logits = model.forward_up_to(draft_tag, draft_input, attention_mask=None, labels=None).logits
            next_tok = logits[:, -1, :].argmax(dim=-1, keepdim=True)
            draft_tokens.append(next_tok)
            draft_input = torch.cat([draft_input, next_tok], dim=-1)
            if next_tok.item() == tokenizer.eos_token_id:
                break

        n_drafted = len(draft_tokens)
        draft_seq = torch.cat(draft_tokens, dim=-1)
        full_seq  = torch.cat([generated, draft_seq], dim=1)

        # Verify
        verify_logits = model(full_seq, attention_mask=None, labels=None).logits

        # Accept / reject
        accepted = 0
        for i in range(n_drafted):
            verifier_pred = verify_logits[:, ctx_len - 1 + i, :].argmax(dim=-1)
            if verifier_pred.item() == draft_tokens[i].item():
                accepted += 1
                total_new += 1
                if total_new >= max_new_tokens or draft_tokens[i].item() == tokenizer.eos_token_id:
                    generated = torch.cat([generated, draft_seq[:, :accepted]], dim=-1)
                    return generated
            else:
                correction = verifier_pred.unsqueeze(0)
                generated = torch.cat([generated, draft_seq[:, :accepted], correction], dim=-1)
                total_new += 1
                break
        else:
            generated = torch.cat([generated, draft_seq[:, :accepted]], dim=-1)
            bonus_tok = verify_logits[:, ctx_len - 1 + n_drafted, :].argmax(dim=-1, keepdim=True)
            if bonus_tok.item() != tokenizer.eos_token_id and total_new < max_new_tokens:
                generated = torch.cat([generated, bonus_tok], dim=-1)
                total_new += 1

    return generated

prompt = "The Roman Empire was a state that dominated the Mediterranean and much of Europe, "

inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
input_ids = inputs.input_ids
input_len = input_ids.shape[1]

# initialize cuda
_ = greedy_generate(model, input_ids, max_new_tokens=5)
torch.cuda.synchronize()

# Baseline 3B alone 

MAX_NEW = 100
torch.cuda.synchronize()
t0 = time.time()
out_base = greedy_generate(model, input_ids, max_new_tokens=MAX_NEW)
torch.cuda.synchronize()
base_time = time.time() - t0
base_tokens = out_base.shape[1] - input_len
base_speed  = base_tokens / base_time

# speculative decoding

draft_lengths = [2, 4, 6, 8, 10]
speeds, speedups = [], []

for gamma in draft_lengths:
    torch.cuda.synchronize()
    t0 = time.time()
    out_spec = speculative_generate(model, input_ids, max_new_tokens=MAX_NEW, gamma=gamma)
    torch.cuda.synchronize()
    elapsed = time.time() - t0

    n_new   = out_spec.shape[1] - input_len
    speed   = n_new / elapsed
    speedup = (speed / base_speed - 1) * 100
    speeds.append(speed)
    speedups.append(speedup)
    print(f"  γ={gamma:2d}: {n_new} tokens, {elapsed:.2f}s → {speed:.2f} tok/s | {speedup:+.1f}% vs baseline")

# plot

fig, ax1 = plt.subplots(figsize=(8, 4.5))

plt.rcParams.update({"font.family": "serif", "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 150})

ORANGE = "#E07B39"

ax1.plot(draft_lengths, speeds, color=ORANGE, marker="o", linewidth=2, markersize=5, label="Matryoshka — Greedy")
ax1.axhline(base_speed, color="black", linewidth=1.2, linestyle="-", alpha=0.5)
ax1.set_xlabel("Draft length", fontsize=11)
ax1.set_ylabel("Throughput (tokens/s)", fontsize=11)
ax1.set_xlim(-0.3, 10.3)
ax1.set_xticks([0, 2.5, 5.0, 7.5, 10.0])
ax1.legend(fontsize=9, frameon=False)
ax1.grid(True, alpha=0.25)

fig.suptitle("Matryoshka Speculative Decoding — Roman Empire Prompt", fontsize=12)
fig.tight_layout()
plt.show()
```

## Results

  γ= 2: 10.93s, 9.15 tok/s | -12.1% vs baseline
  γ= 4: 7.12s, 14.04 tok/s | +35.0% vs baseline
  γ= 6: 7.31s, 13.68 tok/s | +31.5% vs baseline
  γ= 8: 7.36s, 13.59 tok/s | +30.6% vs baseline
  γ=10: 7.44s, 13.44 tok/s | +29.2% vs baseline

  <img width="1185" height="669" alt="image" src="https://github.com/user-attachments/assets/b4f7a641-b92d-4b47-aeb3-d274ccd6480d" />

The throughput I managed to generate on Google colab GPU was significantly slower than the paper proposed:
15 tokens per second compared to thousands - this is probably due to the compute limitations.
Testing the throughput against different prompts, in many cases the throughput improved with gamma, 
but not in all cases, and sometimes even performed worse.

Some ideas as to why it does not show a stable improvement:
* I'm not sure the naive loop implemented here accounts for the cache sharing between the models  
* Single tests can not reflect batch performance
* The sequences I tested might be too short for a significant signal 

## What I learned

I was introduced to the speculative decoding concept, and learned how the Matryoshka stacking approach is a natural structure for this concept, which should enable acceleration of performance while saving compute.
I also learned implementation basics, like how to access models available on Huggingface.


