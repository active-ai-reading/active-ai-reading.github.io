---
title: What are these evals anyway?
description: We discuss evals in general, evals in the MSAR paper and the OpenCompass evaluation platforms
paper: multi-stream-attention-residuals
role: learning
task: teach
by: [IdoRavid]
---

## Why should we care about evals?

Many pretraining papers, or more broadly papers that propose a new LLM training method,
claim their method "outperforms" all the alternatives they compare against. The paper we are reading this week is no exception.

The evaluation process, although it might feel technical and dry at times, provides the central (and sometimes single) place to judge such claims about model performance. Verifying that the evaluation process does what it claims to do, is a central part of reading the paper.

This post briefly goes over the main things to look out for in model evaluation, in this paper and in general.

## What are these Evals anyway?

**Evaluations** (or just evals) are ways to test a model's capabilities on particular tasks. A **metric** is the scoring rule, such as the percentage of questions answered correctly. A **benchmark** provides a standardized set of tasks or questions and a protocol for evaluating performance on them.

Modern LLMs are designed to be versatile. We expect Claude to help us debug our code, think of birthday gifts for grandma, select the best washing machine cycle, and know the capital city of Palau (it's Ngerulmud, btw).
Since we expect state-of-the-art models to be a kind of "everything machine", benchmarking them on a wide range of tasks is inevitable. It's also what makes evaluation difficult.

## Which model is in question?

One key distinction about evaluation should be- which type of models are we evaluating? pretrained models, such as the ones in this paper, may lack a wide range of capabilities that are introduced during post-training (either via SFT, RLHF or RLVR).
We know for example, that conversationalist abilities, as well as mathematical and reasoning capabilities, are improved significantly during post-training (In fact, this accounts for some of the major improvements of LLMs in recent years).

Pretrained LLMs are still expected to have various capabilities - general knowledge, math solving and language understanding, for example.

## Main evaluation approaches 

We can broadly divide evals into two types - look directly at output probabilities (say, which answer the model scores highest), or we could let the model generate an answer (say, a sentence), and check what it said.


**Likelihood-based evaluation** is the first approach. We give the model a question and several optional answers with a score. Then we let the model predict the next token, and see how it rated each answer.


{% include figure.liquid path="assets/img/posts/but-what-are-these-evals-anyway/llm_tk_1.BVI0TDSU_1F5u4t.webp" class="img-fluid rounded bg-white" alt="A multiple-choice question is passed to an LLM, and the next-token probabilities are compared for the answer labels." %}

(From HuggingFace's Evaulation Guidebook.)

This is useful for base models, especially smaller models or early training checkpoints, where following the answer format can itself be a challenge.

We can, alternatively, measure perplexity on some held out test set. This is in a way the metric that fits best the original task the pretrained models trained for. It does not, however, test a SPECIFIC capability as we might want.



**Generation-based evaluation**  justlets the model write an answer. Grading that answer is the difficult part.
We then need a way to grade it. 
For some tasks, such as math or code, we can evaluate the answer directly (checking the final math answer against the reference, unit tests for a script etc).
Other more open-ended tasks may require a human/llm as judges.

in generation-based eval we often use few-shot prompting to steer the model by showing it what we expect.

## Evals used in this paper

We can split the benchmarks used in this paper into 3 categories, following the authors' grouping: general capabilities, code and math, and Chinese language understanding.

 The type, scoring and shots refer to how they are used **in this paper**, according to [Appendix A](https://arxiv.org/pdf/2610.13630#page=16). year marks the paper publication year for a given benchmark.

### General capabilities

This is where we test things like general knowledge, science questions and reasoning across different domains.

| Benchmark | Introduced | Type and metric | What is tested | Shots |
| --- | --- | --- | --- | --- |
| [MMLU](https://arxiv.org/abs/2009.03300) | 2020 | Likelihood; accuracy | Knowledge and problem solving across 57 subjects | 5 |
| [MMLU-Pro](https://arxiv.org/abs/2406.01574) | 2024 | Generation; answer accuracy | More reasoning-focused questions, with up to 10 options | 5 |
| [MMLU-Redux](https://arxiv.org/abs/2406.04127) | 2024 | Likelihood; accuracy | A manually checked and corrected subset of MMLU | 5 |
| [ARC-C](https://arxiv.org/abs/1803.05457) | 2018 | Likelihood; accuracy | The challenging subset of grade-school science questions | 25 |
| [BBH](https://arxiv.org/abs/2210.09261) | 2022 | Generation; answer accuracy | A collection of 23 challenging reasoning tasks | 3 |

For the likelihood tasks, the selected answer is the one with the lowest conditional perplexity.

**An actual ARC-C example** ([training set, `ACTAAP_2009_7_4`](https://huggingface.co/datasets/allenai/ai2_arc/viewer/ARC-Challenge/train)):

> Which planet has the longest planetary year?
>
> A. Earth<br>
> B. Venus<br>
> C. Jupiter<br>
> D. Neptune

The reference answer is **D, Neptune**. We score the candidates, select one, and check whether it matches the reference. There is no requirement that the correct answer receive more than 50% probability; it needs to rank highest under the scoring rule.

### Code and math

Here we let the model produce a solution. For math we check its answer, and for code we can actually run what it wrote.

| Benchmark | Introduced | Type and metric | What is tested | Shots |
| --- | --- | --- | --- | --- |
| [HumanEval](https://arxiv.org/abs/2107.03374) | 2021 | Generation; pass@1 | Writing Python functions from descriptions | 0 |
| LCBench | Not clearly identified | Generation; pass@1 | Code tasks; see the note below | 5 |
| [GSM8K](https://arxiv.org/abs/2110.14168) | 2021 | Generation; answer accuracy | Grade-school math word problems | 4 |
| [MATH](https://arxiv.org/abs/2103.03874) | 2021 | Generation; answer accuracy | Competition math problems | 4 |

For code, pass@1 measures how often a single sampled solution passes the tests. This is different from generating many solutions and accepting any one that works.

**An actual GSM8K example** ([test set, question 306](https://github.com/openai/grade-school-math/blob/master/grade_school_math/data/test.jsonl#L306)):

> John arm wrestles 20 people.  He beats 80%.  How many people did he lose to?

The reference answer is **4**: he beats 16 people and loses to the other 4. The model generates a solution, and the scorer checks its final answer. Getting the final number right doesn't guarantee that every step of the explanation was correct.

**An actual HumanEval example** ([`HumanEval/55`, from the original dataset](https://github.com/openai/human-eval/blob/master/data/HumanEval.jsonl.gz)):

```python
def fib(n: int):
    """Return n-th Fibonacci number.
    >>> fib(10)
    55
    >>> fib(1)
    1
    >>> fib(8)
    21
    """
```

This is the prompt, including the examples the model gets to see. The model needs to complete the function body. The evaluator then runs the completed function against the task's tests, including additional inputs that weren't in the prompt.

The paper lists "LCBench" without specifying its version or evaluation period.

### Chinese language understanding

The first two benchmarks test knowledge and reasoning in Chinese. C3 adds reading comprehension: we give the model a passage and ask questions about it.

| Benchmark | Introduced | Type and metric | What is tested | Shots |
| --- | --- | --- | --- | --- |
| [CMMLU](https://arxiv.org/abs/2306.09212) | 2023 | Likelihood; accuracy | Knowledge across subjects, including Chinese cultural contexts | 5 |
| [C-Eval](https://arxiv.org/abs/2305.08322) | 2023 | Likelihood; accuracy | Chinese exam questions across subjects and education levels | 5 |
| [C3](https://arxiv.org/abs/1904.09679) | 2019 | Likelihood; accuracy | Chinese reading comprehension | 3 |

**An actual C3 example** ([dialogue development set, `36-3`](https://github.com/nlpdata/c3/blob/master/data/c3-d-dev.json#L16012)):

> 男：请问这里有牛奶吗?<br>
> 女：有，在水果旁边。
>
> 男的现在可能在哪儿?
>
> 家里 / 车上 / 商店里

For those of us who don't read Chinese, here is an English translation:

> Man: Excuse me, is there milk here?<br>
> Woman: Yes, next to the fruit.
>
> Where is the man most likely now?
>
> At home / In a vehicle / In a shop

The reference answer is **商店里 (in a shop)**. The dialogue doesn't explicitly say "we are in a shop", so the model needs to infer the location from the conversation. The model receives the Chinese version; the translation here is just for us.

### Why these evals specifically? (and what's missing)

The paper does not explain the reason for choosing these benchmarks.
It does, however, select benchmark families that focus on key areas of interest in pretrained models - geneeral knowledge, math, lanugage understanding.

There is, notably, some overlap between benchmarks - three MMLU versions, plus CMMLU, and a clear focus on Chinese.

One key point is about evals NOT in the paper - since the new architecture in question is focused on improving the residual stream, we might expect to see better in-context information retrieval.

One benchmark that could test this is [RULER](https://arxiv.org/abs/2404.06654), specifically its retrieval tasks. These ask the model to find information within an input containing irrelevant text, with different input lengths and numbers of facts to retrieve.

## OpenCompass: what is that?

[OpenCompass](https://opencompass.readthedocs.io/en/latest/user_guides/framework_overview.html) is an evaluation framework.
The platform takes care of the plumbing needed for high-scale evaluation with multiple models and multiple benchamrks - it takes care of: loading questions, formatting prompts, running inference, extracting answers, grading them and collecting the results.

For example. for a GSM8K-style evaluation, the workflow should look like this:

1. Choose the model, dataset split, prompt and generation settings.
2. Build each prompt, including any solved examples.
3. Let the model generate a response.
4. Extract the final answer and compare it with the reference answer.
5. Aggregate the question scores into a benchmark score.

The configuration controls these choices, so the same dataset can have several evaluation setups.

The authors use a lightweight suite based on OpenCompass. The steps above describe the general workflow; Appendix A documents their task-level choices, including 4-shot generation for GSM8K.

## What these scores leave out

There are a few things missing here:

- These scores don't isolate the improvement in in-context retrieval we might expect.

- Benchmarks like MMLU can suffer from **saturation** and **contamination**. Saturation is when scores get so similar, often near the ceiling, that the test stops telling models apart. A test that's too easy for frontier models can still be useful for the base models here. Contamination is when test material ends up in training data, so the model may already know the exam. This is a [documented concern for MMLU](https://aclanthology.org/2024.naacl-long.482/), and the paper doesn't report a contamination check.

- [Anthropic recommends](https://www.anthropic.com/research/statistical-approach-to-model-evals) reporting uncertainty, sampling multiple responses for stochastic generation, and comparing models' results on the same questions using paired statistics. The paper reports scores without error bars and doesn't report those paired statistics or generation sample counts. We can't tell whether these practices were used, which makes the smaller score differences harder to judge.

## Sources and further reading

- [Hugging Face: The LLM Evaluation Guidebook](https://huggingface.co/spaces/OpenEvals/evaluation-guidebook)
- [Anthropic: A statistical approach to model evaluations](https://www.anthropic.com/research/statistical-approach-to-model-evals)
- [OpenCompass: Workflow and Core Concepts](https://opencompass.readthedocs.io/en/latest/user_guides/framework_overview.html)
