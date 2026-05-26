# HARNESS_NOTES — Tier 0 Phase 0.1 (gradcheck.py)

Validated per HARNESS_VALIDATION_PROTOCOL.md before handoff.

- **Oracle:** central finite differences (numpy, always) + PyTorch autograd (optional, when torch present). Independent of the autograd being tested.
- **Gate 2 (passes correct ref):** ran against a throwaway correct micrograd+tensor reference — all 11 rows PASS (linear/tensor ops ~1e-9–1e-10; CE finite-diff ~3.7e-8; the (p-y)/N clean-form oracle matched to 1.95e-16).
- **Gate 3 (catches broken ref):** confirmed rows flip to FAIL under the relevant bug class (e.g. assign-instead-of-accumulate breaks `scalar reuse/accumulation`; missing broadcast-reduce breaks `broadcast add [N,D]+[D]`).
- **Gate 4 (graceful partial):** with only `Value` present, the 10 Tensor/NN rows report SKIP, nothing crashes or false-passes.
- **Gate 5:** reference deleted. Only gradcheck.py + this note remain.
- **Tolerances:** TOL=1e-5 relative, central-diff h=1e-6, float64, SEED=0 (deterministic, stranger-rerunnable).
- **torch note:** my sandbox had no torch so the part4-torch rows SKIP there; on your Pop!_OS env they activate — get them green for the literal "matches PyTorch" proof.
