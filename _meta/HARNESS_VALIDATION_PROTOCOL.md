# HARNESS VALIDATION PROTOCOL

**No test harness is trusted until it has caught a known-correct implementation passing AND a known-broken implementation failing.** An unvalidated oracle gives false green or false red; either one corrupts the whole learning loop. This protocol is non-negotiable and applies to every phase.

This is exactly the loop used to validate `gradcheck.py` (write harness → write a throwaway correct reference → confirm all PASS → confirm graceful SKIP/FAIL on incomplete/broken → delete reference). Repeat it for every phase.

## The five gates (a harness is "validated" only when all five pass)

1. **Independent oracle.** The harness checks correctness against something that does NOT depend on the same idea being tested. Examples: finite differences vs analytic grads; a known closed-form answer; a reference library (PyTorch/numpy) computing the same thing a different way; a property that must hold (rows of softmax sum to 1, KV-cache output == full-recompute output). If the only "check" is "did it run without crashing," it is NOT a harness.

2. **Passes a correct reference.** Write a throwaway correct implementation of the phase's contract. Run the harness. **Every row must PASS.** If a row fails against a known-correct reference, the harness is wrong — fix the harness, not the reference.

3. **Fails a broken reference.** Deliberately break the reference in one way the phase is meant to teach (e.g., assign instead of accumulate grads; forget to reduce a broadcast; drop the softmax max-subtraction; claim a CAS slot before writing data). Run the harness. **The relevant row must FAIL.** A harness that stays green on a known bug is blind exactly where it matters.

4. **Graceful partial state.** Unbuilt parts must report SKIP (not crash, not false-pass), so you can run the harness from the moment Part 1 exists and watch rows go green. Catch `NotImplementedError`/`AttributeError`/`TypeError` as SKIP.

5. **Delete the reference.** The throwaway reference is removed before you build. You never see it; the learning is in writing your own. Keep only the harness + a note that gates 2/3 passed.

## Tolerances (numerics phases)
- Use float64 and central differences (`(f(x+h) − f(x−h)) / 2h`), h ≈ 1e-6.
- Relative error metric, PASS under ~1e-5. Expect ~1e-9 for linear/tensor ops; ~1e-7 for finite-diff through softmax/CE is normal and fine.
- Seed all randomness; the harness must be deterministic so a stranger reruns identically.

## Non-numerics phases (systems / agents)
The oracle changes but the gates don't:
- **Inference (2.3):** output of your KV-cache path must equal full-recompute output token-for-token (greedy); throughput/latency measured, not asserted.
- **Retrieval (4.2):** brute-force exact search is the oracle for HNSW recall@k; recall is a number vs ground truth, not a vibe.
- **Evals (4.3):** the harness scores a known-good and known-bad trajectory and must rank them correctly; judge calibration checked against held-out labels.
- **Capstone contract (5.0):** a conformance suite that validates BOTH ends (engine + agent) against the interface independently, with a passthrough stub as the reference.

## The one-line rule
> If you cannot state what known-correct thing the harness passed and what known-broken thing it caught, it is not validated — do not build against it.
