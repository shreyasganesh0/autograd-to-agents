# Capstone Architecture — Two Systems, One Contract

**Owner:** Shreyas
**Status:** Expands v5 §5.2. This is the README/spec for the end-goal project.
**Design thesis:** Two independently-excellent systems — an **inference/serving substrate** (infra moat) and a **backend-agnostic agentic tool** (agentic moat) — composed into one product through a **load-bearing standard interface**. Each half stands alone as a portfolio piece; the seam is itself the union artifact. Depth is maximized per half; the accepted tradeoff is effort (~1.7x scope) and an upfront contract commitment.

---

## 0. Why two-deep beats one-hybrid (the reframe)

A monolithic capstone that must "run on inference you built, use kernels you wrote, be tuned with RL you implemented, exposed via MCP, measured by evals" subordinates every component to a single narrative. Real depth in kernels/serving has a different *shape* than real depth in harnesses/evals; forcing both into one story compromises both, and the result reads as "jack of both" to a specialist reviewer.

Two standalone-deep systems + a real seam is strictly better:
- **Legibility.** An infra reviewer reads System A on its own terms; an agentic reviewer reads System B; a full-stack reviewer reads the seam. Nothing is diluted for the others.
- **Depth.** Each system is optimized for its own correctness and benchmark, not for fitting a unifying demo.
- **Honesty.** It mirrors how production systems are actually composed: excellent components behind clean interfaces.

**The relabel:** not "two projects larping as one" — *two systems composing into one product*. "Larping" implies pretense; the whole point is to make the integration real so it isn't pretense.

---

## 1. The load-bearing-seam test (the rule that prevents cosmetic integration)

The seam must pass **both**:
1. **Standalone test.** Delete the seam — is each half still excellent on its own? Must be **yes** (that's the standalone depth).
2. **Load-bearing test.** Does the seam carry real traffic / data / signal — not just a README claim? Must be **yes** (that's the real integration).

A cosmetic seam passes (1) and fails (2); it is worse than either half alone because it signals neither real integration nor honesty. You want both true.

---

## 2. The architecture

```
                 ┌─────────────────────────────────────────────┐
                 │  System B — Agentic tool (backend-agnostic)  │
                 │  harness · tools/MCP · RAG/memory · evals ·  │
                 │  observability · RL reward loop              │
                 └───────────────┬─────────────────────────────┘
                                 │
            ┌────────────────────┴─────────────────────┐
            │  THE CONTRACT (the seam)                  │
            │  OpenAI-compatible /v1/chat/completions   │
            │  + 1 deliberate leak (logprobs / timing / │
            │    scheduler hook) consumed by B's eval+RL│
            └────────────────────┬─────────────────────┘
                                 │
                 ┌───────────────┴─────────────────────────────┐
                 │  System A — Inference/serving substrate      │
                 │  KV cache · continuous batching · paged KV · │
                 │  quantization · spec-decode · (kernels under)│
                 │  serving a checkpoint (optionally RL-tuned)  │
                 └─────────────────────────────────────────────┘
```

### System A — Inference / serving substrate (Infra moat)
Pulls from v5 Tier 2 (and optionally 2.1 kernels, 2.2/3.1 training):
- KV cache → continuous batching (admit/evict across decode steps) → paged-KV allocator → KV quantization → speculative-decoding draft loop.
- Exposes an **OpenAI-compatible `/v1/chat/completions`** endpoint (streaming + non-streaming).
- Optionally: your hand-written kernels (2.1) plug in under it; the checkpoint it serves can be one you fine-tuned (3.2).
- **Standalone proof:** throughput/latency benchmark table vs vLLM/reference on the same model + hardware. This is a complete infra portfolio piece by itself.

### System B — Agentic tool (Agentic moat)
Pulls from v5 Tier IV/V:
- ReAct harness from scratch → tool dispatch + MCP → context compaction/recovery → RAG/memory → trajectory eval harness → observability.
- **Backend-agnostic by construction:** it speaks the OpenAI-compatible contract and does not know or care what's behind it.
- Task in your identity: an autonomous **fuzzing/bug-triage agent** (AFL++/SymCC) or **DB-tuning/triage agent** (ClickHouse/ScyllaDB).
- **Standalone proof:** eval scorecard on a real-benchmark slice (SWE-bench-lite subset / GAIA-style / your domain harness), rerunnable by a stranger. A complete agentic portfolio piece by itself.

### The contract — clean baseline + one deliberate leak
- **Baseline:** OpenAI-compatible API. This makes B provider-agnostic (it can target a hosted provider *or* System A) and de-risks integration by using an industry-standard interface.
- **The one leak (co-design depth):** the engine exposes something a stock API hides, and B *actually consumes it*. Pick one:
  - **Token-level timing + logprobs** → B's eval harness scores latency/uncertainty per token; B's RL reward uses logprob signal. (Recommended — directly feeds 3.2 and 4.3.)
  - **Scheduler / batching hook** → B's sub-agent spawning hints the engine's batching for parallel tool-call decode.
  - **KV-state handle** → B's context compaction coordinates with the engine's paged-KV eviction.

The leak is the proof that both halves were built by the same person. Keep it to **one** — more than one couples the systems so tightly that the standalone test (§1.1) starts to fail.

---

## 3. The union artifact — the substitution benchmark

The seam earns its place by enabling a demonstration neither half can produce alone:

Run **the same agent (B)** against:
1. a hosted reference provider, and
2. **your own engine (A)** serving an open-weight model (optionally one you RL-tuned).

Produce one table:

| Metric | B on reference provider | B on your engine | Notes |
|---|---|---|---|
| Eval score (task success) | … | … | capability parity? |
| TTFT (time to first token) | … | … | |
| TPOT (time per output token) | … | … | |
| Throughput (req/s at batch) | … | … | continuous batching win |
| $/task (or tokens·price model) | … | … | the cost story |

This single table *demonstrates* the full-stack tradeoff instead of asserting it. It is the union profile in one artifact.

### The cross-seam RL loop (the deepest integration)
Reward from **B's eval harness (4.3)** → tunes a model **served by A (2.3)** via **your PPO/GRPO loop (3.2)**. The reward signal crosses the seam; the tuned checkpoint crosses back. Plot the before/after eval curve. This is your "roast-in-the-oven" credit-assignment problem operating across your own full stack — the single highest-signal thing in the entire portfolio.

---

## 4. Build order — contract-first (so the seam doesn't die)

Even with unlimited effort, the failure mode is: both halves expand to fill available effort, the seam is perpetually "next," and you end with two disconnected repos. Defuse with design, not hours:

1. **Write the contract first.** Define the OpenAI-compatible interface spec + the one leak's schema. Commit it before deepening either side.
2. **Stub both ends against the contract on day one.** System B talks to a trivial echo/passthrough "engine"; System A serves a trivial loopback "agent." End-to-end path exists immediately, empty but wired.
3. **Deepen each side independently, integrating continuously.** Every increment on A or B must keep the stubbed end-to-end path green. Never a big-bang integration at the end.
4. **Add the leak only after both baselines are solid.** Premature coupling makes both sides harder to debug in isolation.
5. **Capstone milestone = the substitution benchmark (§3) runs green**, not "both repos exist."

---

## 5. Standalone proofs (each must stand alone)

| System | Standalone proof | Reviewer audience |
|---|---|---|
| A (inference substrate) | throughput/latency table vs vLLM, same model+HW | infra |
| B (agentic tool) | rerunnable eval scorecard on a real-benchmark slice | agentic |
| Seam (union) | the substitution benchmark + the cross-seam RL curve | full-stack |

If any row can't stand on its own, that half isn't done — regardless of how good the union looks.

---

## 6. The tradeoff, stated honestly

- **Scope:** ~1.7x a single capstone. You accepted this ("forget time/effort").
- **Depth:** higher than the monolith — each half is optimized for its own correctness, not a unifying demo.
- **Residual risk under infinite effort:** integration risk (the seam never lands). Defused by §4 contract-first, not by hours.
- **What you get:** two standalone portfolio pieces (one per role) + a union artifact that is *real* (passes the load-bearing-seam test) instead of cosmetic. The two-audience legibility is the actual payoff: an infra team and an agentic team each see a complete, deep artifact addressed to them, plus proof you own the layer the other team works in.

---

*To start: say "scaffold the capstone contract" and you'll get the interface spec + a contract-conformance test harness (so both A and B can be validated against the seam independently) + acceptance criteria — no solution code. Build A and B against it from scratch; paste back; the mentor reviews principal-engineer style.*
