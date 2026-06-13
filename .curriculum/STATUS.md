# STATUS — phase tracker (source of truth; a resuming instance reads this first)

Legend: ⬜ not started · 🔨 building · 🔁 in review · ✅ accepted · 📖 conversant-only
Scaffold: `spec` = README written · `harness` = harness validated per protocol · `—` = N/A

**Update this every time a phase changes state. Never let scaffolding run more than 1 phase ahead of `building`.**

**Exit bar (changed):** a phase advances the scorecard only when it has shipped a
**published artifact + benchmark vs a named baseline + write-up**, not at "harness
green." Harness = learning gate; published+benchmarked artifact = career gate.
Thresholds/dates: the local rubric. Evidence: the local goal dossier.

## Shared core (restructured — execute in this order)
`0.1 → 1.1 → 1.2 → 2.3 → 2.1-compressed → thin-2.2 → thin-4.3 → 3.2`

| Tier · Phase | Tag | State | Spec | Harness | Ceiling | Artifact to ship (public + benchmarked) | Notes |
|---|---|---|---|---|---|---|---|
| 0.1 Autograd | CORE | 🔨 | ✅ | ✅ | 2 wk | gradient-check suite + RESULTS.md | **CURRENT.** Don't gold-plate scalar; tensor/broadcast backward is the worth-it part |
| 1.1 Transformer | CORE | ⬜ | ⬜ | ⬜ | 2 wk | generation from GPT-2 weights + tok/s | next |
| 1.2 Architecture zoo | CORE | ⬜ | ⬜ | ⬜ | 2 wk | attn-variant writeup + KV deltas + RoPE curve | |
| 2.3 Inference systems | CORE✦ | ⬜ | ⬜ | ⬜ | 8 wk | server (batching+paged KV+quant+spec-decode) vs **vLLM** + merged vLLM/SGLang PR → System A | **flagship.** library kernels allowed; read vLLM/SGLang post-acceptance |
| 2.1 Kernels (compressed) | INFRA | ⬜ | ⬜ | ⬜ | 6 wk | kernel vs cuBLAS/FA2 + roofline; swap into 2.3 | **promoted from tail** — top infra signal + his differentiator; Triton port here |
| 2.2 Distributed (thin) | INFRA | ⬜ | ⬜ | ⬜ | 2 wk | 2–4-GPU all-reduce scaling data point | "multi-GPU" is in the hiring bar; full ZeRO/TP deferred |
| thin 4.3 Evals | CORE✦ | ⬜ | ⬜ | ⬜ | 2 wk | thin rerunnable scorecard | sandbox on real isolation prims (ns/seccomp/cgroups) |
| 3.2 Post-training & RL | CORE✦ | ⬜ | ⬜ | ⬜ | 8 wk | before/after eval + credit-assignment writeup | async rollout loop; his DQN/bandit bridge |

## Tail (only as the pipeline heats up — not before offers stabilize)
| Tier · Phase | Tag | State | Artifact | Notes |
|---|---|---|---|---|
| 2.2-full Distributed | INFRA | ⬜ | scaling curve + sharding table | ZeRO-1 → TP → 📖 pipeline |
| 3.1 Data + pretraining | INFRA | ⬜ | loss curve vs public ref | ≤2-wk llm.c repro or **drop** |
| 3.3 Interp & safety | INFRA | 📖 | — | **conversant-only**; build nothing |
| 4.1 Agent harness | AGENTS | ⬜ | zero-framework harness → System B | thin eval + trivial retrieval folded in |
| 4.2 Memory & retrieval | AGENTS | 📖 | — | **demoted to conversant-only** |
| 4.3-full Evals | CORE✦ | ⬜ | full scorecard | lead artifact; expand the thin core version |
| 5.0–5.2 Capstone | CORE | ⬜ | substitution benchmark + cross-seam RL curve | **freeze if an offer/seat lands first** (least legible) |
| 6.x Novelty | DEST | ⬜ | falsifiable novel result | deprioritized; DeepMind/Meta tail only |

## Always-on (open today, never "done")
- **The four tracks** (run in parallel with every phase — see `build_plan.md`):
  **Publish** (repo + write-up per phase) · **OSS** (toward a merged flagship PR) ·
  **Papers** (2–3/wk logged in `research_map.md`) · **Apply** (screenable systems/
  agent-tooling roles **now**; inference/RE-RL at ~month 6).
- **Drill protocols** (the local rubric §C): spaced rebuild (1wk/1mo/3mo, N=3) ·
  closed-book question bank · interview-mode reps (from M+2) · why-prompts ·
  post-acceptance reference reading.
- `research_map.md` — taxonomy + paper log. `gaps_log.md` — Tier-VI fuel + every
  scope cut forced by a ceiling. **Start both now.**

## Current session pointer
**Phase 0.1, Part 1 — scalar autograd in `src/autograd/autograd.py`.** Build-only;
acceptance gates are the `tests/test_autograd.py` rows. Then the *career* gate:
publish the suite + RESULTS.md. The application trigger is ~month 6 (shared core
shipped), not plan completion.
