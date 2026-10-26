---
title: Multi-Stream Attention Residuals
short: Multi-stream attention residuals
authors: Xiaohan Qin, Xiangdong Zhang, Tuo Dai, Sunan Zou, Huaijin Wu, Yebin Yang, Zhuo Xia, Lin Yao, Yuliang Liu, Junchi Yan
year: 2026
arxiv: "2610.13630"
license: CC BY 4.0
tldr: >
  Instead of a plain residual connection, each layer attends over the outputs of earlier layers, with several heads
  that each look at the past through a different context window. At 18B and 28B MoE scale it beats standard residuals,
  Hyper-Connections and Attention Residuals on 12 benchmarks, for a 1.58x compute speedup at equal loss.
tags: [architecture, residual connections, pretraining]
---
