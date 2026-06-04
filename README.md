# scratchstack

From-scratch implementations of modern LLM and agent infrastructure internals —
**no frameworks, every component built and benchmarked from a blank file.**
Autograd, transformers, inference serving, and agent harnesses, written by hand
to understand them at the level of "which Jacobian / which allocation / which
scheduler decision is wrong," not "the library did something."

The discipline is constant across components: each ships **one verifiable
artifact** (a benchmark, a generation, a scorecard) checked by an **independent
oracle** before it counts as done. Green-but-unproven doesn't ship.

## Status

Implementing the **autograd engine** (`src/autograd/`) — reverse-mode autodiff
with broadcasting, plus the NN primitives (linear / softmax / cross-entropy /
layernorm) built on top of it. Verified by an independent gradient-check oracle
(central finite differences + PyTorch cross-check) in `tests/`.

## Roadmap

Built in dependency order; each line is a standalone, benchmarked deliverable.

| Component | What it is | Proof it works |
|---|---|---|
| **autograd** | reverse-mode autodiff + NN primitives | gradients match finite-diff & PyTorch |
| **transformer** | BPE → attention → GPT block → sampling; loads GPT-2 weights | coherent generation from real weights + tok/s |
| **architecture variants** | RoPE · GQA/MQA · RMSNorm/SwiGLU · MoE routing | measured KV deltas + RoPE extrapolation curve |
| **inference serving** | KV cache → continuous batching → paged KV; OpenAI-compatible API | throughput/latency table vs a reference server |
| **post-training / RL** | SFT → reasoning → preference opt → PPO/GRPO on a verifiable reward | before/after eval curves |
| **agent harness** | ReAct → tool dispatch → context engineering → sub-agents | completes an over-context task, trajectories logged |
| **retrieval / memory** | brute-force vector search → HNSW → RAG → episodic memory | recall@k / latency vs baseline |
| **evals** | sandboxed scoring → judge calibration → trajectory eval → CI gating | rerunnable scorecard |

The serving engine and the agent harness are substantial enough to graduate into
their own standalone repositories once they have content; this repo holds the
foundational internals and the work in progress.

## Layout

```
src/        hand-written implementations (one package per component)
  autograd/   reverse-mode autodiff + NN primitives  (current)
tests/      independent-oracle harnesses (test_<component>.py)
docs/        design notes (added as components land)
```

## Running the checks

```
python3 tests/test_autograd.py     # prints a PASS/FAIL/SKIP table; exit 0 iff no FAIL
```

Unbuilt parts report `SKIP`, so the harness is runnable from the first commit of a
component and you watch rows go green as it's built.

## AI collaboration

Implementation code in `src/` is authored by hand by the maintainer. The
conventions for AI assistants working in this repo (they may write tests/docs and
review, never implementation) are in the local mentor contract.
