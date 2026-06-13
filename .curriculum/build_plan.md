# 01 · BUILD PLAN — what to build, what to ship, in what order

Build-focused. Goal in one line: **a verifiable, public, adopted body of
from-scratch work that makes the author an obvious fit for a frontier LLM-infra
or agentic-tooling role.** Order, scope, and the per-phase exit bar below were
restructured against a deep-research pass on how people actually reached those
roles (the local goal dossier); per-phase thresholds and dates live in the local
rubric.

Tags: **[CORE]** buys both roles (do first) · **[INFRA]** infra tail · **[AGENTS]**
agents tail · **[DEST]** the destination.
Calibration: 🔨 full build · 🧩 reimplement core · 📖 conversant (no build).

**The exit bar (changed — read this first).** A phase is **not done at "harness
green."** It is done when it has shipped **one *published* artifact with a
benchmark number against a named strong baseline** (cuBLAS / FlashAttention-2 /
vLLM / a reference provider) **plus a measurement write-up.** Every documented
career break in the dossier came from a public, adopted, benchmarked artifact —
never a private repo of passing tests. The harness is the *learning* gate; the
published+benchmarked artifact is the *career* gate. Both are required.

---

## The four always-on tracks (run in parallel with every phase)

The build alone is necessary but not sufficient — the dossier's clearest finding.
From day one, in parallel:

1. **Publish** — a named public repo + a measurement write-up (the
   Dettmers/Horace-He "what I measured" genre) per shipped phase.
2. **OSS** — work toward a **merged PR into a flagship project** (vLLM / SGLang /
   PyTorch / llama.cpp / TRL / an RL-environments stack). A merged vLLM/SGLang PR
   is a **gated deliverable of Phase 2.3**, not a footnote. This is a documented
   hiring channel and the external validation a private repo can't give.
3. **Papers** — 2–3/week tied to the active phase, logged in
   `research_map.md` with a 3-sentence critique + "what I'd extend" (this is the
   research-discussion interview format).
4. **Apply** — screenable systems / agent-tooling roles **now**, in parallel
   (classical-systems depth already clears their hard requirements); inference and
   RE-RL roles when the shared core lands (~month 6). Applying is a track, not the
   finish line.

---

## TIER 0 — Math→Code [CORE]
**0.1 Autograd from scratch 🔨** — scalar → tensor reverse-mode autodiff
(broadcasting) → linear/softmax/cross-entropy/layernorm by hand. **Hard-capped at
2 weeks** — only the tensor/broadcasting backward is worth the full from-scratch
treatment; do not gold-plate scalar autograd. **Ship: gradient-check suite +
RESULTS.md (grads match finite-diff & PyTorch).**

## TIER I — Internals [CORE]
**1.1 Transformer from scratch 🔨** — BPE → attention → MHA → causal mask → GPT
block → train loop → sampling → load GPT-2 weights & generate. ≤2 wk. **Ship:
coherent generation from real weights + tok/s, published.**
**1.2 Architecture zoo 🔨/🧩** — 🔨 RoPE (reproduce extrapolation failure, fix
w/ interpolation) · 🔨 GQA/MQA (measure KV reduction) · 🔨 RMSNorm/SwiGLU · 🧩 MoE
top-k routing. ≤2 wk. **Ship: attention-variant writeup with measured KV deltas +
RoPE failure curve.**

## TIER II — Systems (the highest-signal tier for this goal — front-loaded)
**2.3 Inference systems 🔨 [CORE]✦** — KV cache → HTTP server → continuous
batching → 🧩 paged-KV allocator → 🧩 **KV quantization (INT8/FP8, with
perplexity-vs-throughput numbers)** → 🧩 **speculative decode (draft model +
acceptance-rate benchmark)**. Exposes an **OpenAI-compatible API → System A of the
capstone.** ≤8 wk.
  - **Allowed-dependency boundary (resolves the old 2.1-before-2.3 contradiction):
    library kernels (flash-attn / torch / triton) ARE permitted here.** A
    production-parity educational engine (cf. nano-vllm, ~1200 LOC, zero custom
    CUDA) does not require hand-written kernels first. The from-scratch rule
    applies to the *serving logic* (cache, scheduler, allocator, batching), not to
    re-deriving GEMM.
  - **Read** vLLM / SGLang source *after* the harness is green (post-acceptance
    consolidation) — labs list "familiarity with vLLM/SGLang/TensorRT-LLM/Triton"
    as a basic requirement; this converts "built my own" into "fluent in the named
    frameworks" without touching the no-AI-code rule.
  - **Ship: server w/ continuous batching + paged KV + quant + spec-decode,
    throughput/latency table benchmarked against vLLM (not just cuBLAS), published
    as a standalone named project. Gated co-deliverable: a merged vLLM/SGLang PR.**
    This is the single highest-leverage artifact in the plan (the gpt-fast effect).

**2.1 GPU/CUDA/kernels 🔨 [INFRA] — COMPRESSED, promoted into the core (was tail).**
naive → tiled matmul (vs cuBLAS) → fused softmax → flash-forward kernel (vs FA2).
≤6 wk. Kernel-level performance is the most-cited infra entry signal and this
author's highest-leverage differentiator as a C/C++ systems engineer. **Ship:
kernel throughput vs cuBLAS/FA2 + roofline; then swap the own-kernel into the 2.3
server as a measurable before/after artifact.** A Triton port of one kernel is a
named posting requirement — do it here.

**2.2 Distributed training 🔨/🧩 [INFRA] — thin slice into the core; rest in tail.**
Core (≤2 wk): 🔨 data-parallel all-reduce on a rented 2–4-GPU node — "multi-GPU
experience" is in the hiring bar. Tail: 🔨 ZeRO-1 optimizer-state sharding → 🧩
tensor-parallel a linear layer → 📖 pipeline/3D. **Ship (core): a 2–4-GPU scaling
data point; (tail): scaling curve + memory-vs-sharding table.**

## TIER III — Capability
**3.2 Post-training & RL 🔨/🧩 [CORE]✦** — 🔨 SFT → 🔨 inference-time reasoning
(self-consistency/best-of-n) → 🧩 DPO → 🔨 PPO/GRPO on a verifiable reward, wired
to the 4.3 eval harness as reward oracle; make the rollout loop **async** (rollout
workers feeding a trainer — a named nice-to-have). Ports the author's fuzzer
credit-assignment work (DQN/bandits) to token/tool-call action spaces — a genuine,
uncommon prior that maps onto the credential-optional RE-RL track. ≤8 wk. **Ship:
before/after eval curves + credit-assignment writeup bridging from DQN/bandits,
published.**
**3.1 Data + small-scale pretraining 🧩/📖 [INFRA] — demoted.** ≤2-wk llm.c-style
GPT-2 reproduction-with-a-twist, or drop. **Ship (if kept): loss curve matching a
public reference.**
**3.3 Interp & safety 📖 [INFRA] — conversant-only.** Read logit-lens / SAE
internals; build nothing unless an interview pipeline demands it. Resist scope
growth.

## TIER IV — Agents [AGENTS]
**4.1 Agent harness from scratch 🔨** — ReAct from raw API → tool dispatch
(schema/validation/error-surfacing/retries) → context engineering
(compaction/filesystem-memory/recovery) → sub-agent spawning. Backend-agnostic →
**System B of the capstone.** Build a thin eval here; fold a trivial retrieval
layer in rather than building 4.2. **Ship: zero-framework harness completing an
over-context task, trajectories logged, published.**
**4.2 Memory & retrieval 📖/🧩 [AGENTS] — demoted to conversant-only.** Read
HNSW/faiss internals; a brute-force vector layer inside 4.1 is enough. Build the
full HNSW/RAG stack only if a target role demands it.
**4.3 Evals: the binding constraint 🔨 [CORE]✦** — task spec + **sandboxed
deterministic execution built on real isolation primitives (namespaces, seccomp,
cgroups — not subprocess mocks; this doubles as evidence for agent-runtime/
sandboxing roles)** + partial credit → LLM-as-judge + calibration + failure modes
→ trajectory eval (tool-efficiency/recovery/cost) → reproduce a real-benchmark
slice → CI regression gating. A **thin** version lands in the shared core (≤2 wk);
expand later. **Ship: rerunnable scorecard.** *Lead the portfolio with this — the
author's fuzzing ablation discipline is the unfair advantage.*

## TIER V — Integration (the capstone) [CORE]
Full spec in `capstone_architecture.md`. **Externally less legible than a merged
vLLM PR or a kernel-leaderboard entry (dossier X9) — it is not the hiring lead.**
Run it only if the application pipeline is still cold when the core + tracks are
done; otherwise freeze and keep shipping standalone artifacts + OSS.
**5.0 Capstone contract 🔨** — OpenAI-compatible interface + one deliberate leak
(token timing/logprobs); stub both ends day one. **Ship: contract spec +
conformance harness.**
**5.1 Production layer 🔨/🧩** — 🔨 MCP server+client · 🔨 observability · 🧩
guardrails · 🧩 caching/rate-limits · 🧩 multi-agent orchestration · 📖 one
framework, learned last, to critique. **Ship: deployed MCP system with
observability.**
**5.2 Capstone integration 🔨** — System A (your engine) + System B (your agent) +
the seam. **Ship: substitution benchmark (your agent on a reference provider vs
your engine — eval/TTFT/TPOT/throughput/$) + cross-seam RL curve.** This benchmark
must produce a genuinely new measurement (the dossier's bar for "novel result").

## TIER VI — Novelty [DEST]
**Prerequisite:** a shipped capstone + (most likely) an intermediate seat.
Matters mainly for the DeepMind/Meta research-scientist tail, which is the weakest
target for a no-publication candidate — **deprioritized** relative to shipping
2–5 publicly. **Mechanism:** from `gaps_log.md`, attack a gap at systems × RL ×
agents (lead candidate: RL credit assignment over long-horizon tool-use
trajectories). **Ship: a falsifiable novel result + reproducible numbers + public
writeup.**

---

## Order (execute this)

**Shared core, restructured (~4–7 months at 40 h/wk):**
`0.1 → 1.1 → 1.2 → 2.3 → 2.1-compressed → thin-2.2 → thin-4.3 → 3.2`.
2.3 ships first as the flagship and OSS-PR vehicle; 2.1 follows and swaps its
kernel back into 2.3; the thin 2.2 / 4.3 slices buy the multi-GPU + evals signals
cheaply. **Until offers stabilize, run only this core** + the four always-on
tracks. The **application trigger is ~month 6 (core shipped), not plan
completion** — every phase after that must ship a public artifact so the gap reads
as a portfolio.

**Then** extend the tail the pipeline heats up (infra: full 2.2 → 3.1 → 3.3-read ·
agents: 4.1 → 4.3-full → 5.1), then the capstone *only if still needed*
(5.0 → 5.1 → 5.2), then Tier VI.

## Hard dependencies
`0.1 → 1.1 → (1.2, 2.x)`. **2.3 does NOT require 2.1** (library kernels permitted;
the old "2.1 precedes 2.3" line was wrong and is removed). 2.1's own-kernel
*optionally* swaps into 2.3 afterward. `2.2` enables full `3.1`. `3.2` consumes
`4.3` as reward oracle (thin eval inside 4.1/core, expanded in 4.3). The capstone
consumes `2.3 + 4.1 + 4.3 + 3.2`.

## Per-phase ceilings (over ceiling → cut scope, never extend; log the cut)
0.1 ≤2 wk · 1.1 ≤2 wk · 1.2 ≤2 wk · 2.3 ≤8 wk · 2.1-compressed ≤6 wk ·
thin-2.2 ≤2 wk · thin-4.3 ≤2 wk · 3.2 ≤8 wk. Thresholds/dates: the local rubric.

## Definition of done (per the rubric, not phase count)
1. Shared core shipped — each phase **public + benchmarked vs a named baseline +
   write-up**.
2. ≥1 flagship artifact with an external signal; ≥1 merged flagship-OSS PR; paper
   cadence sustained; closed-book retention bank current; interview-mode reps
   logged; application pipeline open.
3. The offer is the *outcome* of those indicators — see the rubric's honest
   "what guarantee means" statement. It is not guaranteed by completing phases.
