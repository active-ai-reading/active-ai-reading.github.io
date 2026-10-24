### Handoff - Coding (Reimplement) - week 2

**What I tried.** A toy-scale version of the paper's main experiment: one transformer with three exits (2 layers @64 → +2 @128 → +2 @256) vs. three separate models of matched parameter count. Pure PyTorch, CPU, char-level text from a small grammar. About 25 minutes of training in total. Post: `2026-10-24-matryoshka-toy.md`; code: github.com/liadber/matryoshka-toy.

**What was harder than expected.** The baseline, not the paper's method. The first run compared each exit to a separate model with the same depth *and width* — not parameter-matched, and not what the paper does (Table 1). The large baseline also didn't converge, partly because I ran two trainings at once on one CPU. That run said the nested model was "20% better". It wasn't; the baseline was broken. Fix: match parameters per size, add warmup + gradient clipping, lower the learning rate, run one thing at a time.

**What I'd tell the next person.**
- Decide before running what the toy *can* claim (the shape of a result) and what it can't (the paper's numbers), and write that paragraph of the post first. It keeps you honest when a number looks too good.
- - Save every run under its own tag (`results_<tag>.json`, `curves_<tag>.png`). I overwrote my first figure and had to re-run.
  - - If the corpus is too easy, every model size reaches the same loss and there is nothing to compare. Add long-range dependencies (agreement across a clause, a name copied to the end of the sentence) so model size matters.
    - - No GPU needed. Two-million-parameter models on a CPU are enough to see the mechanism; they are not enough to say anything about 3B.
      - 
