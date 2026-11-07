---
title: "LearningHarness: Optimize your learning with AI"
description: My experience using an AI learning tool to read this paper.
paper: recurrent-depth-latent-reasoning
role: learning
task: teach
by: AdamJaber03
---

I've decided to focus my learning post this week on a tool I've recently been exposed to called Learning Harness. This tool, which plugs into your preferred LLM, promises to streamline learning using AI, allowing you to focus your time on the critical learning stage, where you can gain the most. The tool breaks down the learning objective into smaller, manageable steps, avoiding the usual "wall of text" encountered when trying to learn something new with LLMs.

Here I'll share my experience learning this week's paper and its surrounding context using LearningHarness:

The learning process begins with your request. I asked: "I want to be prepared and brought up to speed to read this paper. I want to know anything that the standard reader this paper is intended for should know before diving in and then I want you to walk me through the paper completely so that I know all the important details (not looking to reimplement this or anything, but I want to understand the mechanisms ideas and any math such that I could intelligently participate in a discussion on the paper)".

Next comes the probing stage. To identify your current knowledge and personalize an efficient learning plan, the model tests your knowledge in different areas related to the requested lesson. The harness allows you to record your thoughts and confidance while going through these questions, helping it identify the edges of your knowledge. The questions adapt to your previous answers and recorded thinking. This process took about an hour for me and included 20 questions, and should take less once previous learning sessions have already built a good understanding of your preexisting knowledge.

Once mapping what you already know has been completed, the harness designs a tree of ideas/logical-steps towards your learning goal and the dependency relations between them:

<img width="1000" alt="image" src="https://github.com/user-attachments/assets/de9cd208-3037-4727-bd9c-2f675fa654d4" />


Learning begins. The model will walk you through one idea at a time. Providing short explanations followed by a question meant to check your understanding or build intuition towards the next point.
Example learning step:
<img width="1000" alt="image" src="https://github.com/user-attachments/assets/141022aa-b6e7-463b-9e63-72d03234a161" />

### What I liked
1. The harness pulls additional resources from various online sources/papers so that it doesn't only walk you through the paper but also through the motivation.
2. Being able to record your thinking and answers allows much better communication of the gaps in your understanding. Sometimes answering a question might be easy from context but you can point out that some details of the question and or definitions around it are unclear.
3. The small learning steps are great, they truly are almost atomic pieces of knowledge. This makes learning more fun than just reading a long page of text, and provides much more friction points to test understanding.
4. where gaps in the paper exist, like failed runs that aren't addressed or explained. The model tries to provide intuition, clearly admitting it doesn't exist in the paper.

### What I didn't like
1. Bugs: sometimes the agent fails to output the correct format, resulting in some learning text missing or tables/graphs not being properly rendered.
2. Not enough visualizations. seems like there's supposed to be an animator agent functionality but I didn't really get to see it in action much.
3. The paper is rarely directly cited, making it at times unclear what information is grounded in the paper and what isn't.

##TLDR
LearningHarness is a cool tool showing a lot of potential in optimizing learning in the AI era. While still unpolished, it offers great value in making a more unique and interactive learning experience than online research.
It seems to me this tool would be most suited for learning topics that aren't grounded in a single paper, but are spread across many sources and can be combined into a single line of knowledge. I will keep using LearningHarness and I reccoment you try it too

## Learn more
[link to youtube video](https://youtu.be/nfTDljFG2g0?si=SYwoECEsHuzUjD7C)

[link to github repo to download](https://github.com/amosblomqvist/learnharness)

Shout-out to David Plotkin for introducing me to this tool.
