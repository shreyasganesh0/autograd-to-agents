# systems/ — the capstone's two homes (reserved; do not fill early)

These two directories are **reserved homes** for the Tier V capstone (see
[`docs/02_capstone_architecture.md`](../docs/02_capstone_architecture.md)).
They are intentionally empty until you reach **Phase 5.0 (capstone contract)**.

- **`A_inference/`** — System A: the inference / serving substrate (the infra
  moat). Grows out of the Tier II work (KV cache → continuous batching → paged
  KV → …) and exposes the OpenAI-compatible `/v1/chat/completions` contract.
- **`B_agent/`** — System B: the backend-agnostic agentic tool (the agentic
  moat). Grows out of Tier IV (ReAct harness → tools/MCP → memory → evals). It
  speaks the contract and does not know what's behind it.

**Why these exist now, empty:** you asked to see the end-shape of the repo up
front. That's all this is — a place to land the two systems so the seam has an
obvious home. **Per the contract, nothing here gets scaffolded until Phase 5.0
is the current phase.** Until then these stay empty (a `.gitkeep` holds each
directory). Building either system is your work, from a blank file, against the
contract harness — not mentor-generated.
