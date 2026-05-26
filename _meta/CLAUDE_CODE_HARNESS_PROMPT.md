# the coding agent prompt — generate + self-validate ONE phase's harness

Use this to have a **the coding agent instance** produce a validated test harness for a single phase, in your own environment (where `torch` is installed → you get the stronger oracle that my sandbox couldn't run). It does the write→validate→delete-reference loop for you and then **removes its own reference implementation** so it never leaks the answer.

> **Scope rule:** one phase per invocation. Do NOT ask it to batch-generate harnesses for multiple phases — an unvalidated batch is the exact failure this whole setup avoids. Generate the harness for phase N when you start phase N.

---

## The prompt (paste into the coding agent, fill the two blanks)

```
You are generating a TEST HARNESS ONLY for a from-scratch learning project. Hard rules:

1. You will NOT write, keep, or reveal any implementation of the thing being learned.
   You may write a throwaway reference ONLY to validate the harness, and you MUST
   delete it before finishing. The learner writes the real implementation themselves.

2. Produce exactly two deliverables that remain on disk:
   - `<phase>/gradcheck.py` (or `<phase>/conformance.py` for non-numerics) — the harness.
   - `<phase>/HARNESS_NOTES.md` — what known-correct thing it passed, what known-broken
     thing it caught, the oracle used, and the tolerances.

3. The harness MUST satisfy all five gates in HARNESS_VALIDATION_PROTOCOL.md:
   independent oracle · passes a correct reference · FAILS a deliberately broken
   reference · SKIPs unbuilt parts gracefully · reference deleted at the end.

4. The harness imports the learner's module by a stated CONTRACT (names + shapes +
   semantics). Print a PASS/FAIL/SKIP table, seed all randomness, exit 0 iff no FAIL.

PHASE SPEC (paste the phase README here):
<<< PASTE README_phase_X_Y.md >>>

CONTRACT (the exact import surface the harness will call — copy from the README):
<<< PASTE the API contract block >>>

Do this, in order, showing me each step:
  a. Write the harness.
  b. Write a throwaway CORRECT reference implementing the contract. Run the harness.
     Show me the table — every row must PASS (and torch rows too, since torch is here).
  c. Break the reference in ONE pedagogically-relevant way (state which). Re-run.
     Show me that the right row FLIPS to FAIL. This proves the harness isn't blind.
  d. Simulate partial progress (only Part 1 present). Re-run. Show graceful SKIPs.
  e. DELETE both reference files. Confirm only the harness + HARNESS_NOTES.md remain.
  f. Write HARNESS_NOTES.md recording gates (b)-(d) results and the tolerances.

Do NOT leave any reference implementation on disk. Do NOT show me how to implement
the learner's part. If you're unsure whether something reveals the solution, omit it.
```

---

## After the coding agent finishes

1. Read `HARNESS_NOTES.md` — confirm it states the correct-pass and broken-catch explicitly. If it can't, the harness isn't validated; regenerate.
2. Sanity-check yourself: run the harness against an empty `autograd.py` (just `pass`) — every row should SKIP, nothing should crash or PASS.
3. Only then start building. Paste your implementation + the harness table back into the mentor chat for principal-engineer review.

## Why the coding agent for this and not the chat
The chat can write a validated harness too (I did, for 0.1), but my sandbox has no torch, so the strongest oracle is unavailable to me. the coding agent runs in YOUR environment with torch present, so it can validate the harness against PyTorch directly — the literal "matches PyTorch to tolerance" proof the plan calls for. That's the one job where the local agent strictly beats the chat. Spec-writing and review stay in the chat, where the feedback loop lives.
