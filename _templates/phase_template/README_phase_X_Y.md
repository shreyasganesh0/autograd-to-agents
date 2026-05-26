# Tier _ · Phase _._ — <NAME> (scaffold)

<!-- Fill this when you START the phase, informed by your review of the previous phase.
     Do not pre-write phases more than 1 ahead. Delete these comments when filled. -->

**Deliverable of this phase:** <the one externally verifiable artifact this phase ships>
**What you'll own afterward:** <the capability this unlocks for later tiers>
**Tag:** CORE / INFRA / AGENTS    **Calibration:** 🔨 / 🧩 / 📖
**Ground rule:** spec + validated harness only. No solution code. You design and write every line.

## Exam questions this phase targets
1. [build-proven | derive-on-paper] <question from v6 §1>
2. ...

## The build, in parts (each gated independently by the harness)
### Part 0 — Derivations/design on paper (before code) → `DERIVATIONS.md` or `DESIGN.md`
<what to reason through before writing anything>

### Part 1 — <name> 🔨
<the central idea; what the harness rows check>

### Part N — The harness as a published artifact
<make every row green; write RESULTS.md; publish>

## API contract (what the harness imports)
```
<exact names + shapes + semantics the harness will call>
```

## Acceptance criteria (phase-level "done")
1. Paper artifact reviewed and correct.
2. Harness: all rows PASS, tolerance <bound>.
3. RESULTS.md published; stranger can rerun.

## Principal-engineer traps (no solutions)
- <the place people bleed #1>
- <#2>

## What you hand back for review
1. <paper artifact>
2. Implementation + harness table
3. One sentence per trap: did it bite, how resolved
