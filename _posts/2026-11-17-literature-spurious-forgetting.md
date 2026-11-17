---
title: "Literature review: where spurious forgetting comes from"
description: "The paper sits where four lines of work meet: catastrophic forgetting, forgetting that is actually recoverable, factual recall as associative memory, and what training choices change how much is forgotten."
paper: spurious-forgetting
role: research
task: literature
by: [Tomeratia]
---

I read the paper's introduction, discussion and reference list, plus the arXiv abstracts of eight cited papers (the ones with links). For the rest I only know what the paper says about them. I ran no code.

## The papers this builds on

**The problem: catastrophic forgetting.** Training on new data damages old knowledge: classic reports (McCloskey & Cohen 1989, French 1999), deep networks (Goodfellow et al. 2014, Kirkpatrick et al. 2017) and language models (Luo et al. 2025, Zucchet et al. 2025). The paper says part of this is something else.

**The direct ancestors: a drop in performance is not a loss of knowledge.**
- [Zheng et al. 2025](https://arxiv.org/abs/2501.13453) coined "spurious forgetting": performance drops often reflect lost *task alignment*, linked to orthogonal weight updates. The new paper looks for a mechanism instead (a common shift of representations that normalization later withdraws) and only *suggests* it may be a concrete form of Zheng et al.'s task-alignment loss.
- [Kotha et al. 2024](https://arxiv.org/abs/2309.10105): fine-tuning skews which task the model infers from a prompt, and a changed prompt recovers some capability. The new paper's recovery needs no special prompt, probe or replay.
- [De Lange et al. 2023](https://arxiv.org/abs/2205.13452), the "stability gap": performance drops after a new task starts, then recovers. This is the same curve shape, but the paper cites it in one sentence only (my observation). The setting differs: they study continual-learning methods, the paper studies plain fine-tuning without replay.
- Shallow forgetting (Murata et al. 2020, Davari et al. 2022, Hess et al. 2024, [Lanzillotta et al. 2026](https://arxiv.org/abs/2512.07400)): old information stays linearly decodable even when outputs fail. The paper's "hidden, not erased" is this idea for individual facts.
- Older roots, as the paper describes them: stored versus accessible memory in psychology (Tulving & Pearlstone 1966) and recovery of forgotten associations in connectionist networks (Hinton & Plaut 1987, Atkins & Murre 1998).

**How a model stores a fact (the setup).** Feed-forward layers as key-value memories (Geva et al. 2021); [Meng et al. 2022](https://arxiv.org/abs/2202.05262) show facts are localized and editable with rank-one updates, and their CounterFact set supplies the old facts for the pretrained-model test. The controlled synthetic biographies come from [Allen-Zhu & Li 2024](https://arxiv.org/abs/2309.14316). [Zucchet et al. 2025](https://arxiv.org/abs/2503.21676) find that fine-tuning on new facts "quickly corrupts" existing ones, which is closely related to the question here (my reading, not stated by the paper).

**What changes how much is forgotten.** Larger learning rates mean more forgetting (Gupta et al. 2023, Ibrahim et al. 2024, Lin et al. 2026, Rofin et al. 2026), and [Springer et al. 2025](https://arxiv.org/abs/2503.19206) show that longer-pretrained models can be harder to fine-tune. The paper finds its collapse deepens with the learning rate and concludes part of that effect is spurious.

## The concepts it connects to

| Concept | Role in this paper |
| --- | --- |
| Catastrophic forgetting | The phenomenon it splits in two |
| Availability vs. accessibility (psychology) | The old idea behind "hidden, not erased" |
| Shallow vs. deep forgetting | Evidence that old information survives in representations |
| Stability gap | A forgetting curve of the same shape |
| Factual recall as associative memory | The minimal model and the synthetic setup |
| Normalization layers | Usually stabilizers; here they withdraw the shift and cause recovery |
| Shared structure is learned first (Saxe et al. 2019) | Explains why the shift reverses only slowly |
| Rank-one weight edits | The fix removes one direction of each update; the link to editing is my observation |

## Read first, and what I'm unsure about

Read Zheng et al. 2025 (the phenomenon), De Lange et al. 2023 (the same curve elsewhere) and Zucchet et al. 2025 (the data and dynamics).

Open questions: is the paper's common shift the same thing as Zheng et al.'s orthogonal update (the paper only says "may be")? Where does it stand relative to the stability gap? And of the 2026 references I checked only Lanzillotta et al.

Paper: [arXiv:2610.08718](https://arxiv.org/abs/2610.08718).
