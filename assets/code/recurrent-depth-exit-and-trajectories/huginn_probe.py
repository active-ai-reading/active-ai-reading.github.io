"""Step the Huginn-0125 recurrence by hand and record, for every token position:
  * the KL divergence between the next-token distributions of successive trips,
  * the trip at which the paper's exit rule (KL < 5e-4) would stop,
  * the latent state after every trip (for trajectory plots).
Then generate an answer greedily, one token at a time, exiting each token at its own trip.
Outputs: results.json + latents_<name>.npy in the directory given as argv[1].
"""
import json, os, sys, time
import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
MODEL = "tomg-group-umd/huginn-0125"
THR = 5e-4
MAX_STEPS = 64
MAX_NEW = 24
dev = "mps" if torch.backends.mps.is_available() else "cpu"
print("device", dev, flush=True)

tok = AutoTokenizer.from_pretrained(MODEL)
from transformers.dynamic_module_utils import get_class_from_dynamic_module
Raven = get_class_from_dynamic_module("raven_modeling_minimal.RavenForCausalLM", MODEL)
Raven._tied_weights_keys = {"lm_head.weight": "transformer.wte.weight"}      # transformers>=5 wants a dict
model = Raven.from_pretrained(MODEL, dtype=torch.bfloat16, trust_remote_code=True).to(dev).eval()
print("loaded", flush=True)
STOP = {tok.convert_tokens_to_ids(t) for t in ["<|end_text|>", "<|end_turn|>"]} | {65505}
V = model.config.vocab_size


@torch.no_grad()
def run_loop(ids, max_steps=MAX_STEPS, thr=THR, keep_latents=False, seed=0):
    """Run the recurrence on the whole sequence; return per-position stats."""
    torch.manual_seed(seed)
    S = ids.shape[1]
    emb, block_idx = model.embed_inputs(ids)
    x = model.initialize_state(emb)
    prev_lp = torch.full((S, V), -np.log(V), device=dev)
    exit_step = [None] * S
    kl_hist, argmax_hist, lat = [], [], []
    for step in range(max_steps):
        x, block_idx, _ = model.iterate_one_step(emb, x, block_idx=block_idx, current_step=step)
        lp = torch.log_softmax(model.predict_from_latents(x).logits[0].float(), -1)
        kl = (prev_lp.exp() * (prev_lp - lp)).sum(-1)          # KL(prev || new), as in KLExitEvaluator
        kl_hist.append(kl.cpu().tolist())
        argmax_hist.append(lp.argmax(-1).cpu().tolist())
        for p in range(S):
            if exit_step[p] is None and kl[p].item() < thr:
                exit_step[p] = step + 1
        if keep_latents:
            lat.append(x[0].float().cpu().numpy())
        prev_lp = lp
    return dict(exit_step=exit_step, kl=kl_hist, argmax=argmax_hist, latents=np.stack(lat) if keep_latents else None)


def probe(name, prompt_ids):
    t0 = time.time()
    S = prompt_ids.shape[1]
    r = run_loop(prompt_ids, keep_latents=True)
    np.save(f"{OUT}/latents_{name}.npy", r["latents"].astype(np.float16))
    prompt_tokens = [tok.decode([i]) for i in prompt_ids[0].tolist()]
    out = dict(prompt_tokens=prompt_tokens, prompt_exit=r["exit_step"], prompt_kl=r["kl"], prompt_argmax_last=[a[-1] for a in r["argmax"]],
               generated=[])
    print(name, "prompt exits", list(zip(prompt_tokens, r["exit_step"])), f"{time.time() - t0:.0f}s", flush=True)
    seq = prompt_ids
    for t in range(MAX_NEW):
        rr = run_loop(seq, keep_latents=False, seed=1000 + t)
        last = seq.shape[1] - 1
        es = rr["exit_step"][last] or MAX_STEPS
        tid = rr["argmax"][es - 1][last]
        tid_full = rr["argmax"][-1][last]
        out["generated"].append(dict(token=tok.decode([tid]), id=tid, exit=es, exited=rr["exit_step"][last] is not None,
                                     token_at_64=tok.decode([tid_full]), kl=[k[last] for k in rr["kl"]]))
        print(f"  gen {t}: {tok.decode([tid])!r} exit={es} (at 64: {tok.decode([tid_full])!r}) {time.time() - t0:.0f}s", flush=True)
        if tid in STOP:
            break
        seq = torch.cat([seq, torch.tensor([[tid]], device=dev)], 1)
    out["answer"] = tok.decode([g["id"] for g in out["generated"] if g["id"] not in STOP])
    return out


results = {}
msgs = [{"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tom has 12 apples and buys 29 more. How many apples does he have now?"}]
chat = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
ids = tok.encode(chat, return_tensors="pt", add_special_tokens=False).to(dev)
results["apples"] = probe("apples", ids)

ids = tok.encode("The capital of Westphalia is", return_tensors="pt", add_special_tokens=True).to(dev)
results["westphalia"] = probe("westphalia", ids)

# cross-check with the authors' own adaptive-compute generator (may not work on this transformers version)
try:
    from transformers import GenerationConfig
    cfg = GenerationConfig(max_length=ids.shape[1] + MAX_NEW, stop_strings=["<|end_text|>", "<|end_turn|>"], use_cache=True, do_sample=False,
                           temperature=None, top_k=None, top_p=None, min_p=None, return_dict_in_generate=True,
                           eos_token_id=65505, bos_token_id=65504, pad_token_id=65509)
    ids = tok.encode(chat, return_tensors="pt", add_special_tokens=False).to(dev)
    o = model.generate_with_adaptive_compute(ids, cfg, num_steps=MAX_STEPS, tokenizer=tok, continuous_compute=False, criterion="kl",
                                             exit_threshold=THR, cache_kwargs={"lookup_strategy": "latest-m4"})
    text = tok.decode(o.sequences[0][ids.shape[1]:])
    steps = [int(s[0][0]) if hasattr(s[0], "__len__") else int(s[0]) for s in o.scores]
    results["official"] = dict(text=text, steps=steps)
    print("official:", text, steps, flush=True)
except Exception as e:
    results["official"] = dict(error=repr(e))
    print("official generate failed:", repr(e), flush=True)

json.dump(results, open(f"{OUT}/results.json", "w"), indent=1)
print("DONE", flush=True)
