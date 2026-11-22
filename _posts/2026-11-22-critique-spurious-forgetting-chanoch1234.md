---
title: "Why did OLMo recover old facts in only one experiment?"
description: "A critique of what the two OLMo training runs tell us about recovery and how to test the explanation."
paper: spurious-forgetting
role: research
task: critique
by: [chanoch1234]
---

I think the strongest result comes from the experiment with the small Transformer. After training on new facts, the model starts to favor the same set of answers across many old questions. When the authors remove this shared bias from the answer scores, the model answers most of those questions correctly again. It does this without training on the old facts a second time.

My main concern is why OLMo recovered some old facts in one experiment but not in the other. The authors train two copies of OLMo on different data. One learns facts about fictional people, such as where they work. The other learns who makes real products. Both start making mistakes on old facts. With more training, the first model gets some of those facts right again. The second does not show the same recovery.

The authors suggest that the difference comes from a clue in the new data. A fictional person’s name gives no clue about an employer chosen at random. But if the model recognizes a product as a car, it can narrow down the list of manufacturers. Favoring car companies helps it answer questions about several products, so it has a reason to keep that bias.

I find this explanation plausible, but the experiment changes two things at once: how useful the clue is and how much the model already knows about the subject. For example, the model might recognize a car and know where it is sold without knowing who makes it. Learning its manufacturer adds one fact about a familiar product. A fictional person, on the other hand, is someone the model has never seen before. From these two runs alone, we cannot tell whether recovery depends on the clue, on how familiar the subject is, or on both.

I would test this using the same fictional products and the same four manufacturers in both runs. In the first run, two companies make cameras and the other two make speakers. Knowing the product type narrows the answer down to two companies. In the second run, I would shuffle the assignments so that each company makes cameras and speakers equally often. I would keep the wording, the amount of training, and the number of examples per company the same. If accuracy on old facts recovers more in the second run, that would be stronger evidence that the clue itself affects recovery.

This matters in practice: when a model starts making mistakes on facts it used to know, the paper does not yet show how to tell whether more training will bring those answers back.
