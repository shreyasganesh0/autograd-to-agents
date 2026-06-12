# Tier 0 · Phase 0.1 — Autograd engine (requirements brief)

**How to read this.** This is a client-style requirements brief. You are the
principal engineer: the brief fixes the *shape* of what's needed — the interface
the acceptance suite imports, the observable behavior, the binding constraints —
plus the vocabulary and primary sources needed to interpret it. Everything not
pinned here (graph representation, traversal strategy, where backward logic
lives, how ops record themselves) is the engineering, and it is deliberately
unspecified: designing it is the work. Acceptance is `tests/test_autograd.py`,
every row PASS. Any math you need is yours, off-repo; this project ships code.

**Deliverable:** a reverse-mode automatic-differentiation engine written from a
blank file into `src/autograd/autograd.py`, plus `RESULTS.md` showing the suite
all-green.

---

## What this is — and is not

A **differentiation engine**: a machine that, given any composition of supported
arithmetic operations, computes the derivative of a scalar output with respect
to every input, by recording operations as they run and applying the chain rule
backward through that record.

It is **not a neural network**. No weights, no training loop, no parameter
updates, no model. The NN-named functions below (`linear`, `softmax`,
`cross_entropy`, `layernorm`) are *acceptance test cases* — compositions hard
enough to prove the engine produces correct gradients. The network itself is
Tier 1.1, built on top of this.

Right-artifact test: *"I can take any expression made of my `Value`/`Tensor` ops
and get the correct gradient with respect to every leaf."* If you find yourself
writing a training step, stop — wrong artifact.

---

## Context (what the client's system needs this for)

Every later component sits on this engine or on the reasoning it builds:

- **Tier 1.1/3.x debugging:** a loss that won't decrease gets debugged at the
  level of "which Jacobian is wrong," not "the framework did something."
- **Tier 2.1:** a custom fused kernel (FlashAttention-style) needs a custom
  backward; the fused softmax–cross-entropy here is the warm-up for exactly that.
- **Tier 2.2:** gradient reduction across tensor-parallel shards is the same bug
  class as gradient flow through a broadcast — get it wrong here, get it wrong there.
- **Tier 2.3/3.2:** backward through KV caches and sampled tokens requires knowing
  what the graph actually recorded.
- **Pattern that recurs everywhere:** a DAG of operations plus a correct
  traversal order — compiler IRs, dataflow systems, the Tier 4.1 tool-call graph.
- **Discipline that recurs everywhere:** the independent-oracle habit (finite
  differences here; full recompute for KV caches; brute-force search for HNSW;
  judge calibration for evals).

Silent failure is the defining risk of this component: a wrong gradient still
trains — toward the wrong answer. That is why the deliverable is a small module
plus an independent-oracle suite, not a demo.

---

## Acceptance (the only gate)

`python3 tests/test_autograd.py` → table of PASS/FAIL/SKIP; exit 0 iff no FAIL.
All rows PASS, including the `part4-torch` rows when torch is installed.

Facts about the suite you should rely on:

- **It is the continuous cross-check, not a final exam.** Unbuilt parts SKIP, so
  run it from the first line of Part 1 and watch rows flip SKIP→PASS. A green
  row is proof the build has the required observable behavior, however you
  implemented it.
- **Independent oracle:** central finite differences in float64
  (`h ≈ 1e-6`), plus PyTorch autograd when available. Neither shares an idea
  with your engine, so agreement is evidence, not circularity. The suite itself
  was validated per the five gates in `HARNESS_VALIDATION_PROTOCOL.md`
  (evidence: `.curriculum/harness_notes/autograd.md`).
- **It touches only the public surface** (`.data`, `.grad`, `.backward()`, op
  outputs). Your internals are never inspected; your design freedom is real.
- **Tolerance:** PASS under relative error `1e-5`. Expected floors: ~`1e-9`–`1e-10`
  for linear/tensor ops, ~`1e-7` for finite-diff through softmax-CE. Passing at
  barely-under-`1e-5` means something is subtly wrong — investigate before moving on.
- The `cross_entropy` row additionally checks your gradient against an
  independently computed `(softmax(logits) − onehot(targets)) / N`; expect
  ~`1e-16` agreement there when correct.

Renamed something? Edit the import shim at the top of `main()` in the suite.
How `tests/` resolves `src/` (conftest, editable install, `PYTHONPATH`) is your
packaging call.

---

## Interface requirements (what the suite imports)

Everything below is the public surface — the only part of your design this brief
pins down. Forward behavior is specified because it's the contract; *how* the
backward achieves its requirement is not, because that's the build.

### `Value` — scalar engine

```
Value(data: float)
  .data : float (mutable)
  .grad : float (0.0 initially; populated by .backward())
  ops: + - * /  and  ** const
  at least one nonlinearity: .tanh() / .relu() / .exp()
  .backward()
```

- **Represents:** one floating-point number participating in a recorded
  computation. `c = a * b` produces a new `Value` that can later route gradient
  to `a` and `b`.
- **Backward requirement (observable):** after `out.backward()`, every node the
  output depends on holds `d out / d node` in `.grad`. This must be correct for
  **any DAG**, including a node consumed by multiple ops (`f = a*b + a` must give
  `a.grad` both contributions). Decide and document how grads reset between
  independent backward passes.

### `Tensor` — N-D engine

```
Tensor(data: np.ndarray, requires_grad: bool = True)
  .data : np.ndarray, float64 (mutable in place — the oracle perturbs it directly)
  .grad : np.ndarray of the same shape as .data, or None before backward
  ops: + - *  (elementwise, with numpy broadcasting)
       @     (matrix multiply)
       .sum(axis=None, keepdims=False)
  .backward(grad=None)   # grad defaults to 1.0 for scalar (size-1) outputs
```

- **Represents:** `Value` generalized to arrays; forward ops produce new
  `Tensor`s; backward fills `.grad` for every input with `requires_grad=True`
  (`requires_grad=False` tensors are constants — no gradient).
- **Backward requirement (observable):** `.grad` must have **the same shape as
  `.data`** and equal the true gradient — *including when the forward op
  broadcast that operand* (e.g. the `[D]` operand in `[N,D] + [D]`). The suite
  has rows specifically for `[N,D]+[D]` and `[N,1]*[1,D]`. This is the
  load-bearing requirement of the phase.
- **Binding detail:** `float64` is required — the finite-difference oracle at
  `h = 1e-6` is meaningless at float32 precision and the rows will fail.

### NN primitives — compositions over `Tensor`

These are functions composing your Tensor ops, so gradients must flow through
them via the same `.backward()`. They are not required to be new graph-node
types.

#### `linear(x, W, b)` — `x:[N,In], W:[In,Out], b:[Out] → [N,Out]`

- **Computes:** the affine map `y = x @ W + b` (bias broadcast across the batch).
- **Role:** every fully-connected layer, every attention projection, every
  classifier head is this function.
- **Note:** `b.grad` must come out shaped `[Out]` from a `[N,Out]` upstream — this
  is where the Tensor broadcast requirement gets exercised for real.

#### `softmax(x, axis=-1)` — `[..., C] → [..., C]`, rows sum to 1 along `axis`

- **Computes:** `exp(x_i) / Σ_j exp(x_j)` along `axis` — scores → probability
  distribution.
- **Role:** classifier outputs, next-token distributions, attention weights.
- **Binding detail — numerical stability is part of the contract:** the
  implementation must not overflow for moderately large logits. The standard
  identity is `softmax(x) = softmax(x − max(x))`; naive `exp` is already `inf`
  at `x ≈ 710` in float64.

#### `cross_entropy(logits, targets)` — `logits:[N,C], targets:int[N] in [0,C) → scalar`

- **Computes:** `mean_i( −log softmax(logits)_i[target_i] )` — the model's
  surprise at the true labels.
- **Role:** the loss of essentially every classifier and every LLM (classes =
  vocabulary → next-token prediction loss).
- **Binding detail — `mean`, not `sum`:** divide by batch size `N`. The suite's
  independent `(p − onehot)/N` oracle assumes it; sum-reduction fails by exactly
  a factor of `N`.
- You **may** implement a fused, stable softmax-CE with its own backward — as an
  informed choice, not as a shortcut to turn the row green.

#### `layernorm(x, gamma, beta, eps=1e-5)` — `x:[...,D], gamma:[D], beta:[D] → same shape as x`

- **Computes:** per row along the last axis: subtract the row mean, divide by
  `sqrt(variance + eps)`, then scale by `gamma` and shift by `beta`.
- **Role:** the normalization spine of every transformer block (Tier 1.1 wires
  it in; Tier 1.2 builds the RMSNorm variant and asks you to defend the
  difference). `eps` guards flat rows; `gamma`/`beta` let the network undo the
  normalization, preserving expressivity.
- **Interpretive fact:** each row's mean and variance depend on *every* element
  of that row — so the gradient is not elementwise-local. The suite's row will
  catch a backward that pretends it is.

---

## Milestones (each gated independently by the suite)

1. **Scalar autograd** — `Value` with `.backward()` correct on arbitrary DAGs.
   Rows: `scalar reuse/accumulation`, `scalar mixed ops + nonlinearity`.
2. **Tensor autodiff with broadcasting** — the five `part2` rows, including
   `[N,D]+[D]` and `[N,1]*[1,D]`.
3. **NN primitives** — the four `part3` rows.
4. **Published artifact** — every row PASS (torch rows too, if torch is in your
   env); `RESULTS.md` with the passing table, the tolerance, and a short note on
   what the `cross_entropy` row took. This is the phase's verifiable artifact.

Proves (build-proven exam questions): (1) reverse-mode autodiff through
`linear` passing an independent numerical gradient check; (2) `softmax` +
`cross_entropy` whose engine-produced gradient matches the independently
computed `(p − onehot)/N` to tolerance.

---

## Vocabulary & primary sources

Definitions are at the level of *what role the term plays in the interface* —
implementing them is the build. The sources are concept anchors, the same ones
the field itself cites. **Do not read open-source autograd implementations
(micrograd, PyTorch internals, etc.) until after acceptance** — that's the one
way to void this phase.

### The field

- **reverse-mode automatic differentiation** — computing exact derivatives of a
  program by recording its operations and propagating derivatives from output
  back to inputs; one backward sweep yields the gradient w.r.t. *all* inputs,
  which is why it (and not forward mode) powers ML training. Primary source:
  Baydin, Pearlmutter, Radul, Siskind, *Automatic Differentiation in Machine
  Learning: a Survey*, JMLR 2018 — https://arxiv.org/abs/1502.05767 (§2–3 for
  the forward/reverse distinction; this is the standard reference).
- **computation graph** — the DAG built implicitly as forward ops run: nodes are
  values, edges point from each output to the inputs that produced it.
- **leaf** — a graph node with no inputs (created directly, not by an op);
  where gradients land.
- **topological order** — an ordering of a DAG where every node appears after
  all its predecessors; relevant whenever per-node work depends on completed
  predecessor work. https://en.wikipedia.org/wiki/Topological_sorting
- **layer normalization** — Ba, Kiros, Hinton, 2016 —
  https://arxiv.org/abs/1607.06450 (§3 defines exactly the forward you're
  implementing).
- **softmax / cross-entropy** — Goodfellow, Bengio, Courville, *Deep Learning*,
  ch. 6 (free: https://www.deeplearningbook.org/) — definitions, the
  logits-to-distribution role, and why stability matters.

### numpy (the only dependency)

- **`np.ndarray`** — N-D numeric array; `np.array(...)`, `np.zeros(shape)`,
  `np.random.randn(*shape)`.
- **`dtype`** — element type; `float64` = IEEE double (required this phase, see
  Tensor contract).
- **broadcasting** — numpy's rules for elementwise ops on mismatched shapes
  (the smaller operand is conceptually replicated along missing/size-1 axes).
  Read the rules before Part 2:
  https://numpy.org/doc/stable/user/basics.broadcasting.html
- **`@`** — matrix multiply (`np.matmul`), distinct from elementwise `*`;
  `[M,K] @ [K,N] → [M,N]`.
- **`.sum(axis, keepdims)`** — reduce along an axis (all axes when `None`);
  `keepdims=True` keeps the reduced axis as size 1 so the result broadcasts back.

### The oracle's method (so you can trust it)

- **central finite differences** — `(f(x+h) − f(x−h)) / 2h`, `h = 1e-6`: the
  suite perturbs each input element, recomputes the loss, and compares the
  numerical gradient to your `.grad`.
- **relative error** — `|analytic − numerical| / (|analytic| + |numerical| + ε)`;
  a row passes when the max over elements is under `1e-5`.

---

## Known failure modes (named, not solved)

Where implementations of this contract historically go wrong. The suite has a
row for each; no mechanisms here — finding them is the build.

- **Gradient loss under reuse.** A node consumed twice ends up with only one
  contribution. The `reuse/accumulation` row exists for this.
- **Order-dependent backward.** Correct on chains, wrong on diamonds — gradient
  read before fully formed. Shows up as wrong values on the mixed-ops rows.
- **Broadcast operands.** The whole difficulty of Part 2: `.grad` shape or value
  wrong for the operand that was broadcast. The `[N,D]+[D]` and `[N,1]*[1,D]`
  rows are aimed precisely at it; if `linear` passes but `b.grad` looks odd,
  this is where to look.
- **Softmax overflow.** Passes small-logit tests, blows up later. The stability
  identity is in the contract; honoring it is not optional.
- **Sum-vs-mean in `cross_entropy`.** Fails by exactly `N`. The contract says
  mean; believe it.
- **float32 anywhere in the path.** The oracle can't see `1e-5` through float32;
  rows fail mysteriously.

---

## Hand-back for review

1. `autograd.py` + the full suite output table (+ benchmark numbers if you took any).
2. One sentence per failure mode above: did it bite, and how you resolved it.

Review is principal-engineer style: correctness first, the interview attack on
your design (e.g. "what happens on a second `.backward()`?", "a leaf feeding two
losses?"), the next upgrade. Then Phase 1.1.
