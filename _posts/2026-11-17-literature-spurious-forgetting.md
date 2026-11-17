---
title: "Literature review: where spurious forgetting comes from"
description: "The paper sits where several lines of work meet: catastrophic forgetting, forgetting that turns out to be recoverable, factual recall as associative memory, and what training choices change how much is forgotten."
paper: spurious-forgetting
role: research
task: literature
by: [Tomeratia]
---

## How I read this

I read the paper's introduction, discussion and full reference list, and I read the abstracts on arXiv of eight of the cited papers (marked with a link below). For the other references I only know what the paper says about them, and I say so. I did not run any code.

The question of the paper is *when is forgetting not catastrophic?* Its answer builds on six groups of earlier work.

## The papers this builds on

### 1. The problem: catastrophic forgetting

Training a network on new data damages what it learned before. The paper cites the classic connectionist reports (McCloskey & Cohen 1989, Ratcliff 1990, French 1999), the deep-learning versions in image classification and reinforcement learning (Goodfellow et al. 2014, Kirkpatrick et al. 2017, Zenke et al. 2017, Ramasesh et al. 2021, Rolnick et al. 2019), and the language-model versions (Luo et al. 2025, Zucchet et al. 2025, Marek et al. 2026). This is the background, and the paper's contribution is to say that part of what looks like this problem is something else.

### 2. The direct ancestors: a drop in performance is not a loss of knowledge

These are the papers the paper argues with most directly.

- **[Zheng et al. 2025, "Spurious Forgetting in Continual Learning of Language Models"](https://arxiv.org/abs/2501.13453).** This introduced the name. Their claim, from the abstract, is that performance drops often reflect a decline in *task alignment* rather than true knowledge loss, and that early optimization steps disrupt that alignment. They connect it to orthogonal updates in the weights and propose a freezing strategy. The new paper keeps the name and the setting (synthetic biographies), but looks for the *mechanism*: a common shift of the representations that normalization later withdraws. It suggests (in the discussion) that this shift "may be one concrete form" of the loss of task alignment found by Zheng et al., which is a proposal, not something it shows.
- **[Kotha et al. 2024, "Understanding Catastrophic Forgetting in Language Models via Implicit Inference"](https://arxiv.org/abs/2309.10105).** Fine-tuning skews the model's implicit inference of *which task* a prompt belongs to, and a changed prompt (conjugate prompting) recovers some lost capability. The new paper stresses that its recovery needs no special prompt, probe or replay.
- **[De Lange et al. 2023, "Continual Evaluation for Lifelong Learning: Identifying the Stability Gap"](https://arxiv.org/abs/2205.13452).** The closest relative by *shape*: after a new task starts, performance drops sharply and then recovers. They found it by evaluating after every iteration instead of after every task. The new paper cites it only in one sentence of the discussion. That is a gap, since the collapse and recovery curve looks very similar, though the setting differs (they study continual-learning methods; the new paper studies plain fine-tuning with no replay).
- **Shallow forgetting** (Murata et al. 2020, Davari et al. 2022, Hess et al. 2024, [Lanzillotta et al. 2026](https://arxiv.org/abs/2512.07400)). Networks often keep linearly separable representations of old tasks even when their outputs fail. Lanzillotta et al. call this the gap between deep (feature-level) and shallow (classifier-level) forgetting. The new paper's "hidden, not erased" claim is the same idea, applied to individual facts and explained through the weight updates.

### 3. The older roots: availability versus accessibility

The discussion places the idea in psychology: stored versus accessible information (Tulving & Pearlstone 1966; Ebbinghaus 1885) and suppressed associations returning once interference stops (Postman et al. 1968). Connectionist networks showed the same savings, and training them on *unrelated* associations could even restore forgotten ones (Hetherington & Seidenberg 1989, Hinton & Plaut 1987, Harvey & Stone 1996, Atkins & Murre 1998). These I know only from the paper's own description.

### 4. How a model stores a fact (the experimental setup)

- **Facts as associative memory.** Geva et al. 2021 (feed-forward layers as key-value memories), [Meng et al. 2022](https://arxiv.org/abs/2202.05262) (factual associations are localized in mid-layer feed-forward modules, and are editable with rank-one updates), Geva et al. 2023 and Nanda et al. 2023. The paper's minimal model is exactly a key-to-value memory.
- **Theory of such memories.** Nichani et al. 2025, Cabannes et al. 2024, Allen-Zhu & Li 2025 (capacity).
- **The data.** [Allen-Zhu & Li 2024](https://arxiv.org/abs/2309.14316) introduced the controlled synthetic biographies used here, so the experimenter knows exactly what the model knows. In the pretrained-model experiment the old facts are CounterFact facts (Meng et al. 2022), and one kind of new facts comes from EntityQuestions (Sciavolino et al. 2021).
- **[Zucchet et al. 2025, "How Do Language Models Learn Facts?"](https://arxiv.org/abs/2503.21676).** Language models learn facts in phases, and, in their words, integrating new knowledge by fine-tuning "quickly corrupts" existing parametric memories. This is closely related to the question of what fine-tuning on new facts does to old ones (my reading; the paper cites it without saying how it motivated this work).

### 5. What changes how much is forgotten

Larger learning rates cause more forgetting in continual pretraining (Gupta et al. 2023, Ibrahim et al. 2024) and in fine-tuning (Lin et al. 2026, Rofin et al. 2026), and [Springer et al. 2025](https://arxiv.org/abs/2503.19206) show that models pretrained for longer can be *harder to fine-tune*. The new paper finds that the depth of its collapse grows with the learning rate, and concludes that part of that known effect acts on forgetting that is spurious.

### 6. Tools it reuses

Saxe et al. 2019 (shared structure is learned before item-specific structure, used to explain why the common shift is withdrawn only slowly); RMSNorm (Zhang & Sennrich 2019) and pre-layer-norm Transformers (Xiong et al. 2020, Radford et al. 2019, Vaswani et al. 2017); and the OLMo 2 models (Team OLMo et al. 2025).

## The fields and concepts it connects to

| Concept | Where it comes from | Role in this paper |
| --- | --- | --- |
| Catastrophic forgetting | Continual learning | The phenomenon it tries to split in two |
| Availability vs. accessibility | Psychology of memory | The old idea behind "hidden, not erased" |
| Shallow vs. deep forgetting | Continual learning with probes | Evidence that old information survives in representations |
| Stability gap | Continual learning evaluation | A forgetting curve of the same shape |
| Factual recall as associative memory | Interpretability and theory | The minimal model and the synthetic setup |
| Normalization layers | Architecture | Usually seen as stabilizers; here they are the ingredient that withdraws the shift and causes recovery |
| Learning dynamics (shared before specific) | Theory of deep networks | Explains the slow reversal of the common shift |
| Rank-one weight edits | Model editing | The fix removes one direction of each weight update; the link to rank-one editing is my observation, not the paper's |

## What I would read first

If you have time for three: Zheng et al. 2025 (the phenomenon and its name), De Lange et al. 2023 (the same curve shape in a different setting), and Zucchet et al. 2025 (the data and the learning dynamics the setup stands on).

## What I'm unsure about

- Is the common shift of this paper the same thing as the *orthogonal update* of Zheng et al.? The paper says it "may be" a concrete form; I could not tell from the text alone.
- Where does this stand relative to the stability gap? Same shape, different setting, and only one sentence of discussion.
- Of the 2026 references, I only checked [Lanzillotta et al.](https://arxiv.org/abs/2512.07400). The other 2026 ones (for example Marek et al., arXiv:2605.26097, and Zucchet et al., arXiv:2608.15448) I only know from the paper's text.

Paper: [arXiv:2610.08718](https://arxiv.org/abs/2610.08718).
