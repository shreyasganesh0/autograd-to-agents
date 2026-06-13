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

## Two gates per phase (this is the restructure — read it)

A phase is done at **two** gates, not one:
- **Learning gate** — the harness goes all-green (what you've always done).
- **Career gate** — you ship a **public, named repo + a benchmark number vs a
  named strong baseline (cuBLAS / FlashAttention-2 / vLLM / a reference provider)
  + a measurement write-up.** Every documented career break came from a public,
  adopted, benchmarked artifact — never a private pile of passing tests. Green
  with nothing published does not advance you. Why-and-evidence: the local goal
  dossier; thresholds and dates: the local rubric.

## The loop (per phase)

1. Say **"scaffold Tier X, Phase Y"** (or "resume" — I read `STATUS.md`). You
   get: brief + validated harness + acceptance criteria + the phase ceiling.
2. **Build offline, from a blank file.** Run the suite after each part — unbuilt
   parts SKIP, finished parts flip PASS. This guide + the brief are all you need open.
3. Stuck? **Run the self-serve checklist below first.**
4. Come back at a **real trigger** (next section) with code + harness output + numbers.
5. Iterate to the learning gate → I update `STATUS.md`.
6. **Hit the career gate:** publish the repo + write-up + benchmark. Then **read
   the reference implementation** (vLLM, llm.c, FlashAttention, faiss) and log a
   short "what they did differently / what I'd steal" note — the struggle comes
   first, the reference-reading comes *after* acceptance, never before.
7. **Respect the ceiling.** Over the phase's time-box → cut scope (drop a stretch
   item), never extend. Log the cut in `gaps_log.md`.

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

## The four always-on tracks (run in parallel — the build alone won't get you hired)

The deep-research finding is blunt: building is necessary, not sufficient. The
break always came from a *public, adopted* artifact plus reputation among
practitioners — sometimes via an intermediate seat, never from solo curriculum
completion. So from day one, alongside the build:

1. **Publish** — a named public repo + a "what I measured" write-up per shipped
   phase (the Dettmers / "Go Brrrr" genre). The private spine stays private; the
   *artifacts* go public and loud.
2. **OSS** — work toward a **merged PR in a flagship project** (vLLM / SGLang /
   PyTorch / llama.cpp / TRL / an RL-env stack). A merged vLLM/SGLang PR is a
   gated deliverable of 2.3, not a bonus. Start reading the target's issues while
   you build 2.3.
3. **Papers** — 2–3/week tied to the active phase, logged in `research_map.md`
   with a 3-sentence critique + "what I'd extend." That *is* the research-
   discussion interview round.
4. **Apply now** — your classical-systems depth already clears the hard
   requirements for systems / agent-tooling / sandboxing roles (syscalls,
   allocators, io_uring). Apply to those **in parallel today**; open the
   inference / RE-RL pipeline when the shared core lands (~month 6). Applying is a
   track, not the finish line.

## Retention drills (the biggest thing the old plan was missing)

One-and-done phases decay exactly the material interviews probe. These are *more*
from-scratch building, so they fit the rule — I author the prompts, you do the
work. Full spec: the local rubric §C.

- **Spaced rebuild** — at ~1 wk / ~1 mo / ~3 mo after each acceptance, a
  **closed-book, timed micro-rebuild** gated by the same harness (scalar autograd
  in 90 min; single-head attention fwd+bwd; a KV-cache allocator). Retire it only
  after **3** clean spaced passes.
- **Closed-book question bank** — at each review I draw 3–5 questions from *past*
  phases; you answer from memory **before** any code review.
- **Interview-mode reps** (weekly from ~month 2) — you explain a past component
  **aloud** while I attack the edges, and **derive on paper** (attention
  FLOPs/memory, ZeRO-1 comm volume, paged-KV math). Spoken + paper, never
  committed.

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

Every phase ships a **public, benchmarked** artifact; green-but-unpublished is not
"done." Ceilings are hard — over → cut scope, never extend. Full rationale:
`build_plan.md`.

**Shared core (do only this until offers stabilize):**

| Phase | Ceiling | Ship (public + benchmarked vs a named baseline) |
|---|---|---|
| **0.1** Autograd | 2 wk | gradient-check suite + `RESULTS.md` *(current)* — don't gold-plate scalar |
| **1.1** Transformer | 2 wk | generation from GPT-2 weights + tok/s |
| **1.2** Architecture zoo | 2 wk | attn-variant writeup + KV deltas + RoPE failure curve |
| **2.3** Inference systems | 8 wk | server (batching+paged KV+**quant**+**spec-decode**) vs **vLLM** + a **merged vLLM/SGLang PR** → System A — *flagship; library kernels allowed* |
| **2.1** Kernels *(compressed)* | 6 wk | kernel vs **cuBLAS/FA2** + roofline + Triton port; swap into 2.3 — *promoted from tail* |
| **2.2** Distributed *(thin)* | 2 wk | 2–4-GPU all-reduce scaling data point |
| **4.3** Evals *(thin)* | 2 wk | thin rerunnable scorecard on **real sandbox prims** (ns/seccomp/cgroups) |
| **3.2** Post-training & RL | 8 wk | before/after eval + credit-assignment writeup (async rollout; your DQN/bandit bridge) |

**Tail (only as the pipeline heats up):** full 2.2 (ZeRO-1 → TP) · 3.1
(≤2-wk llm.c repro or **drop**) · 3.3 (**📖 read-only**) · 4.1 agent harness →
System B · 4.2 (**📖 read-only**) · 4.3-full · capstone 5.0→5.1→5.2
(**freeze if an offer/seat lands first**) · 6.x novelty (**deprioritized**).

**Order (execute this):** `0.1 → 1.1 → 1.2 → 2.3 → 2.1-compressed → thin-2.2 →
thin-4.3 → 3.2`, plus the four always-on tracks. **Application trigger = ~month 6
(core shipped), not plan completion.**

**Hard dependencies:** `0.1 → 1.1 → (1.2, 2.x)` · **2.3 does NOT require 2.1**
(library kernels permitted; the old "2.1 precedes 2.3" line was wrong, removed) ·
2.1's own kernel optionally swaps into 2.3 after · `2.2` enables full `3.1` ·
`3.2` consumes `4.3` as reward oracle (thin eval in core, expanded later) ·
capstone consumes `2.3 + 4.1 + 4.3 + 3.2`. Systems A and B graduate to standalone
repos at the 2.3 / 4.1 boundaries.

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

1. **Two gates per phase** — harness green (learning) AND a public, benchmarked
   artifact + write-up (career). A stranger must be able to rerun it; a recruiter
   must be able to find it.
2. **No harness is trusted until validated** (passed a correct ref AND caught a
   broken one).
3. **Shared core first; the four tracks run in parallel from day one.**
4. **Ceilings are hard** — over → cut scope, never extend; log the cut.
5. **Capstone is contract-first** — stubs day one, integrate continuously, never
   big-bang — *and* freezable if an offer/seat lands first.
6. **`gaps_log.md` runs from day one.** Started late, it produces nothing.

---

*Current phase: 0.1 autograd, Part 1 = scalar autograd in
`src/autograd/autograd.py`. Open `.curriculum/phase_specs/autograd.md`, start
from a blank file, run `python3 tests/test_autograd.py` after each part.*
