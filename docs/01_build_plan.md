# 01 · BUILD PLAN — what to build, what to ship, in what order

Build-focused. The reasoning behind these choices is settled; this doc is the map you execute. Goal in one line: **a verifiable body of from-scratch work that makes you an obvious fit for both a frontier LLM-infra role and an agentic-AI-tooling team — and a launchpad for a novel result.**

Tags: **[CORE]** buys both roles (do first) · **[INFRA]** infra tail · **[AGENTS]** agents tail · **[DEST]** the destination.
Calibration: 🔨 full build · 🧩 reimplement core · 📖 conversant (no build).
**Every phase ships the one artifact named in bold. No phase is "done" without it.**

---

## TIER 0 — Math→Code [CORE]
**0.1 Autograd from scratch 🔨** — scalar → tensor reverse-mode autodiff (broadcasting) → linear/softmax/cross-entropy/layernorm by hand. **Ship: gradient-check suite + RESULTS.md (grads match finite-diff & PyTorch).**

## TIER I — Internals [CORE]
**1.1 Transformer from scratch 🔨** — BPE → attention → MHA → causal mask → GPT block → train loop → sampling → load GPT-2 weights & generate. **Ship: coherent generation from real weights + tok/s.**
**1.2 Architecture zoo 🔨/🧩** — 🔨 RoPE (reproduce extrapolation failure, fix w/ interpolation) · 🔨 GQA/MQA (measure KV reduction) · 🔨 RMSNorm/SwiGLU · 🧩 MoE top-k routing. **Ship: attention-variant writeup with measured KV deltas + RoPE failure curve.**

## TIER II — Systems
**2.1 GPU/CUDA/kernels 🔨 [INFRA]** — naive → tiled matmul (vs cuBLAS) → fused softmax → FlashAttention-style fused kernel. **Ship: kernel throughput vs cuBLAS + roofline.**
**2.2 Distributed training 🔨/🧩 [INFRA]** — 🔨 data-parallel via all-reduce → 🔨 ZeRO-1 optimizer-state sharding → 🧩 tensor-parallel a linear layer → 📖 pipeline/3D. **Ship: scaling curve + memory-vs-sharding table.**
**2.3 Inference systems 🔨 [CORE]✦** — KV cache → HTTP server → continuous batching → 🧩 paged-KV allocator → 🧩 KV quantization → 🧩 speculative decode. Exposes an **OpenAI-compatible API → becomes System A of the capstone.** **Ship: server w/ continuous batching + paged KV + throughput/latency table.** (Strongest: a vLLM contribution.)

## TIER III — Capability
**3.1 Data + small-scale pretraining 🔨/🧩 [INFRA]** — 🔨 dedup (MinHash/LSH) → 🧩 tokenizer training → 🔨 pretrain a small model. **Ship: loss curve matching a public reference.**
**3.2 Post-training & RL 🔨/🧩 [CORE]✦** — 🔨 SFT → 🔨 inference-time reasoning (self-consistency/best-of-n) → 🧩 DPO → 🔨 PPO/GRPO on a verifiable reward, wired to the 4.3 eval harness as reward oracle. (Ports your fuzzer credit-assignment work to token/tool-call action spaces.) **Ship: before/after eval curves + credit-assignment writeup bridging from DQN/bandits.**
**3.3 Interp & safety 🧩/📖 [INFRA]** — 🧩 logit lens + activation probing → 🧩 train an SAE. **Ship: SAE writeup surfacing interpretable features.**

## TIER IV — Agents [AGENTS]
**4.1 Agent harness from scratch 🔨** — ReAct from raw API → tool dispatch (schema/validation/error-surfacing/retries) → context engineering (compaction/filesystem-memory/recovery) → sub-agent spawning. Backend-agnostic → **System B of the capstone.** Build a thin eval here. **Ship: zero-framework harness completing an over-context task, trajectories logged.**
**4.2 Memory & retrieval 🔨/🧩** — 🔨 brute-force vector search → 🧩 HNSW core → 🔨 RAG into harness → 🧩 episodic+semantic memory w/ write/forget. **Ship: recall@k/latency vs baseline + retrieval-quality eval (separate from generation) + agent-success A/B.**
**4.3 Evals: the binding constraint 🔨 [CORE]✦** — task spec + sandboxed deterministic execution + partial credit → LLM-as-judge + calibration + failure modes → trajectory eval (tool-efficiency/recovery/cost) → reproduce a real-benchmark slice → CI regression gating. **Ship: rerunnable scorecard.** *Lead the portfolio with this — your fuzzing ablation discipline is the unfair advantage.*

## TIER V — Integration (the capstone) [CORE]
Full spec in `02_capstone_architecture.md`. Two independently-excellent systems joined by a load-bearing contract.
**5.0 Capstone contract 🔨** — write the OpenAI-compatible interface + one deliberate leak (token timing/logprobs) BEFORE deepening either side; stub both ends. **Ship: contract spec + conformance harness validating both ends independently.**
**5.1 Production layer 🔨/🧩** — 🔨 MCP server+client · 🔨 observability (traces/cost-latency/failure clustering) · 🧩 guardrails/permission boundary · 🧩 caching/rate-limits/degradation · 🧩 multi-agent orchestration · 📖 one framework, learned last, to critique. **Ship: deployed MCP system with observability.**
**5.2 Capstone integration 🔨** — System A (your inference engine, optionally serving a model you RL-tuned) + System B (your agent in your fuzzing/DB domain) + the seam. **Ship: substitution benchmark (same agent: reference provider vs your engine — eval/TTFT/TPOT/throughput/$) + cross-seam RL curve (reward from B's evals tunes model served by A).** Done = benchmark runs green.

## TIER VI — Novelty [DEST]
**Prerequisite:** Tiers 0–V + a shipped capstone. **Mechanism:** from `always_on/GAPS_LOG.md`, attack a gap at systems × RL × agents. **Lead candidate:** RL credit assignment over long-horizon tool-use trajectories with verifiable rewards (open frontier + a direct port of your fuzzer expertise). **Ship: a falsifiable novel result — method + reproducible numbers + public writeup.** Unschedulable by nature; the plan delivers you armed.

---

## Order (execute this)
1. **Shared core first (do regardless of which role's interviews land):** 0.1 → 1.1 → 1.2 → 2.3 → thin 4.3 → 3.2. Every hour buys both roles.
2. **Extend the tail the pipeline heats up:** infra → 2.1 → 2.2 → 3.1 → 3.3 · agents → 4.1 → 4.2 → 4.3(full) → 5.1.
3. **Capstone:** 5.0 → 5.1 → 5.2 (contract-first).
4. **Novelty:** Tier VI, fed by the gaps log you kept throughout.
**Until job offers stabilize, run ONLY the Phase-1 shared core.** It's the no-regret, most interview-legible investment.

## Hard dependencies
0.1 → 1.1 → (1.2, 2.x). 2.1 precedes 2.3. 2.2 enables 3.1. 3.2 consumes 4.3 as reward oracle (build a thin eval inside 4.1, expand in 4.3). Capstone consumes 2.3 + 4.1–4.3 + 3.2.

## Definition of done
1. Every Tier 0–V phase's named build artifact is shipped (harness green, RESULTS.md published, stranger can rerun).
2. Portfolio links: ≥3 paper reproductions w/ matching numbers; ≥2 merged OSS contributions (one infra, one agents); from-scratch artifacts with public benchmarks; the capstone (substitution benchmark + cross-seam RL curve).
3. Critique a framework against your primitives + whiteboard a multi-GPU serving stack.
4. `GAPS_LOG.md` has a live candidate you're attacking — ideally one shipped novel result.
