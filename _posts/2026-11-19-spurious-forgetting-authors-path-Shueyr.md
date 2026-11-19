---
layout: post
title: "The authors’ path: Spurious forgetting"
description: "How the authors’ research on mechanistic interpretability, representation learning, and learning dynamics connects to spurious forgetting."
paper: spurious-forgetting
role: research
task: authors
by: [Shueyr]
---

### Vedant Palit

Vedant Palit is a machine learning researcher at the Max Planck Institute for Intelligent Systems, collaborating with Zhijing Jin's research group at the University of Toronto. His research focuses on mechanistic interpretability, particularly understanding how language models and vision-language models represent and process information internally. His previous work includes developing causal tracing methods for multimodal models and investigating the internal circuits responsible for learned concepts and reasoning.

*When Forgetting is not Catastrophic* fits directly into his research interests by investigating the internal mechanisms responsible for forgetting in language models. Rather than treating forgetting solely as a loss of learned knowledge, the paper examines how changes in internal representations can temporarily prevent models from accessing information that remains stored. This builds on his broader interest in understanding model behavior through mechanistic analysis and identifying how internal representations influence performance.

### Florent Draye

Florent Draye is a PhD researcher at the Max Planck Institute for Intelligent Systems, supervised by Bernhard Schölkopf. His research focuses on mechanistic interpretability, representation learning, and causal structures in neural networks. He is particularly interested in understanding the internal representations learned by large language models, including their world models and how these representations change through training. His work also includes developing tools for analyzing neural circuits and investigating how interpretable features emerge within models.

*When Forgetting is not Catastrophic* connects closely to his research on representation learning and mechanistic interpretability. The paper investigates how fine-tuning changes the internal representations of previously learned facts and distinguishes between temporary shifts that make knowledge inaccessible and changes that permanently damage stored information. This aligns with his broader goal of understanding how neural networks organize information and how their internal representations affect model behavior.

### Nicolas Zucchet

Nicolas Zucchet is a postdoctoral researcher at Stanford University whose work focuses on machine learning, computational neuroscience, and neural network learning dynamics. He previously completed his PhD at ETH Zürich and conducted research at Google DeepMind. His research investigates how neural networks learn, store, and organize information, including how training data and learning curricula influence model behavior. His previous work includes studying how language models acquire factual knowledge, how attention mechanisms emerge, and how different learning strategies affect neural networks.

*When Forgetting is not Catastrophic* is closely related to his previous research on how language models learn facts. In particular, his paper *How Do Language Models Learn Facts? Dynamics, Curricula and Hallucinations* studies how factual knowledge is acquired during training. The new paper extends this line of investigation by examining what happens to previously learned facts when models are trained on new information. Both works seek to understand the learning dynamics underlying factual knowledge rather than evaluating models only through their final performance.

### Zhijing Jin

Zhijing Jin is an assistant professor of computer science at the University of Toronto and a research scientist at the Max Planck Institute for Intelligent Systems. Her research focuses on large language models, causal inference, mechanistic interpretability, and AI safety. She is particularly interested in understanding how language models reason, how their internal representations influence behavior, and how causal methods can help explain and improve their capabilities. Her previous work includes developing benchmarks for causal reasoning and investigating the mechanisms underlying model behavior.

*When Forgetting is not Catastrophic* aligns with her research through its use of mechanistic analysis to explain language model behavior. The paper moves beyond observing that fine-tuning causes forgetting and instead investigates the representational changes responsible for this behavior. By identifying mechanisms that distinguish reversible forgetting from genuine knowledge loss, the work connects to her broader interest in explaining model behavior through internal representations and causal interventions.

### Bernhard Schölkopf

Bernhard Schölkopf is a prominent machine learning researcher and director of the Empirical Inference Department at the Max Planck Institute for Intelligent Systems. His research has made significant contributions to statistical learning theory, kernel methods, and causal inference. More recently, his work has emphasized causal representation learning, which aims to understand how models can discover meaningful underlying structures in data rather than relying only on statistical correlations. His broader research seeks to improve the interpretability, robustness, and generalization capabilities of machine learning systems.

*When Forgetting is not Catastrophic* connects to his research on representation learning and the mechanisms underlying neural network behavior. The paper shows that apparent forgetting can arise from shared shifts in learned representations without necessarily destroying the information they encode. This distinction relates to his broader interest in understanding how learned representations influence model behavior and generalization. By developing a simplified mathematical model and testing its predictions through interventions, the work also reflects his emphasis on explaining machine learning phenomena through underlying mechanisms rather than observations alone.
