# BUILD_GUIDE — you build, I guide

This is your field guide, written **to you**, to read **offline** — away from the
chat, while you build. It does not contain solution code, and it never will:
that's the whole point of the repo. It tells you how to work a phase solo, what
to exhaust before you come back, and the exact moments coming back is worth a
context switch.

If you only remember one sentence: **the build is yours, from a blank file; the
mentor is an oracle and a reviewer, not a source of code.** Anything I generate
for you destroys the thing you're here to build — the ability to recreate every
artifact with your eyes closed.

---

## The deal (builder-side boundary)

So you never burn a turn asking for something I'm contractually bound to refuse:

| You CAN ask me for | I will NOT give you |
|---|---|
| A phase **spec / README** (what to build, the API contract, the traps) | Solution code — not skeletons, not "just the tricky function," not a "starting point" |
| A **validated harness** (the oracle you check your work against) | The `*.py` you're meant to build, or `RESULTS.md` filled in for you |
| **Principal-engineer review** of code + numbers you paste back | A pre-built phase you haven't reached (specs stay ≤1 phase ahead of where you are) |
| The **interview attack** on your design, and the next upgrade | Math derivations as a deliverable — this is build-only; any math you do is yours, off-repo |
| A **standalone explanation** in chat when you're stuck on a concept | That same explanation written into the repo |

The local pre-write guard hook enforces the code half of
this at the tool layer. If you ever see me try to write a solution `.py` under
`src/`, the hook should stop it — and if it didn't, I already broke the
contract. Hold me to it.

---

## The loop (per phase)

1. **Start a phase.** Tell me *"scaffold Tier X, Phase Y"* (or *"resume"* — then I
   read `.curriculum/STATUS.md` for where you are). I hand you a README + a **validated**
   harness + acceptance criteria + which exam questions it proves.
2. **Build it offline.** From a blank file. Run the harness after each part —
   unbuilt parts report `SKIP`, finished parts flip to `PASS`. This guide + the
   phase README are all you should need open.
3. **Get stuck? Run the checklist below first.** Most blocks clear without me.
4. **Come back at a real trigger** (next section) — paste code + harness output +
   numbers. I review principal-engineer style.
5. **Iterate to acceptance.** When every harness row is `PASS` and the artifact is
   shipped, I update `STATUS.md` and we advance.

---

## When to come back to the mentor (triggers)

Come back when you hit one of these — not before (you learn more fighting the
block than handing it over), and not after silently working around it:

- **Stuck past ~60–90 min on the same failing harness row** after the checklist
  below. Paste: the row, the relevant code, what you've already ruled out.
- **A harness row is green but you don't trust it.** Bring the "this passes but I
  think it's wrong" case — that's exactly the overstated-"it works" failure the
  review style hunts for.
- **You need a harness validated** before you build against it. Never trust an
  oracle that hasn't passed a known-correct ref AND caught a known-broken one
  (the five gates in `.curriculum/HARNESS_VALIDATION_PROTOCOL.md`).
- **Phase looks done — you want the review** before advancing. Paste code +
  full harness table + benchmark numbers. Green tests are necessary, not
  sufficient; I'll pose the interview attack and name the next upgrade.
- **You hit a design fork** you can't resolve from the spec ("mean vs sum here?",
  "does this leaf feed two losses?"). Ask the question, not "what's the answer."
- **A concept is genuinely opaque** (a library term, a property the harness
  assumes). Ask for a standalone explanation — I'll give it in chat, not in the
  repo.
- **You found a gap worth logging** — an unproven assumption, a hack the field
  tolerates, a "breaks at X." That's Tier-VI fuel; we log it in
  `.curriculum/gaps_log.md` as you go, not at the end.

When you come back, the lean context is: `.curriculum/STATUS.md` + the current phase
folder. Don't re-upload the whole repo — I'll ask for a specific file by name if
I need one.

---

## Self-serve when stuck (exhaust this before coming back)

A failing or surprising harness row, in order:

1. **Re-read the phase's traps section.** It names where people bleed on exactly
   this phase. Your bug is probably listed.
2. **Isolate the failing row.** Which single check flipped? What's the smallest
   input that reproduces it? Don't debug the whole suite at once.
3. **Read what the oracle actually computes.** The harness checks you against an
   *independent* method (finite differences, full recompute, brute-force exact,
   a reference library). If your value and the oracle's disagree, decide which
   one you actually believe and why — that question usually contains the bug.
4. **Check the boring contract details first.** mean vs sum · in-place vs return ·
   shape/axis/`keepdims` · dtype (is something silently `float32`?) · sign ·
   off-by-`N`. Most "deep" bugs are one of these.
5. **Add a scratch print, not a rewrite.** Diff your intermediate against what
   the oracle's intermediate must be. Resist rewriting the whole function.
6. **Rule things out, write them down.** By the time a trigger fires, you should
   be able to say "it's not A, B, or C, because…". That list is what makes the
   review fast — and half the time, writing it surfaces the answer yourself.

If you've done 1–6 and you're still blocked, that's a real trigger. Come back.

---

## Phase map (read-only — your offline compass)

Every phase ships **one** verifiable artifact. No phase is "done" without it.
This mirrors `.curriculum/build_plan.md`; it's here so you can navigate offline
without spoilers. It is a *map*, not a spec — you get the real spec one phase at
a time, when you reach it.

| Phase | Build | Ship (the one artifact) |
|---|---|---|
| **0.1** Autograd | scalar → tensor reverse-mode autodiff → NN primitives | gradient-check suite + `RESULTS.md` *(current)* |
| **1.1** Transformer | BPE → attention → GPT block → train loop → load GPT-2 | coherent generation from real weights + tok/s |
| **1.2** Architecture zoo | RoPE · GQA/MQA · RMSNorm/SwiGLU · MoE routing | attn-variant writeup + measured KV deltas + RoPE failure curve |
| **2.1** GPU / kernels | naive → tiled matmul → fused softmax → flash-style kernel | kernel throughput vs cuBLAS + roofline |
| **2.2** Distributed training | data-parallel all-reduce → ZeRO-1 → tensor-parallel | scaling curve + memory-vs-sharding table |
| **2.3** Inference systems | KV cache → server → continuous batching → paged KV | server + throughput/latency table → **System A** |
| **3.1** Data + pretraining | dedup (MinHash/LSH) → tokenizer → pretrain small model | loss curve matching a public reference |
| **3.2** Post-training & RL | SFT → reasoning → DPO → PPO/GRPO on verifiable reward | before/after eval curves + credit-assignment writeup |
| **3.3** Interp & safety | logit lens + probing → train an SAE | SAE writeup surfacing interpretable features |
| **4.1** Agent harness | ReAct → tool dispatch → context engineering → sub-agents | zero-framework harness over an over-context task → **System B** |
| **4.2** Memory & retrieval | brute-force vector search → HNSW → RAG → episodic memory | recall@k/latency + retrieval eval + agent-success A/B |
| **4.3** Evals | task spec → sandboxed scoring → judge+calibration → CI gating | rerunnable scorecard *(lead artifact)* |
| **5.0** Capstone contract | OpenAI-compatible interface + one deliberate leak; stub both ends | contract spec + conformance harness (validates both ends) |
| **5.1** Production layer | MCP server/client · observability · guardrails · orchestration | deployed MCP system with observability |
| **5.2** Capstone integration | A + B + the seam, integrated continuously | substitution benchmark + cross-seam RL curve |
| **6.x** Novelty | attack a gap from `GAPS_LOG.md` (systems × RL × agents) | a falsifiable novel result + reproducible numbers |

### Order (execute this, not the table's row order)
**Shared core first** — buys both the infra role and the agents role:
`0.1 → 1.1 → 1.2 → 2.3 → thin 4.3 → 3.2`. **Until job offers stabilize, run only
this core.** Then extend the tail the pipeline heats up (infra: `2.1 → 2.2 → 3.1
→ 3.3`; agents: `4.1 → 4.2 → 4.3-full → 5.1`). Then the capstone, **contract-first**:
`5.0 → 5.1 → 5.2`. Then Tier VI, fed by the gaps log you kept throughout.

### Hard dependencies (don't skip ahead past these)
`0.1 → 1.1 → (1.2, 2.x)` · `2.1` precedes `2.3` · `2.2` enables `3.1` · `3.2`
consumes `4.3` as its reward oracle (build a thin eval inside `4.1`, expand in
`4.3`) · the capstone consumes `2.3 + 4.1–4.3 + 3.2`. The capstone's two systems
(the inference engine and the agent) graduate into their own standalone repos at
the 2.3 / 4.1 boundaries; you don't reserve homes for them early.

---

## Where state lives (how to resume cold)

1. **`.curriculum/STATUS.md`** — the source of truth for which phase you're in and its
   state. Read this first every time. Never infer state from filenames or git log.
2. **The current component** — its spec `.curriculum/phase_specs/<component>.md`,
   its code home `src/<component>/`, and its harness `tests/test_<component>.py`.
3. **`.curriculum/gaps_log.md`** (novelty fuel) and **`.curriculum/research_map.md`**
   (taxonomy). Open from day one; never "done."

Deeper background, only if 1–2 don't answer the question:
`.curriculum/start_here.md` (full philosophy) · `.curriculum/build_plan.md` (the map +
rationale) · `.curriculum/capstone_architecture.md` (Tier V only). The authorship
policy you're holding me to is the local mentor contract; the
full operating manual is `.curriculum/CONTRACT.md`.

---

## Non-negotiables (these govern every phase)

1. **Ship one verifiable artifact per phase before advancing.** A stranger must
   be able to rerun it. Finished-and-benchmarked beats ambitious-and-unfinished —
   half-built artifacts are the main failure mode.
2. **Trust no harness until it's validated** — passed a known-correct ref AND
   caught a known-broken one. An unvalidated oracle is worse than none.
3. **Shared core first.** Dual-purpose phases before either specialist tail.
4. **Capstone is contract-first.** Interface + stubbed ends day one; integrate
   continuously; never big-bang at the end.
5. **`GAPS_LOG.md` runs from day one.** Started late, it produces nothing.

---

*Current phase: Tier 0 · Phase 0.1 (autograd), Part 1 = scalar autograd in
`autograd.py`. Open `.curriculum/phase_specs/autograd.md` and start from a
blank file. Run `python3 tests/test_autograd.py` after each part and watch the rows go
green.*
