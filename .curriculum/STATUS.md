# STATUS — phase tracker (source of truth; a resuming instance reads this first)

Legend: ⬜ not started · 🔨 building · 🔁 in review · ✅ accepted · 📖 conversant-only
Scaffold: `spec` = README written · `harness` = harness validated per protocol · `—` = N/A

**Update this every time a phase changes state. Never let scaffolding run more than 1 phase ahead of `building`** — pre-scaffolding the whole plan rebuilds the batch anti-pattern and anchors later specs to decisions not yet earned.

| Tier · Phase | Tag | State | Spec | Harness | Artifact to ship | Notes |
|---|---|---|---|---|---|---|
| 0.1 Autograd | CORE | 🔨 | ✅ | ✅ | gradient-check suite + RESULTS.md | **CURRENT.** Build-only; start at Part 1 |
| 1.1 Transformer | CORE | ⬜ | ⬜ | ⬜ | generation from GPT-2 weights + tok/s | next |
| 1.2 Architecture zoo | CORE | ⬜ | ⬜ | ⬜ | attn-variant writeup + KV deltas | |
| 2.1 GPU/CUDA/kernels | INFRA | ⬜ | ⬜ | ⬜ | kernel vs cuBLAS + roofline | tail |
| 2.2 Distributed training | INFRA | ⬜ | ⬜ | ⬜ | scaling curve + sharding table | tail |
| 2.3 Inference systems | CORE✦ | ⬜ | ⬜ | ⬜ | server: cont. batching + paged KV → System A | OpenAI-compat API |
| 3.1 Data + pretraining | INFRA | ⬜ | ⬜ | ⬜ | loss curve vs public ref | tail |
| 3.2 Post-training & RL | CORE✦ | ⬜ | ⬜ | ⬜ | before/after eval + credit-assignment writeup | needs 4.3 |
| 3.3 Interp & safety | INFRA | ⬜ | ⬜ | ⬜ | SAE writeup | mostly 📖 |
| 4.1 Agent harness | AGENTS | ⬜ | ⬜ | ⬜ | zero-framework harness → System B | thin eval here |
| 4.2 Memory & retrieval | AGENTS | ⬜ | ⬜ | ⬜ | recall@k/latency + A/B | |
| 4.3 Evals | CORE✦ | ⬜ | ⬜ | ⬜ | rerunnable scorecard | lead artifact |
| 5.0 Capstone contract | CORE | ⬜ | ⬜ | ⬜ | contract spec + conformance harness | CONTRACT-FIRST |
| 5.1 Production layer | AGENTS | ⬜ | ⬜ | ⬜ | deployed MCP system + observability | |
| 5.2 Capstone integration | CORE | ⬜ | ⬜ | ⬜ | substitution benchmark + cross-seam RL curve | done = green |
| 6.x Novelty | DEST | ⬜ | — | — | falsifiable novel result | fed by GAPS_LOG |

## Always-on (open today, never "done")
- `.curriculum/research_map.md` — taxonomy, updated as you read.
- `.curriculum/gaps_log.md` — unproven assumptions / tolerated hacks. **Tier-VI fuel. Start now.**

## Current session pointer
**Phase 0.1, Part 1 — scalar autograd in `src/autograd/autograd.py`.** Build-only project: no paper derivations are deliverables here or in any future phase. Any math the owner needs is done off-repo. Acceptance gates are entirely the `tests/test_autograd.py` harness rows.

## Order (from .curriculum/build_plan.md)
Shared core first: 0.1 → 1.1 → 1.2 → 2.3 → thin 4.3 → 3.2. Then the tail the pipeline heats up. Then capstone (5.0→5.1→5.2). Then 6.x. Until offers stabilize, run only the shared core.
