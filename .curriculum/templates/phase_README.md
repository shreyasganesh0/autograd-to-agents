# Tier _ · Phase _._ — <NAME> (requirements brief)

<!-- Fill when the phase STARTS, informed by review of the previous phase.
     Never pre-write more than 1 phase ahead. Delete these comments when filled.

     GENRE RULE (the whole point of this template): this is a CLIENT-STYLE
     REQUIREMENTS BRIEF read by a principal engineer. It pins down (a) the
     interface the harness imports, (b) observable behavior, (c) binding
     constraints, (d) vocabulary + primary sources. It NEVER specifies
     mechanisms — no algorithms, no data-structure choices, no "do it by
     X-ing" — and it contains no pep talk. State each fact exactly once.
     If a sentence tells the engineer HOW rather than WHAT-must-be-true,
     cut it: discovering the how is the learning. -->

**How to read this.** Client-style requirements brief. The interface, observable
behavior, and binding constraints below are fixed; every design decision not
pinned here is deliberately unspecified — designing it is the work. Acceptance
is `tests/test_<component>.py`, every row PASS. Math is yours, off-repo; this
project ships code.

**Deliverable:** <the one externally verifiable artifact this phase ships>
**Tag:** CORE / INFRA / AGENTS    **Calibration:** 🔨 / 🧩 / 📖

## What this is — and is not

<!-- REQUIRED, FIRST. The category of the component (a differentiation engine?
     an inference server? a benchmark harness?) and explicitly what it is NOT —
     naming the adjacent thing the engineer is most likely to build by mistake.
     Close with the one-sentence right-artifact test. Never a one-liner. -->

## Context (what the client's system needs this for)

<!-- The client's reasons, stated once, concretely: which later tiers/phases
     consume this, which downstream failures trace back to getting it wrong,
     which patterns recur (with real cross-references: Tier 2.1, Tier 4.3...).
     End with the defining risk of the component (silent wrongness? perf cliff?
     integration rot?) and why the deliverable's shape answers that risk.
     Bullets over essays. No motivation padding. -->

## Acceptance (the only gate)

<!-- REQUIRED. Foreground the validated harness as the CONTINUOUS cross-check:
     build a part, run the suite, a row flipping SKIP→PASS is proof of the
     required observable behavior however it was implemented. State:
     - the run command and pass condition
     - the independent oracle (finite differences / full recompute /
       brute-force / reference impl) so the engineer trusts it isn't circular
     - that only the public surface is inspected (design freedom is real)
     - tolerances/thresholds AND the expected quality floor (so barely-passing
       reads as a warning)
     - pointer to the five-gate validation evidence in harness_notes/ -->

## Interface requirements (what the harness imports)

<!-- For EVERY imported name:
     - signature (shapes + dtypes)
     - **Computes:** observable forward behavior — this is spec, not spoiler
     - **Role:** where it lives in real systems
     - **Requirement (observable):** what must be true after a call / what the
       side effects must produce — phrased as observable outcomes, NEVER as the
       mechanism that achieves them
     - **Binding details:** mean vs sum, dtypes, in-place vs return, error modes
     State explicitly that everything below is the public surface and all
     internals are private and deliberately unspecified. -->

### <name>

```
<signature with shapes and dtypes>
```

- **Computes:** <observable forward behavior>
- **Role:** <role in real systems>
- **Requirement (observable):** <what must be true; not how>
- **Binding details:** <the contract details people get wrong>

## Milestones (each gated independently by the suite)

1. <part — and which suite rows gate it>
2. ...
N. <published artifact: all rows PASS + RESULTS.md>

Proves (build-proven exam questions): <1–3, phrased as "implement X such that
row Y PASSes" / "measure Z and report it">

## Vocabulary & primary sources

<!-- Every library/vocabulary term the brief or harness assumes, defined at the
     level of the ROLE it plays in the interface (audience: knows Python/C,
     never touched the relevant library). Each concept that is part of the
     learning gets a PRIMARY SOURCE: the paper that introduced it, official
     docs, or a textbook chapter — the same sources the field cites. NEVER link
     an implementation of the thing being built; add the standing warning not
     to read reference implementations until after acceptance. -->

### <sub-area>
- **`<term>`** — <role-level definition>. Primary source: <paper/docs link>.

## Known failure modes (named, not solved)

<!-- Where implementations of this contract historically go wrong, one bullet
     each, tied to the suite row that catches it. Name the failure, never the
     fix. -->

- <failure mode — and the row aimed at it>

## Hand-back for review

1. Implementation + full harness table (+ benchmark numbers where the phase has them)
2. One sentence per failure mode: did it bite, how resolved
