# 02 · MATH REFERENCE — the derivation agenda (targets, not answers)

**This is curriculum, not an answer key.** It lists what you must be able to derive cold, the shape-check invariants to validate your own work against, and where to read. It deliberately does **not** contain worked solutions — deriving these yourself is the core learning act of Tiers 0–I. (If you want a worked answer key, ask the mentor instance for one as a separate file you attempt first.)

A note on how to use the invariants: they are *checks*, not solutions. "The gradient wrt W must have shape [In, Out]" tells you when you're wrong without telling you the answer. Use them the way you'd use a type signature.

---

## Tier 0 · Phase 0.1 — Autograd

### Derive (Part 0, on paper, before any code)
1. **Linear layer.** For `y = xW + b` (x:[N,In], W:[In,Out], b:[Out]) followed by scalar loss L: derive ∂L/∂W, ∂L/∂b, ∂L/∂x as matrix expressions.
   - *Invariants:* ∂L/∂W shape = [In,Out]; ∂L/∂b shape = [Out] (so it must sum over the batch axis); ∂L/∂x shape = [N,In]. If a shape doesn't match its operand, the expression is wrong.
2. **Softmax + cross-entropy, fused.** For `p = softmax(z)`, `L = −log p[target]` (mean over batch): derive ∂L/∂z and show it collapses.
   - *Invariant / the punchline:* ∂L/∂z = (p − onehot(target)) / N. Your Part-0 derivation must reach exactly this, and the harness confirms it to ~1e-16. You must be able to say *why* it's this clean — what cancels between the exp in softmax and the log in CE. That "why" is the exam answer; reaching the formula isn't enough.
3. **Adam + bias correction** (derive-on-paper now; built in a later optimizer phase). Write the update rule from memory. Explain why m̂, v̂ need bias correction at small t. Map how storing m and v (two extra full-size states) creates the memory cost that ZeRO-1 later sharded.

### Be able to answer cold
- Why is reverse-mode (not forward-mode) the right choice for scalar-loss/many-params? (cost asymmetry)
- Why must gradients accumulate (+=) rather than assign, for a value used twice?
- Why float64 + central differences for the check, and what tolerance is honest?

### Read
Karpathy "Neural Networks: Zero to Hero" (micrograd, then makemore); any matrix-calculus reference for the layout convention (numerator vs denominator) — pick one and be consistent.

---

## Tier I · Phase 1.1 — Transformer

### Derive / be able to answer cold
- Scaled dot-product attention: why the √d_k scaling (what blows up without it)?
- Why causal masking is applied to scores pre-softmax, not post.
- The KV cache: what exactly is cached, why it makes generation O(n) per token instead of O(n²) re-attention, and where the memory goes.
- BPE: why subword beats word-level and char-level; what a merge operation is.

### Read
Raschka, *Build a Large Language Model (From Scratch)* (the spine). "Attention Is All You Need" for the original formulation.

---

## Tier I · Phase 1.2 — Architecture zoo

### Derive / be able to answer cold
- **RoPE:** how rotating query/key by position encodes *relative* position in the dot product; why it extrapolates poorly past training length; what position interpolation / NTK-scaling / YaRN change.
- **GQA/MQA/MHA:** what is shared (KV heads) vs not; the exact KV-cache memory ratio between them (derive it from #heads).
- **RMSNorm vs LayerNorm:** what RMSNorm drops (mean-centering) and why it still works.
- **SwiGLU:** why a gated activation; the parameter-count bookkeeping vs a plain MLP.
- **MoE:** top-k routing math; what the load-balancing auxiliary loss penalizes; why the all-to-all is the systems cost.

### Read
The RoPE paper; the GQA paper; the SwiGLU/GLU-variants note; a MoE routing overview (Switch Transformer / Mixtral).

---

## Tier II–III math you'll need (pointers; detailed targets land with each phase's README)
- **FlashAttention (2.1):** the IO-complexity argument — HBM accesses, not FLOPs; why recomputation wins. Derive the memory traffic of naive vs tiled attention.
- **ZeRO (2.2):** the per-stage memory accounting (params / grads / optimizer states) and the communication volume of each stage.
- **PPO/GRPO (3.2):** the policy-gradient objective; why the clipped surrogate; the bridge from your DQN/contextual-bandit background to on-policy PG; what GRPO drops (the critic) and replaces it with (group-relative advantage). This is the one place to go deep — it's your differentiation.
- **Quantization (2.3):** the int8/int4/fp8 number formats; what range/precision you lose; why outliers break naive quantization.

*Full derivation targets for these arrive in each phase's README when you reach it — they depend on build decisions you haven't made yet, so they're not pre-written here.*

---

## The rule
If you can derive every Tier-0 and Tier-I target above from a blank page, and defend the *why* (not just the formula), the math foundation is done. The harnesses confirm your code; this list confirms your understanding. Both must hold before a phase is accepted.
