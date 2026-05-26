# Tier 0 · Phase 0.1 — Autograd from scratch (scaffold)

**Deliverable of this phase:** a reverse-mode automatic-differentiation engine you wrote from scratch, plus the gradient-check suite (already shipped, validated) reporting every row PASS.

**What you'll own afterward:** every gradient in the rest of this plan stops being magic. When attention or a fused kernel or an RL loss misbehaves three tiers from now, you debug it at the level of "which Jacobian is wrong," not "the framework did something."

**Ground rule:** the spec + the conformance suite (`gradcheck.py`) are the contract. Designing the computation graph, the topological order, and the backward wiring is the entire point — that's where the understanding lives. Write every line yourself. Any math you need is yours to do off-repo; this project ships code, not derivations.

---

## Exam questions this phase targets (build-proven)

1. Implement reverse-mode autodiff for a `linear(x, W, b)` layer and pass a numerical gradient check (central finite differences in float64, and PyTorch where available).
2. Implement `softmax` + `cross_entropy` such that the suite's `cross_entropy` row PASSes — the analytic gradient your engine produces must equal `(softmax(logits) − onehot(targets)) / N` to numerical tolerance. The clean form is the answer; the suite verifies it independently of your code.

---

## Prerequisites — concepts this phase uses

These appear in the spec, the API contract, and the harness. They are *library / vocabulary* concepts, not the algorithm you're building. You need to recognize them. You should NOT look up how they're implemented — implementing them is the build.

### numpy primitives

- **`numpy.ndarray`** — an N-dimensional array of numbers, stored contiguously in memory. Created with `np.array([[1,2],[3,4]])`, `np.zeros(shape)`, `np.random.randn(*shape)`, etc.
- **`dtype`** — the element type. `float64` is a 64-bit IEEE double; `float32` is single-precision. This phase requires `float64` because the finite-difference oracle (`h ≈ 1e-6`) needs the precision to be meaningful; `float32` is too coarse and will fail the tolerance check.
- **broadcasting** — numpy's rule for elementwise ops on mismatched-shape arrays. `np.array([[1,2,3],[4,5,6]]) + np.array([10,20,30])` adds the 1-D array to each row, producing a `[2,3]` result. The "smaller" operand is conceptually replicated along the missing axes. Full rules: https://numpy.org/doc/stable/user/basics.broadcasting.html. Backward broadcasting (gradients flowing back through a broadcast op) is the hardest correctness trap in Part 2 — read the rules now.
- **`@` operator** — matrix multiply. `A @ B` is `np.matmul(A, B)`. Different from `*` (elementwise). Shape rule: `[M,K] @ [K,N] → [M,N]`.
- **`.sum(axis=None, keepdims=False)`** — reduces along the given axis (or all axes when `None`). `keepdims=True` keeps the reduced axis as size 1 so the result broadcasts back cleanly.

### autograd vocabulary

These are the names your engine must expose. The *semantics* are described in the API contract below; the *implementation* is yours.

- **`Tensor`** — in any autograd library (PyTorch, TF, JAX, micrograd), a `Tensor` is a numeric array bundled with metadata that lets the library track operations done to it, so gradients can be computed later. You will define your own `Tensor` class with this behavior.
- **`.data`** — the underlying numeric value (a Python float for `Value`, an `ndarray` for `Tensor`). The harness reads and mutates this directly when running finite differences.
- **`.grad`** — the slot where the computed gradient ends up. `None` (or zero) before `.backward()` runs; an array of the same shape as `.data` afterward.
- **`requires_grad`** — boolean attribute. If `False`, the engine should skip gradient accumulation for this tensor (treat it as a constant). The harness uses this to mark random multipliers as constants.
- **`.backward(grad=None)`** — the standard autograd API: calling this on a scalar (size-1) output should populate `.grad` on every ancestor tensor with `requires_grad=True`. `grad` defaults to 1.0 for scalar outputs. What `.backward()` does internally — walk the computation graph in some order, compute local Jacobians, accumulate them — is exactly what you're building.

### graph concepts

- **computation graph** — the implicit DAG you build as forward operations run. Each node is a `Tensor` (or `Value`); each edge points from an output back to the inputs that produced it. The backward pass traverses this DAG.
- **leaf** — a node with no inputs in the graph (e.g. a parameter you created directly, not as the result of an op). Leaves are where gradients land.
- **topological order** — an ordering of a DAG such that every node appears after all its predecessors. The backward pass must visit nodes in reverse topological order so that a node's gradient is fully accumulated *before* it's used to compute its inputs' gradients. CS reference: https://en.wikipedia.org/wiki/Topological_sorting

### numerical checking

- **central finite differences** — approximating a derivative as `(f(x+h) − f(x−h)) / 2h`. The harness uses this as an independent oracle: it perturbs each input element by `h = 1e-6`, recomputes the scalar loss, and compares the resulting numerical gradient to *your* `.grad` after `.backward()`.
- **relative error** — `|analytic − numerical| / (|analytic| + |numerical| + ε)`. A row PASSes when the max relative error across all gradient elements is below `TOL = 1e-5`. Expect ~`1e-9` for linear/tensor ops and ~`1e-7` for finite-diff through softmax/CE; both pass comfortably.

### offered as optional, not required

The owner has chosen to work out any math privately. The suite *empirically* confirms correctness — if you'd rather skip paper derivations entirely and just iterate on the code until rows go green, that's a valid path. The traps section below names where intuition (not algebra) typically breaks.

---

## The build, in four parts (each gated independently by the suite)

Run `python3 gradcheck.py` after every part. Unbuilt parts report **SKIP**; watch rows turn **PASS**.

### Part 1 — Scalar autograd 🔨
A `Value` scalar with a computation graph and `.backward()`. The reverse pass must visit nodes in reverse-topological order and **accumulate** (`+=`) gradients, so a value used twice gets both contributions.
**Suite rows:** `scalar reuse/accumulation`, `scalar mixed ops + nonlinearity`.

### Part 2 — Tensor reverse-mode autodiff with broadcasting 🔨
A `Tensor` over float64 numpy arrays: `+ - * @ .sum()`, with **broadcasting**. The hard, load-bearing idea: when an op broadcasts an operand, the backward pass must **reduce (sum) the upstream gradient back down to that operand's original shape**. Get this wrong and every bias gradient in the plan is silently wrong.
**Suite rows:** the five `part2` checks, including `[N,D]+[D]` and `[N,1]*[1,D]`.

### Part 3 — NN primitives by hand 🔨
Built **on top of** your Part-2 Tensor ops so gradients flow through `.backward()`:
- `linear(x, W, b)`
- `softmax(x, axis=-1)` — numerically stable (subtract the max)
- `cross_entropy(logits, targets)` — **mean** over the batch; integer targets
- `layernorm(x, gamma, beta, eps=1e-5)` — over the last axis
**Suite rows:** the four `part3` checks. The `cross_entropy` row also verifies the `(p − y)/N` clean form independently — when that passes, you've empirically confirmed the analytic identity.

### Part 4 — The gradient-check suite as a published artifact 🔨
The suite is provided; your job is to make **every row PASS** and then turn the run into the proof: a short `RESULTS.md` with the passing table, the tolerance, and one paragraph on what made the `cross_entropy` row tricky (or easy) for you. If `torch` is installed in your env, the `part4-torch` rows light up as the stronger oracle — get those green too (that's the literal "matches PyTorch" proof the plan calls for).
**This is the verifiable artifact for the phase.** Publish the suite + results.

---

## API contract (what `gradcheck.py` imports)

Put your code in **`autograd.py`** next to the suite, exposing:

```
Value(data: float)        .data (float, mutable)   .grad (float)   .backward()
   + - * / **(const) and at least one of .tanh()/.relu()/.exp()

Tensor(data: np.ndarray float64, requires_grad=True)
   .data (np.ndarray, mutable in place)   .grad (np.ndarray | None)   .backward(grad=None)
   + - *  (elementwise, broadcasting)   @ (matmul)   .sum(axis=None, keepdims=False)

linear(x, W, b)               x:[N,In] W:[In,Out] b:[Out] -> [N,Out]
softmax(x, axis=-1)           rows sum to 1
cross_entropy(logits, targets) logits:[N,C] targets:int[N] -> scalar, MEAN of -log p[target]
layernorm(x, gamma, beta, eps=1e-5)   normalize over last axis; gamma,beta:[D]
```

Named differently? Edit the import shim at the top of `main()` in `gradcheck.py`. Semantics must match — especially: `cross_entropy` is the **mean** (the `(p−y)/N` oracle assumes it), and `.data` is **float64** (finite differences needs it).

**Run:** `python3 gradcheck.py` → table of PASS/FAIL/SKIP, exit 0 iff no FAIL/ERROR.

---

## Acceptance criteria (phase-level "done")

1. `python3 gradcheck.py` → **all rows PASS** (torch rows too, if torch is in your env), max rel error well under `1e-5` (you should see ~`1e-9`–`1e-10` for the linear/tensor ops; CE via finite-diff is looser, ~`1e-7`, which is expected).
2. `RESULTS.md` published with the table + a short note on the `cross_entropy` row. The suite is in the repo so a stranger can rerun it.

---

## Principal-engineer notes / traps (no solutions — just where people bleed)

- **Accumulate, don't assign.** If `.grad = ...` instead of `.grad += ...`, a node used twice loses a term. The `reuse/accumulation` row exists specifically to catch this. Decide how grads get zeroed between independent backward passes and write it down.
- **Topological order is not optional.** Running `_backward` in the wrong order means a node's grad isn't fully accumulated before it's used. Build the topo sort explicitly; don't rely on insertion order.
- **Broadcasting backward is the whole difficulty of Part 2.** Forward broadcasting is free (numpy does it); the gradient must travel *back* through the broadcast by summing over the expanded axes and reshaping to the operand. If `[N,D]+[D]` passes but the bias grad is subtly off, you're not reducing correctly.
- **Numerical stability in softmax is a correctness issue, not a nicety.** Subtract the row-max before `exp`. Skipping it can still pass small-logit tests and then blow up later — do it now.
- **float32 will fail the tolerance.** Central differences on float32 won't hit `1e-5`. Keep `.data` float64 this phase.
- **Don't fuse softmax-CE just to pass the row.** You *may* implement a fused stable CE with a hand-written backward — but only as an informed choice (you understand what the fusion is doing and chose it), not as a shortcut to make the row go green.

---

## What you hand back for review

1. Your `autograd.py` + the `gradcheck.py` run output (the table).
2. One sentence per trap above: did it bite you, and how did you resolve it?

I'll review principal-engineer style: correctness, any overstated "it works" claims, the interview attack on your design (e.g., "what happens if a leaf feeds two different losses?"), and the next upgrade. Then we advance to Phase 1.1.

*Start Part 1 when ready — `autograd.py` is yours to write from a blank file.*
