---
title: The core idea in one picture
description: Same sentence, same model, different token IDs, and the knowledge stops flowing. A diagram of the three setups.
paper: cross-lingual-knowledge-pretraining
role: visualization
task: key-visual
by: [course-team]
example: true
_styles: >
  .tok-diagram { display: grid; gap: 1.25rem; margin: 1.5rem 0; font-family: var(--course-sans); }
  .tok-row { border: 1px solid var(--global-divider-color); border-radius: 12px; padding: 0.9rem 1rem; }
  .tok-row h4 { font-size: 1rem; font-weight: 700; margin: 0 0 0.6rem; }
  .tok-line { display: flex; flex-wrap: wrap; align-items: center; gap: 0.35rem; margin: 0.3rem 0; }
  .tok-lang { width: 6.5rem; font-size: 0.8rem; color: var(--global-text-color-light); }
  .tok { display: inline-flex; flex-direction: column; align-items: center; padding: 0.15rem 0.5rem; border-radius: 6px; font-size: 0.9rem; border: 1px solid; }
  .tok small { font-size: 0.68rem; opacity: 0.8; font-family: monospace; }
  .tok.a { background: #2f6fde1a; border-color: #2f6fde66; }
  .tok.b { background: #e8590c1a; border-color: #e8590c66; }
  .tok.shared { background: #0c8a5f1a; border-color: #0c8a5f88; }
  .tok-verdict { margin-top: 0.5rem; font-size: 0.92rem; }
  .tok-verdict b { font-variant-numeric: tabular-nums; }
---

The paper has one idea you can draw: **knowledge flows between languages only through tokens they share, and only if those tokens mean the same thing.** Three setups show it. Blue and orange are separate token spaces; green is a shared one. The small numbers are token IDs (with a vocabulary of size V). Words are shown left to right in reading order.

<div class="tok-diagram">
<div class="tok-row">
<h4>1. English₁ – English₂: identical text, disjoint token IDs</h4>
<div class="tok-line"><span class="tok-lang">English₁</span>
<span class="tok a">The<small>464</small></span><span class="tok a">cat<small>3797</small></span><span class="tok a">sleeps<small>22118</small></span>
</div>
<div class="tok-line"><span class="tok-lang">English₂</span>
<span class="tok b">The<small>V+464</small></span><span class="tok b">cat<small>V+3797</small></span><span class="tok b">sleeps<small>V+22118</small></span>
</div>
<div class="tok-verdict">Same words, same grammar, same data. Only the IDs differ. Knowledge transfer: <b>CLeq ≈ −2.6%</b> (none).</div>
</div>
<div class="tok-row">
<h4>2. English – WWT-Arabic: Arabic grammar, English tokens</h4>
<div class="tok-line"><span class="tok-lang">Arabic</span>
<span class="tok b">ينام<small>Ar-ID</small></span><span class="tok b">القط<small>Ar-ID</small></span>
</div>
<div class="tok-line"><span class="tok-lang">WWT-Arabic</span>
<span class="tok shared">sleeps<small>22118</small></span><span class="tok shared">the cat<small>464 3797</small></span>
</div>
<div class="tok-verdict">Each Arabic word is replaced by its English translation, keeping Arabic word order (verb first). The tokens are now shared and mean the same. Transfer: <b>0.9% → 12.6%</b>.</div>
</div>
<div class="tok-row">
<h4>3. Controls: shared tokens, wrong meanings</h4>
<div class="tok-line"><span class="tok-lang">Shuffled dict.</span>
<span class="tok shared">window<small>4324</small></span><span class="tok shared">idea<small>2126</small></span>
</div>
<div class="tok-line"><span class="tok-lang">Transliterated</span>
<span class="tok shared">ynAm<small>…</small></span><span class="tok shared">AlqT<small>…</small></span>
</div>
<div class="tok-verdict">Same token inventory, but the shared tokens no longer carry the same meaning. Transfer collapses: <b>3.0%</b> (shuffled) and <b>−0.3%</b> (transliteration).</div>
</div>
</div>

<p class="muted">The token IDs and the two-word Arabic example are illustrative, not taken from the paper's tokenizer. The paper's own WWT example is below.</p>

{% include figure.liquid path="assets/img/papers/cross-lingual-knowledge-pretraining/vocabulary_mapping_table.png" class="img-fluid rounded z-depth-1" caption="The paper's Table 1 (CC BY 4.0): an Arabic sentence, its WWT-Ar rendering and an English translation. WWT-Ar is Arabic written in English tokens, not a translation." %}

## Why this picture

The paper's Figure 1 shows *results* (bars). A reader who hasn't read Section 5 can't tell what "English₁–English₂" or "WWT" even are. A diagram of the inputs explains the experiments in five seconds, and makes the conclusion feel obvious in hindsight, which is what a good key figure does.

**Ideas for doing better:** animate it (the same sentence morphing between setups), or add a fourth row with soft mapping, where each token pair shares only part of its embedding.

Numbers from {% cite gaber2026crosslingual %}.
