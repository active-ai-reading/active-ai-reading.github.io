"""Turn the probe output into compact JSON for the figures: per-token exits, KL curves, PCA trajectories."""
import json, sys
import numpy as np

D = sys.argv[1]
R = json.load(open(f"{D}/results.json"))
out = {}
for name in ["apples", "westphalia"]:
    r = R[name]
    toks = r["prompt_tokens"]
    lat = np.load(f"{D}/latents_{name}.npy").astype(np.float32)        # steps x S x 5280
    T, S, H = lat.shape
    # trajectory stats per position: movement on late trips relative to early trips
    d = np.linalg.norm(lat[1:] - lat[:-1], axis=-1)                     # (T-1) x S
    late = d[-8:].mean(0); early = d[:8].mean(0)
    pca = {}
    for p in range(S):
        X = lat[:, p] - lat[:, p].mean(0, keepdims=True)
        U, s, Vt = np.linalg.svd(X, full_matrices=False)
        xy = (U[:, :2] * s[:2])
        Xl = lat[32:, p] - lat[32:, p].mean(0, keepdims=True)
        Ul, sl, _ = np.linalg.svd(Xl, full_matrices=False)
        pca[p] = dict(xy=np.round(xy, 3).tolist(), var=np.round((s[:2] ** 2 / (s ** 2).sum()), 3).tolist(),
                      xy_late=np.round(Ul[:, :2] * sl[:2], 3).tolist(), var_late=np.round((sl[:2] ** 2 / (sl ** 2).sum()), 3).tolist(),
                      step_norm=np.round(np.linalg.norm(lat[:, p], axis=-1), 2).tolist(), move=np.round(d[:, p], 3).tolist())
    out[name] = dict(prompt_tokens=toks, prompt_exit=r["prompt_exit"],
                     prompt_kl=[[kl[p] for kl in r["prompt_kl"]] for p in range(S)],     # S x T
                     late_over_early=np.round(late / early, 3).tolist(), late_move=np.round(late, 3).tolist(),
                     generated=[dict(token=g["token"], exit=g["exit"], exited=g["exited"], kl=g["kl"]) for g in r["generated"]],
                     answer=r["answer"], pca=pca)
    print(name, "answer:", repr(r["answer"]))
    for p in range(S):
        print(f"  {p:2d} {toks[p]!r:16} exit={str(r['prompt_exit'][p]):>4}  late/early={late[p]/early[p]:.3f} late={late[p]:.2f}  pc var={pca[p]['var']}")
    for g in r["generated"]:
        print(f"  gen {g['token']!r:12} exit={g['exit']} exited={g['exited']}")
out["official"] = R.get("official")
json.dump(out, open(f"{D}/figdata.json", "w"))
print("official:", R.get("official"))
