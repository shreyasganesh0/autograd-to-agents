# BUILD_GUIDE — you build, I guide

Your field guide, read offline while you build. It contains no solution code and
never will. The frame: each phase hands you a **client-style requirements
brief** — the vague shape (interface, observable behavior, constraints,
acceptance suite). You are the **principal engineer**: you interpret the brief,
design the internals, build them, and hand the result back for a critique.
Interpreting and designing is the learning; that's why the brief won't tell you
how.

## The deal (so you never burn a turn asking for what I must refuse)

| You CAN ask me for | I will NOT give you |
|---|---|
| A phase **brief** (interface, constraints, failure modes, primary sources) | Solution code — no skeletons, no "tricky function," no "starting point" |
| A **validated harness** (the acceptance suite you check against) | The `*.py` you're meant to build, or `RESULTS.md` filled in |
| **Principal-engineer review** of code + numbers you hand back | A brief for a phase you haven't reached (≤1 phase ahead, always) |
| The **interview attack** on your design, and the next upgrade | Math derivations as deliverables — any math you do is yours, off-repo |
| A **standalone explanation** of a concept, in chat | That explanation written into the repo |

The local pre-write guard hook enforces the code half at the tool layer. Hold me
to it.

## The loop (per phase)

1. Say **"scaffold Tier X, Phase Y"** (or "resume" — I read `STATUS.md`). You
   get: brief + validated harness + acceptance criteria.
2. **Build offline, from a blank file.** Run the suite after each part — unbuilt
   parts SKIP, finished parts flip PASS. This guide + the brief are all you need open.
3. Stuck? **Run the self-serve checklist below first.**
4. Come back at a **real trigger** (next section) with code + harness output + numbers.
5. Iterate to acceptance → I update `STATUS.md` → next phase.

## Triggers (when coming back beats fighting on)

- **Stuck past ~60–90 min on one failing row** after the checklist. Bring: the
  row, the relevant code, what you've ruled out.
- **A row is green but you don't trust it** — exactly the overstated-"it works"
  case the review hunts for.
- **You need a harness validated** before building against it (the five gates in
  `HARNESS_VALIDATION_PROTOCOL.md`; never trust an unvalidated oracle).
- **Phase looks done — you want the review** before advancing. Green is
  necessary, not sufficient.
- **A design fork the brief doesn't resolve.** Ask the question, not "what's
  the answer."
- **A concept is opaque** after its primary source. I explain in chat, not in repo.
- **You found a gap worth logging** (unproven assumption, tolerated hack,
  "breaks at X") → `gaps_log.md`, logged as you go. Tier-VI fuel.

Lean context when you return: `STATUS.md` + the current phase's files. I'll ask
for anything else by name.

## Self-serve when stuck (exhaust before returning)

1. **Re-read the brief's failure-modes section** — your bug is probably named.
2. **Isolate the failing row.** Smallest reproducing input; never debug the
   whole suite at once.
3. **Read what the oracle computes.** It's independent (finite differences, full
   recompute, brute force, reference library). Decide which value *you* believe
   and why — that question usually contains the bug.
4. **Check the boring contract details:** mean vs sum · in-place vs return ·
   shape/axis/`keepdims` · dtype (silent float32?) · sign · off-by-N.
5. **Scratch print, not rewrite.** Diff one intermediate against what the
   oracle's must be.
6. **Write down what you've ruled out.** "Not A, B, or C because…" makes the
   review fast — and writing it surfaces the answer half the time.

## Phase map (offline compass — a map, not a brief; briefs arrive one phase at a time)

Every phase ships **one** verifiable artifact; no artifact, no "done."

| Phase | Build | Ship (the one artifact) |
|---|---|---|
| **0.1** Autograd | scalar → tensor reverse-mode autodiff → NN primitives | gradient-check suite + `RESULTS.md` *(current)* |
| **1.1** Transformer | BPE → attention → GPT block → train loop → load GPT-2 | coherent generation from real weights + tok/s |
| **1.2** Architecture zoo | RoPE · GQA/MQA · RMSNorm/SwiGLU · MoE routing | attn-variant writeup + KV deltas + RoPE failure curve |
| **2.1** GPU / kernels | naive → tiled matmul → fused softmax → flash-style kernel | kernel throughput vs cuBLAS + roofline |
| **2.2** Distributed training | data-parallel all-reduce → ZeRO-1 → tensor-parallel | scaling curve + memory-vs-sharding table |
| **2.3** Inference systems | KV cache → server → continuous batching → paged KV | server + throughput/latency table → **System A** |
| **3.1** Data + pretraining | dedup (MinHash/LSH) → tokenizer → pretrain small model | loss curve matching a public reference |
| **3.2** Post-training & RL | SFT → reasoning → DPO → PPO/GRPO on verifiable reward | before/after eval curves + credit-assignment writeup |
| **3.3** Interp & safety | logit lens + probing → train an SAE | SAE writeup surfacing interpretable features |
| **4.1** Agent harness | ReAct → tool dispatch → context engineering → sub-agents | zero-framework harness over an over-context task → **System B** |
| **4.2** Memory & retrieval | brute-force vector search → HNSW → RAG → episodic memory | recall@k/latency + retrieval eval + agent-success A/B |
| **4.3** Evals | task spec → sandboxed scoring → judge+calibration → CI gating | rerunnable scorecard *(lead artifact)* |
| **5.0** Capstone contract | OpenAI-compatible interface + one deliberate leak; stub both ends | contract spec + conformance harness |
| **5.1** Production layer | MCP server/client · observability · guardrails · orchestration | deployed MCP system with observability |
| **5.2** Capstone integration | A + B + the seam, integrated continuously | substitution benchmark + cross-seam RL curve |
| **6.x** Novelty | attack a gap from `gaps_log.md` (systems × RL × agents) | falsifiable novel result + reproducible numbers |

**Order (execute this, not row order):** shared core `0.1 → 1.1 → 1.2 → 2.3 →
thin 4.3 → 3.2` — until job offers stabilize, run only this. Then the tail the
pipeline heats up (infra: `2.1 → 2.2 → 3.1 → 3.3`; agents: `4.1 → 4.2 →
4.3-full → 5.1`). Then capstone contract-first `5.0 → 5.1 → 5.2`. Then 6.x, fed
by the gaps log.

**Hard dependencies:** `0.1 → 1.1 → (1.2, 2.x)` · `2.1` precedes `2.3` · `2.2`
enables `3.1` · `3.2` consumes `4.3` as reward oracle (thin eval inside 4.1,
expanded in 4.3) · capstone consumes `2.3 + 4.1–4.3 + 3.2`. Systems A and B
graduate to standalone repos at the 2.3 / 4.1 boundaries.

## Where state lives (resuming cold)

1. **`STATUS.md`** — source of truth for phase + state. Never infer from
   filenames or git log.
2. **The current component** — brief (`phase_specs/`), code home (`src/`),
   harness (`tests/`).
3. **`gaps_log.md` + `research_map.md`** — open from day one; never "done."
   `research_map.md` also carries the primary-source reading list per branch —
   the papers are the depth target, read them as their phases approach.

Deeper background only if needed: `start_here.md` · `build_plan.md` ·
`capstone_architecture.md` (Tier V only). Authorship policy: the local mentor
contract; full manual: `CONTRACT.md`.

## Non-negotiables

1. **One verifiable artifact per phase, before advancing.** A stranger must be
   able to rerun it. Finished-and-benchmarked beats ambitious-and-unfinished.
2. **No harness is trusted until validated** (passed a correct ref AND caught a
   broken one).
3. **Shared core first.**
4. **Capstone is contract-first** — stubs day one, integrate continuously, never
   big-bang.
5. **`gaps_log.md` runs from day one.** Started late, it produces nothing.

---

*Current phase: 0.1 autograd, Part 1 = scalar autograd in
`src/autograd/autograd.py`. Open `.curriculum/phase_specs/autograd.md`, start
from a blank file, run `python3 tests/test_autograd.py` after each part.*
