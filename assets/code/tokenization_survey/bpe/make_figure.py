import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = json.load(open("results.json"))
fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
e3 = R["E3"]
m = [r["merges"] for r in e3]
ax[0].plot(m, [r["iterative_s"] for r in e3], "o-", label="Code 3.2 (iterative: try every merge)")
ax[0].plot(m, [r["priority_s"] for r in e3], "s-", label="Code 3.3 (priority: only merges that apply)")
ax[0].set_xscale("log"); ax[0].set_xlabel("number of merges in the list"); ax[0].set_ylabel("seconds to tokenize 3,000 words")
ax[0].set_title("Iterative inference slows with the merge list")
for r in e3:
    ax[0].annotate(f"{r['ratio']:.0f}x", (r["merges"], r["iterative_s"]), textcoords="offset points", xytext=(-4, 6), fontsize=8)
ax[0].legend(fontsize=8)
e4 = R["E4"]
ax[1].plot([r["merges"] for r in e4], [r["chars_per_token"] for r in e4], "o-", color="#e45756")
ax[1].set_xlabel("number of merges applied"); ax[1].set_ylabel("characters per token (held-out book)")
ax[1].set_title("Compression grows with more merges")
plt.tight_layout(); plt.savefig("bpe_inference_and_compression.png", dpi=150)
