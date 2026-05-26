# Tier _ · Phase _._ — <NAME> (scaffold)

<!-- Fill this when you START the phase, informed by your review of the previous phase.
     Do not pre-write phases more than 1 ahead. Delete these comments when filled. -->

**Deliverable of this phase:** <the one externally verifiable artifact this phase ships>
**What you'll own afterward:** <the capability this unlocks for later tiers>
**Tag:** CORE / INFRA / AGENTS    **Calibration:** 🔨 / 🧩 / 📖
**Ground rule:** spec + validated harness only. No solution code. You design and write every line. Any math is yours to do off-repo; this project ships code, not derivations.

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
```
<exact names + shapes + semantics the harness will call>
```

## Acceptance criteria (phase-level "done")
1. Harness: all rows PASS, tolerance <bound>.
2. RESULTS.md published; stranger can rerun.

## Principal-engineer traps (no solutions)
- <the place people bleed #1>
- <#2>

## What you hand back for review
1. Implementation + harness table
2. One sentence per trap: did it bite, how resolved
