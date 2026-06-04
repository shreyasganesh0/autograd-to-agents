# .curriculum — planning spine (private)

This directory holds the planning, specs, and process for building the repo's
components from scratch. It is intentionally separate from the shippable tree
(`src/`, `tests/`, `docs/`) so the public surface reads as engineering, not
process. Nothing here is a build artifact; it's how the build is driven.

## Read order

1. **`STATUS.md`** — current component + its state. Source of truth; read first.
2. **`CONTRACT.md`** — the operating manual for the AI collaborator (what to
   produce, what never to, review style). The terse auto-loaded version is the
   the local mentor contract.
3. **`start_here.md`** — full philosophy and the per-phase loop.
4. **`build_plan.md`** — the component roadmap, order, and dependencies.
5. **`capstone_architecture.md`** — the two-systems end goal (engine + agent +
   contract).
6. **`BUILD_GUIDE.md`** — the maintainer-facing "you build, I guide" field guide.

## Contents

```
STATUS.md                       current state (read first)
CONTRACT.md                     AI operating manual (full; the local contract is the terse copy)
start_here.md                   philosophy + per-phase loop
build_plan.md                   component roadmap, order, dependencies
capstone_architecture.md        Tier V: engine + agent + the load-bearing contract
BUILD_GUIDE.md                  maintainer-facing field guide
HARNESS_VALIDATION_PROTOCOL.md  the five gates every tests/ harness must pass
phase_specs/<component>.md       the spec for each component (the contract for the build)
harness_notes/<component>.md     validation evidence for each tests/ harness
templates/                       scaffolds for a new component spec + results writeup
gaps_log.md                      unproven assumptions / tolerated hacks (novelty fuel)
research_map.md                  living taxonomy across the field
```

## Eventual split

When the inference engine and the agent graduate into their own standalone
repositories, this spine stays private and continues to drive all of them. The
mapping from "phase" to its shipped home:

- autograd, transformer, architecture variants → `src/` here
- inference serving (System A) → its own repo at graduation
- agent harness (System B) → its own repo at graduation
- the seam / substitution benchmark → joins the two at the capstone
