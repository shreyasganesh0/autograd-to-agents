# autograd-to-agents

A from-scratch LLM-mastery curriculum. Owner: Shreyas — and the **only** code
author on this repo. The goal is to rebuild every artifact (autograd →
transformer → inference server → agents → capstone) from a blank page when
the curriculum is done. **Build-only:** every phase ships code + benchmark
numbers; no math derivations are deliverables.

Six tiers, executed shared-core-first:

```
Tier 0  Math → Code        autograd
Tier I  Internals          transformer · architecture zoo
Tier II Systems            kernels · distributed training · inference server (System A)
Tier III Capability        data + pretraining · post-training & RL · interp
Tier IV Agents             harness (System B) · memory & retrieval · evals
Tier V  Capstone           A + B joined by an OpenAI-compatible contract + one deliberate leak
Tier VI Novelty            falsifiable result, fed by always_on/GAPS_LOG.md
```

## For any AI collaborator landing on this repo

**Read the local mentor contract before touching anything.** It is the mentor
contract — auto-loaded by the coding agent, also surfaced as the local mentor contract for other
agents. Headline rule: you do not write solution code for this repo, ever.
Specs, validated test harnesses, and principal-engineer review only.

## Where to start

| You are... | Read in this order |
|---|---|
| A fresh LLM picking up the mentor role | the local mentor contract → `_meta/STATUS.md` → the current `phases/tierX_phase_Y/` folder |
| The owner resuming a build session | `_meta/STATUS.md` |
| The owner, building a phase offline | `BUILD_GUIDE.md` → `_meta/STATUS.md` |
| A reader trying to understand the philosophy | `docs/00_start_here.md` → `docs/01_build_plan.md` |

## Repo map

```
local mentor contract (untracked)       mentor contract (auto-loaded by the coding agent; the local contract → the local contract symlink)
BUILD_GUIDE.md              owner-facing "you build, I guide" field guide — read offline

docs/
  00_start_here.md          full philosophy & per-phase loop
  01_build_plan.md          six-tier plan: what to ship, in what order
  02_capstone_architecture.md Tier V: two systems + the load-bearing contract

_meta/
  STATUS.md                       current phase — source of truth
  HARNESS_VALIDATION_PROTOCOL.md  five gates every harness must pass

_templates/phase_template/   scaffold for new phases (README + RESULTS)

always_on/
  GAPS_LOG.md     Tier-VI fuel — open from day one
  RESEARCH_MAP.md living taxonomy across architectures, training, inference, RL, agents, evals, interp

phases/
  tier0_phase_0_1/   autograd (current phase) — README + validated gradcheck.py
  …                  one folder per phase as you reach it

systems/             reserved homes for the Tier V capstone (empty until 5.0)
  A_inference/       System A — inference/serving substrate
  B_agent/           System B — backend-agnostic agentic tool
```

## Status

See [`_meta/STATUS.md`](./_meta/STATUS.md). Currently: **Tier 0 · Phase 0.1**
(autograd from scratch), Part 1 = scalar autograd in `autograd.py`.
