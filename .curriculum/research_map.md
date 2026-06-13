# RESEARCH_MAP — living taxonomy + primary-source reading list (update as you read; never finished)

Depth target: GENUINE in Systems(train+infer), Post-training/RL, Agents, Evals · CONVERSANT elsewhere.

The anchors below are the primary sources — the papers/docs the field itself
cites, chosen because the matching phase builds the thing the paper describes.
Read each as its phase approaches (the brief will assume the vocabulary), and
log every stated-but-unproven assumption you notice into `gaps_log.md`. Add what
you read; replace anchors with better ones as you find them. **Never read
reference *implementations* of a component before its phase is accepted.**

**Paper cadence (an always-on track, not passive reading).** 2–3 papers/week
tied to the active phase. Log each here with a 3-sentence critique +
"what I'd extend." This is deliberate prep for the frontier-lab research-discussion
interview round (a paper sent 2–3 days before; discuss contribution / method /
limits / extensions) — the exact format. The log itself is the evidence of
fluency.

## Foundations (Tier 0)
- Baydin, Pearlmutter, Radul, Siskind — *Automatic Differentiation in ML: a Survey* (JMLR 2018) — https://arxiv.org/abs/1502.05767
- Ba, Kiros, Hinton — *Layer Normalization* (2016) — https://arxiv.org/abs/1607.06450
- Goodfellow, Bengio, Courville — *Deep Learning*, ch. 6–8 — https://www.deeplearningbook.org/

## Architectures (attention variants, MoE, hybrid/SSM, long-context) — Tiers 1.1/1.2
- Vaswani et al. — *Attention Is All You Need* (2017) — https://arxiv.org/abs/1706.03762
- Radford et al. — *Language Models are Unsupervised Multitask Learners* (GPT-2, 2019) — the weights Phase 1.1 loads
- Sennrich et al. — *BPE for NMT* (2015) — https://arxiv.org/abs/1508.07909
- Su et al. — *RoFormer* (RoPE, 2021) — https://arxiv.org/abs/2104.09864
- Ainslie et al. — *GQA* (2023) — https://arxiv.org/abs/2305.13245
- Zhang & Sennrich — *RMSNorm* (2019) — https://arxiv.org/abs/1910.07467 · Shazeer — *GLU Variants* (SwiGLU, 2020) — https://arxiv.org/abs/2002.05202
- Fedus et al. — *Switch Transformers* (MoE routing, 2021) — https://arxiv.org/abs/2101.03961

## Training systems (parallelism, precision, optimizers, data) — Tier 2.1/2.2
- Dao et al. — *FlashAttention* (2022) — https://arxiv.org/abs/2205.14135
- Shoeybi et al. — *Megatron-LM* (tensor parallelism, 2019) — https://arxiv.org/abs/1909.08053
- Rajbhandari et al. — *ZeRO* (2019) — https://arxiv.org/abs/1910.02054
- Micikevicius et al. — *Mixed Precision Training* (2017) — https://arxiv.org/abs/1710.03740

## Inference (batching, paging, speculation, quantization, disaggregation) — Tier 2.3
- Yu et al. — *Orca: continuous batching* (OSDI 2022) — https://www.usenix.org/conference/osdi22/presentation/yu
- Kwon et al. — *PagedAttention / vLLM* (SOSP 2023) — https://arxiv.org/abs/2309.06180
- Leviathan et al. — *Speculative Decoding* (2022) — https://arxiv.org/abs/2211.17192 · Chen et al. — *Accelerating LLM Decoding with Speculative Sampling* (2023) — https://arxiv.org/abs/2302.01318
- Dettmers et al. — *LLM.int8()* (2022) — https://arxiv.org/abs/2208.07339 · Frantar et al. — *GPTQ* (2022) — https://arxiv.org/abs/2210.17323 · Lin et al. — *AWQ* (2023) — https://arxiv.org/abs/2306.00978  *(quantization is a named basic qualification on inference postings — not optional)*
- Zheng et al. — *SGLang / RadixAttention* (2023) — https://arxiv.org/abs/2312.07104  *(read the source post-acceptance; labs require framework familiarity)*
- gpt-fast (PyTorch, 2023) — https://pytorch.org/blog/accelerating-generative-ai-2/ · nano-vllm — https://github.com/GeeeekExplorer/nano-vllm  *(existence proofs: vLLM-class serving with library kernels, no custom CUDA)*

## Post-training (SFT, preference opt, RL, reasoning, distillation, PRMs) — Tier 3.2
- Ouyang et al. — *InstructGPT* (RLHF, 2022) — https://arxiv.org/abs/2203.02155
- Schulman et al. — *PPO* (2017) — https://arxiv.org/abs/1707.06347
- Rafailov et al. — *DPO* (2023) — https://arxiv.org/abs/2305.18290
- Shao et al. — *DeepSeekMath* (GRPO, 2024) — https://arxiv.org/abs/2402.03300

## Data + pretraining — Tier 3.1
- Kaplan et al. — *Scaling Laws* (2020) — https://arxiv.org/abs/2001.08361 · Hoffmann et al. — *Chinchilla* (2022) — https://arxiv.org/abs/2203.15556
- Leskovec, Rajaraman, Ullman — *Mining of Massive Datasets*, ch. 3 (MinHash/LSH) — http://www.mmds.org/

## Agents/harness (context engineering, recovery, orchestration, protocols) — Tier 4.1/4.2/5.x
- Yao et al. — *ReAct* (2022) — https://arxiv.org/abs/2210.03629
- Malkov & Yashunin — *HNSW* (2016) — https://arxiv.org/abs/1603.09320
- Lewis et al. — *RAG* (2020) — https://arxiv.org/abs/2005.11401
- Model Context Protocol spec — https://modelcontextprotocol.io/specification

## Evals (benchmarks, judges, contamination, trajectory scoring) — Tier 4.3
- Zheng et al. — *Judging LLM-as-a-Judge* (MT-Bench, 2023) — https://arxiv.org/abs/2306.05685
- Jimenez et al. — *SWE-bench* (2023) — https://arxiv.org/abs/2310.06770

## Interpretability & safety (circuits, SAEs, probing, alignment, red-teaming) — Tier 3.3
- *Towards Monosemanticity* (SAEs, 2023) — https://transformer-circuits.pub/2023/monosemantic-features
- nostalgebraist — *the logit lens* (2020) — https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens
