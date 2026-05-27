# Tier _ · Phase _._ — <NAME> (scaffold)

<!-- Fill this when you START the phase, informed by your review of the previous phase.
     Do not pre-write phases more than 1 ahead. Delete these comments when filled. -->

**Deliverable of this phase:** <the one externally verifiable artifact this phase ships>
**What you'll own afterward:** <one-sentence capability unlock; expanded in "Why this phase exists" below>
**Tag:** CORE / INFRA / AGENTS    **Calibration:** 🔨 / 🧩 / 📖
**Ground rule:** spec + validated harness only. No solution code. You design and write every line. Any math is yours to do off-repo; this project ships code, not derivations.

## Why this phase exists (goals, rationale, what carries forward)

<!-- Detailed motivation. The audience is the owner about to spend days or weeks
     on this — they deserve to know why it's worth their time, not just "build X."
     Fill in each subsection substantively; don't punt with one-liners. -->

### The skill you're building
<the underlying engineering capability this phase develops — phrased as "you'll be the kind of engineer who can debug/design/reason about X". One paragraph.>

### Why "from scratch" is the right call here
<what specifically goes opaque if you use the library version. Name the later debugging / design moments that depend on having built this yourself. Bullet list of 3-5 concrete future failure modes is good.>

### What carries forward to later tiers
<bullets, each naming a future tier/phase and the specific thing from this phase that recurs there. Use real cross-references (Tier 2.1, Tier 4.3, etc.). This is where you justify the order of the curriculum.>

### What good looks like
<bullets describing observable properties of a well-built solution WITHOUT giving the implementation. Things like "your class has small surface area," "you can answer interview-attack question X without running it," "numerical errors are at the floor expected from float64."  4-6 bullets.>

### Why this is the shape of the deliverable
<one paragraph: why the artifact is what it is (a single .py + harness? a benchmark table? a writeup?). Connect the deliverable shape to the nature of the correctness problem (silent bugs, performance-sensitive, etc.).>

## Exam questions this phase targets (build-proven)
1. <build-proven question — phrased as "implement X such that harness row Y PASSes" or "measure Z and report it">
2. ...

## Prerequisites — concepts this phase uses

<!-- List every library/vocabulary concept the spec, contract, or harness assumes.
     Audience: someone who knows Python (or C) but has never touched the relevant
     library (PyTorch / CUDA / vLLM / MCP / etc.). They should be able to recognize
     the term and know what role it plays — NOT how to implement it. Implementing
     it is the build. Group by sub-area; link to authoritative docs.  -->

### <sub-area, e.g. "transformer vocabulary">
- **`<term>`** — <1-2 sentence definition: what role does it play in the API? Where would a fresh dev encounter it?>
- **`<term>`** — <...>

### <next sub-area>
- ...

## The build, in parts (each gated independently by the harness)
### Part 1 — <name> 🔨
<the central idea; what the harness rows check>

### Part N — The harness as a published artifact
<make every row green; write RESULTS.md; publish>

## API contract (what the harness imports)

<!-- For EVERY function/class/method the harness imports, give all of:
     - signature (shapes + dtypes)
     - **What it computes** — the observable forward behavior (the spec)
     - **Why it exists** — what role it plays in real systems
     - **What backward / side effects must do** — the requirement, NOT the recipe
     - Any non-obvious contract details (mean vs sum, in-place vs return, etc.)
     A bare signature is not a spec. The owner cannot implement what is not
     specified. Specifying the FORWARD behavior is not giving away the BUILD —
     the build is making the forward composable with whatever larger machinery
     (autograd, KV cache, batching scheduler) the phase demands. -->

### <component name>

```
<signature with shapes and dtypes>
```

- **What it computes:** <observable forward behavior>
- **Why it exists:** <role in real systems / what it unlocks>
- **Backward / side-effect requirement:** <what must happen as a result of using it; NOT how>
- **Critical contract details:** <mean vs sum, in-place vs return, error modes, etc.>

### <next component>
...

## Acceptance criteria (phase-level "done")
1. Harness: all rows PASS, tolerance <bound>.
2. RESULTS.md published; stranger can rerun.

## Principal-engineer traps (no solutions)
- <the place people bleed #1>
- <#2>

## What you hand back for review
1. Implementation + harness table
2. One sentence per trap: did it bite, how resolved
