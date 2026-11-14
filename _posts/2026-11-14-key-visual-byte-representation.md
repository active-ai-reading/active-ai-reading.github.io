---
title: "Byte-Level Modeling and Latent Tokenization - Chapter 9"
description: A side-by-side view of how byte-level approaches differ in the way they group input into latent representations
paper: tokenization-survey
role: visualization
task: key-visual
by: [NettaShemesh103]
chart:
  chartjs: true # enables ```chartjs code blocks. Also available: echarts, plotly, vega_lite (see the showcase)
---

### Byte-Level Modeling and Latent Tokenization

**Process text at the byte level, with different ways to group bytes into latent tokens for more efficient processing.**

<table>
<thead>
<tr><th align="left">Method</th><th align="center">Byte input</th><th align="center">Internal representation</th><th align="left">Principle</th></tr>
</thead>
<tbody>
<tr><th align="left">Pure Byte-Level</th><td align="center"><kbd>T</kbd><kbd>h</kbd><kbd>e</kbd><kbd>_</kbd><kbd>q</kbd><kbd>u</kbd><kbd>i</kbd><kbd>c</kbd><kbd>k</kbd><kbd>_</kbd><kbd>f</kbd><kbd>o</kbd><kbd>x</kbd></td><td align="center">→&nbsp; <kbd>T</kbd><kbd>h</kbd><kbd>e</kbd><kbd>_</kbd><kbd>q</kbd><kbd>u</kbd><kbd>i</kbd><kbd>c</kbd><kbd>k</kbd><kbd>_</kbd><kbd>f</kbd><kbd>o</kbd><kbd>x</kbd></td><td>Processes each byte individually.</td></tr>
<tr><th align="left">Fixed-Width</th><td align="center"><kbd>T</kbd><kbd>h</kbd><kbd>e</kbd><kbd>_</kbd><kbd>q</kbd><kbd>u</kbd><kbd>i</kbd><kbd>c</kbd><kbd>k</kbd><kbd>_</kbd><kbd>f</kbd><kbd>o</kbd><kbd>x</kbd></td><td align="center">→&nbsp; <kbd>The_</kbd> <kbd>quic</kbd> <kbd>k_fo</kbd> <kbd>x</kbd></td><td>Groups bytes into fixed-size latent tokens.</td></tr>
<tr><th align="left">Whitespace-Based</th><td align="center"><kbd>T</kbd><kbd>h</kbd><kbd>e</kbd><kbd>_</kbd><kbd>q</kbd><kbd>u</kbd><kbd>i</kbd><kbd>c</kbd><kbd>k</kbd><kbd>_</kbd><kbd>f</kbd><kbd>o</kbd><kbd>x</kbd></td><td align="center">→&nbsp; <kbd>The_</kbd> <kbd>quick_</kbd> <kbd>fox</kbd></td><td>Uses whitespace-based boundaries.</td></tr>
<tr><th align="left">Entropy-Based</th><td align="center"><small>Illustrative next-byte entropy:</small><br><code>▁▂▁▁▇▁▁▁▂▁▇▁▁</code><br><kbd>T</kbd><kbd>h</kbd><kbd>e</kbd><kbd>_</kbd><kbd>q</kbd><kbd>u</kbd><kbd>i</kbd><kbd>c</kbd><kbd>k</kbd><kbd>_</kbd><kbd>f</kbd><kbd>o</kbd><kbd>x</kbd></td><td align="center">→&nbsp; <kbd>The_</kbd> <kbd>quick_</kbd> <kbd>fox</kbd></td><td>Creates latent tokens at entropy spikes.</td></tr>
<tr><th align="left">Learned Dynamic</th><td align="center"><kbd>T</kbd><kbd>h</kbd><kbd>e</kbd><kbd>_</kbd><kbd>q</kbd><kbd>u</kbd><kbd>i</kbd><kbd>c</kbd><kbd>k</kbd><kbd>_</kbd><kbd>f</kbd><kbd>o</kbd><kbd>x</kbd></td><td align="center">→&nbsp; <kbd>The_quick_</kbd> <kbd>fox</kbd></td><td>Learns where to place latent-token boundaries.</td></tr>
</tbody>
</table>

*Figure X. A comparison of pure byte-level modeling and four latent-tokenization strategies using the same illustrative input, `The quick fox` (with `_` representing a space). Grouped units stand for **internal latent representations**, not conventional vocabulary tokens. Entropy-based and learned segmentations, including the entropy profile, are schematic rather than measured outputs from specific models.*
