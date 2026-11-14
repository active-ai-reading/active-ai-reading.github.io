---
title: "One text, many token sequences"
description: "The survey's core point in one figure: a language model scores token sequences, not text, so the tokenizer is part of the model rather than a preprocessing step."
paper: tokenization-survey
role: visualization
task: key-visual
by: [EylonKrause]
---

## The original

Section 2.2 makes the survey's core point in prose and one equation. A language model assigns probabilities to token sequences, while detokenization is many-to-one, so the probability of a text is the sum over all of its tokenizations,

$$p(s) = \sum_{t \in T(s)} p(t),$$

yet common practice scores only the canonical one. The survey's overview figure (Figure 1.1) draws tokenization as a single path from raw text to token IDs, so the reader has to assemble the many-to-one picture from the text and the inline "sample sentence" example, against the impression the figure gives.

## The redesign

<div markdown="0">
<svg xmlns="http://www.w3.org/2000/svg" width="100%" role="img" aria-label="One text, many token sequences: the usual one-path picture of tokenization next to the many tokenizations of the same text, whose probabilities sum to the probability of the text" style="display:block;height:auto;max-width:1200px;margin:0 auto" viewBox="0 0 1200 720" font-family="'Segoe UI', Inter, system-ui, -apple-system, Helvetica, Arial, sans-serif">
  <defs>
    <marker id="tkv-ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#6b7280"/>
    </marker>
  </defs>
  <rect width="1200" height="720" rx="18" fill="#ffffff"/>
  <text x="40" y="58" font-size="30" font-weight="700" fill="#111827">One text, many token sequences</text>
  <text x="40" y="90" font-size="17" fill="#4b5563">Language models score token sequences, not text. The tokenizer decides which of them the model ever sees.</text>
  <line x1="420" y1="124" x2="420" y2="568" stroke="#e5e7eb" stroke-width="2"/>
  <text x="40" y="140" font-size="13" font-weight="700" letter-spacing="1.5" fill="#6b7280">THE USUAL PICTURE</text>
  <rect x="70" y="164" width="300" height="44" rx="8" fill="#f9fafb" stroke="#d1d5db"/>
  <text x="220" y="192" text-anchor="middle" font-size="18" font-family="Consolas, ui-monospace, Menlo, monospace" fill="#111827">sample sentence</text>
  <line x1="220" y1="208" x2="220" y2="236" stroke="#6b7280" stroke-width="2" marker-end="url(#tkv-ah)"/>
  <rect x="120" y="240" width="200" height="44" rx="8" fill="#f3f4f6" stroke="#9ca3af"/>
  <text x="220" y="268" text-anchor="middle" font-size="17" fill="#111827">Tokenizer</text>
  <line x1="220" y1="284" x2="220" y2="312" stroke="#6b7280" stroke-width="2" marker-end="url(#tkv-ah)"/>
  <text x="232" y="303" font-size="13" font-style="italic" fill="#6b7280">fixed preprocessing</text>
  <g font-family="Consolas, ui-monospace, Menlo, monospace" font-size="17" text-anchor="middle" fill="#1e3a8a">
    <rect x="70" y="316" width="116" height="40" rx="6" fill="#dbeafe" stroke="#2563eb"/>
    <text x="128" y="342">sample</text>
    <rect x="190" y="316" width="96" height="40" rx="6" fill="#dbeafe" stroke="#2563eb"/>
    <text x="238" y="342">▁sent</text>
    <rect x="290" y="316" width="80" height="40" rx="6" fill="#dbeafe" stroke="#2563eb"/>
    <text x="330" y="342">ence</text>
  </g>
  <line x1="220" y1="356" x2="220" y2="384" stroke="#6b7280" stroke-width="2" marker-end="url(#tkv-ah)"/>
  <rect x="120" y="388" width="200" height="44" rx="8" fill="#f3f4f6" stroke="#9ca3af"/>
  <text x="220" y="416" text-anchor="middle" font-size="17" fill="#111827">Language model</text>
  <line x1="220" y1="432" x2="220" y2="460" stroke="#6b7280" stroke-width="2" marker-end="url(#tkv-ah)"/>
  <rect x="180" y="464" width="80" height="36" rx="18" fill="#ffffff" stroke="#111827"/>
  <text x="220" y="488" text-anchor="middle" font-size="18" font-weight="700" fill="#111827">p(s)</text>
  <text x="220" y="534" text-anchor="middle" font-size="15" fill="#374151">One text, one token sequence:</text>
  <text x="220" y="556" text-anchor="middle" font-size="15" fill="#374151">tokenization looks like a fixed step.</text>
  <text x="450" y="140" font-size="13" font-weight="700" letter-spacing="1.5" fill="#6b7280">WHAT THE SURVEY SHOWS (SECTION 2.2)</text>
  <text x="450" y="160" font-size="13" fill="#6b7280">the text s, character by character</text>
  <g font-family="Consolas, ui-monospace, Menlo, monospace" font-size="17" text-anchor="middle" fill="#111827">
    <rect x="450" y="166" width="34" height="34" rx="4" fill="#f9fafb" stroke="#e5e7eb"/><text x="467" y="189">s</text>
    <rect x="486" y="166" width="34" height="34" rx="4" fill="#f9fafb" stroke="#e5e7eb"/><text x="503" y="189">a</text>
    <rect x="522" y="166" width="34" height="34" rx="4" fill="#f9fafb" stroke="#e5e7eb"/><text x="539" y="189">m</text>
    <rect x="558" y="166" width="34" height="34" rx="4" fill="#f9fafb" stroke="#e5e7eb"/><text x="575" y="189">p</text>
    <rect x="594" y="166" width="34" height="34" rx="4" fill="#f9fafb" stroke="#e5e7eb"/><text x="611" y="189">l</text>
    <rect x="630" y="166" width="34" height="34" rx="4" fill="#f9fafb" stroke="#e5e7eb"/><text x="647" y="189">e</text>
    <rect x="666" y="166" width="34" height="34" rx="4" fill="#f9fafb" stroke="#e5e7eb"/><text x="683" y="189" fill="#9ca3af">␣</text>
    <rect x="702" y="166" width="34" height="34" rx="4" fill="#f9fafb" stroke="#e5e7eb"/><text x="719" y="189">s</text>
    <rect x="738" y="166" width="34" height="34" rx="4" fill="#f9fafb" stroke="#e5e7eb"/><text x="755" y="189">e</text>
    <rect x="774" y="166" width="34" height="34" rx="4" fill="#f9fafb" stroke="#e5e7eb"/><text x="791" y="189">n</text>
    <rect x="810" y="166" width="34" height="34" rx="4" fill="#f9fafb" stroke="#e5e7eb"/><text x="827" y="189">t</text>
    <rect x="846" y="166" width="34" height="34" rx="4" fill="#f9fafb" stroke="#e5e7eb"/><text x="863" y="189">e</text>
    <rect x="882" y="166" width="34" height="34" rx="4" fill="#f9fafb" stroke="#e5e7eb"/><text x="899" y="189">n</text>
    <rect x="918" y="166" width="34" height="34" rx="4" fill="#f9fafb" stroke="#e5e7eb"/><text x="935" y="189">c</text>
    <rect x="954" y="166" width="34" height="34" rx="4" fill="#f9fafb" stroke="#e5e7eb"/><text x="971" y="189">e</text>
  </g>
  <text x="450" y="226" font-size="13" font-weight="600" fill="#1d4ed8">canonical: Tokenize(s), the one sequence normally used</text>
  <g font-family="Consolas, ui-monospace, Menlo, monospace" font-size="17" text-anchor="middle" fill="#1e3a8a">
    <rect x="450" y="232" width="214" height="38" rx="6" fill="#dbeafe" stroke="#2563eb"/><text x="557" y="257">sample</text>
    <rect x="666" y="232" width="178" height="38" rx="6" fill="#dbeafe" stroke="#2563eb"/><text x="755" y="257">▁sent</text>
    <rect x="846" y="232" width="142" height="38" rx="6" fill="#dbeafe" stroke="#2563eb"/><text x="917" y="257">ence</text>
  </g>
  <text x="450" y="296" font-size="13" fill="#6b7280">non-canonical, same text</text>
  <g font-family="Consolas, ui-monospace, Menlo, monospace" font-size="17" text-anchor="middle" fill="#374151">
    <rect x="450" y="302" width="70" height="38" rx="6" fill="#f3f4f6" stroke="#9ca3af"/><text x="485" y="327">sa</text>
    <rect x="522" y="302" width="34" height="38" rx="6" fill="#f3f4f6" stroke="#9ca3af"/><text x="539" y="327">m</text>
    <rect x="558" y="302" width="106" height="38" rx="6" fill="#f3f4f6" stroke="#9ca3af"/><text x="611" y="327">ple</text>
    <rect x="666" y="302" width="178" height="38" rx="6" fill="#f3f4f6" stroke="#9ca3af"/><text x="755" y="327">▁sent</text>
    <rect x="846" y="302" width="70" height="38" rx="6" fill="#f3f4f6" stroke="#9ca3af"/><text x="881" y="327">en</text>
    <rect x="918" y="302" width="70" height="38" rx="6" fill="#f3f4f6" stroke="#9ca3af"/><text x="953" y="327">ce</text>
  </g>
  <text x="450" y="366" font-size="13" fill="#6b7280">non-canonical, same text</text>
  <g font-family="Consolas, ui-monospace, Menlo, monospace" font-size="17" text-anchor="middle" fill="#374151">
    <rect x="450" y="372" width="214" height="38" rx="6" fill="#f3f4f6" stroke="#9ca3af"/><text x="557" y="397">sample</text>
    <rect x="666" y="372" width="106" height="38" rx="6" fill="#f3f4f6" stroke="#9ca3af"/><text x="719" y="397">▁se</text>
    <rect x="774" y="372" width="70" height="38" rx="6" fill="#f3f4f6" stroke="#9ca3af"/><text x="809" y="397">nt</text>
    <rect x="846" y="372" width="70" height="38" rx="6" fill="#f3f4f6" stroke="#9ca3af"/><text x="881" y="397">en</text>
    <rect x="918" y="372" width="70" height="38" rx="6" fill="#f3f4f6" stroke="#9ca3af"/><text x="953" y="397">ce</text>
  </g>
  <text x="450" y="442" font-size="14" font-style="italic" fill="#9ca3af">⋮  and many more ways to spell the same text</text>
  <g font-size="17" text-anchor="end">
    <text x="1060" y="257" fill="#1e3a8a" font-weight="600">p(t₁)</text>
    <text x="1060" y="327" fill="#374151">+ p(t₂)</text>
    <text x="1060" y="397" fill="#374151">+ p(t₃)</text>
    <text x="1060" y="442" fill="#9ca3af">+ …</text>
  </g>
  <path d="M1068 234 H1076 V450 H1068" fill="none" stroke="#111827" stroke-width="2"/>
  <text x="1086" y="348" font-size="19" font-weight="700" fill="#111827">= p(s)</text>
  <text x="450" y="494" font-size="18" fill="#111827"><tspan font-weight="700">p(s) = Σ p(t)</tspan> over every token sequence t with Detokenize(t) = s</text>
  <text x="450" y="524" font-size="16" fill="#4b5563">In common practice p(s) ≈ p(Tokenize(s)): only the canonical path is counted.</text>
  <text x="40" y="600" font-size="16" font-weight="700" fill="#111827">Because the tokenizer decides what the model sees, it also sets:</text>
  <g font-size="14" fill="#4b5563">
    <rect x="40" y="614" width="274" height="80" rx="10" fill="#f9fafb" stroke="#e5e7eb"/>
    <text x="56" y="642" font-size="15" font-weight="700" fill="#111827">Sequence length</text>
    <text x="56" y="664">compute and price</text>
    <text x="56" y="683">of every query</text>
    <rect x="322" y="614" width="274" height="80" rx="10" fill="#f9fafb" stroke="#e5e7eb"/>
    <text x="338" y="642" font-size="15" font-weight="700" fill="#111827">Parameter budget</text>
    <text x="338" y="664">embeddings + output layer:</text>
    <text x="338" y="683">59.8% of Gemma 4 E2B</text>
    <rect x="604" y="614" width="274" height="80" rx="10" fill="#f9fafb" stroke="#e5e7eb"/>
    <text x="620" y="642" font-size="15" font-weight="700" fill="#111827">Cost per language</text>
    <text x="620" y="664">non-English users</text>
    <text x="620" y="683">pay for more tokens</text>
    <rect x="886" y="614" width="274" height="80" rx="10" fill="#f9fafb" stroke="#e5e7eb"/>
    <text x="902" y="642" font-size="15" font-weight="700" fill="#111827">Evaluation</text>
    <text x="902" y="664">perplexity is not comparable</text>
    <text x="902" y="683">across tokenizers</text>
  </g>
</svg>
</div>

*Left: the usual picture, in which text passes through a fixed tokenizer to a single token sequence. Right: the same text spelled three ways, using the example and tokenizations from Section 2.2 (▁ marks a word-initial space). The probability of the text is the sum over all of them, but in common practice only the canonical one is scored.*

