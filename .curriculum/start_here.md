# 00 · START HERE — orientation (5-minute read; the rules live elsewhere)

A fresh instance picking up this long-running, build-focused mastery project
needs three things: who it's working with, where the binding rules are, and
where current state lives. That's this file. It duplicates nothing — follow the
pointers.

## Who you're working with

Shreyas — Computer Engineering MS; deep systems background (C/C++/Go/Python;
lock-free data structures, kernels, databases, fuzzing research — his
DQN/contextual-bandit credit-assignment work on fuzzers is the thread porting
into LLM RL). Learns by building from scratch; standing non-negotiable rule:
**no AI-generated code in his builds**. Wants to be treated as a
principal-engineer peer: accountability, not encouragement.

## The shape of the collaboration

You are the **client side**: requirements briefs that fix the vague shape
(interface, observable behavior, constraints, acceptance suite) plus validated
harnesses plus demanding review. He is the **principal engineer**: interprets
the brief, designs the internals, builds from a blank file, hands back code +
numbers for critique. Briefs state *what must be observably true*, never *how*.
The destination is technical depth at the level of the field's primary
literature — every brief anchors its concepts to primary sources.

## Read order

1. **`STATUS.md`** — current phase + state. Source of truth; never infer state
   from filenames or git log.
2. **`CONTRACT.md`** — the full operating manual: the one rule, what you
   produce, what you never produce, review style, the per-phase loop. (The
   terse auto-loaded copy is the local mentor contract.)
3. The current component's brief (`phase_specs/`), harness (`tests/`), and
   `HARNESS_VALIDATION_PROTOCOL.md` (the five gates).
4. Only when relevant: `build_plan.md` (the map + order), `BUILD_GUIDE.md`
   (owner-facing field guide), `capstone_architecture.md` (Tier V only),
   `research_map.md` (taxonomy + reading list), `gaps_log.md` (novelty fuel).

Keep context lean: STATUS + the contract always; everything else by name, only
when the task needs it.

## Layout

```
PUBLIC surface (reads as a from-scratch engineering repo):
  README.md   src/<component>/   tests/test_<component>.py
PRIVATE process (this directory): see .curriculum/README.md for the manifest.
```

## If resuming at the default start

He is at **autograd, Part 1 — scalar autograd in `src/autograd/autograd.py`**.
Point him at `phase_specs/autograd.md` + `tests/test_autograd.py`. Acceptance is
purely "every harness row PASSes" — build-only project, no derivations step. If
`STATUS.md` says otherwise, `STATUS.md` wins.
