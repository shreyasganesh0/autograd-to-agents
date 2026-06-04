# Tier 0 · Phase 0.1 — Autograd from scratch (scaffold)

**Deliverable of this phase:** a reverse-mode automatic-differentiation engine you wrote from scratch, plus the gradient-check suite (already shipped, validated) reporting every row PASS.

**What you'll own afterward:** every gradient in the rest of this plan stops being magic. When attention or a fused kernel or an RL loss misbehaves three tiers from now, you debug it at the level of "which Jacobian is wrong," not "the framework did something."

**Ground rule:** the spec + the conformance suite (`tests/test_autograd.py`) are the contract. Designing the computation graph, the topological order, and the backward wiring is the entire point — that's where the understanding lives. Write every line yourself. Any math you need is yours to do off-repo; this project ships code, not derivations.

---

## Why this phase exists (goals, rationale, what carries forward)

### The skill you're building

An intuition for how gradients propagate through composed operations — deep enough that you can debug a 50-line attention bug or a numerically-unstable RL loss at the level of *"which Jacobian is wrong"* rather than *"the framework did something."* When you're staring at a loss that won't decrease three tiers from now, you want to be the person who reaches for the autograd internals, not the person who tries random hyperparameter changes.

### Why "from scratch" is the right call here

Autograd is the substrate every subsequent tier sits on. Treat it as a black box (let PyTorch do the gradients for you) and you'll spend the rest of the curriculum unable to reason about:

- Why a custom CUDA kernel needs a custom backward (Tier 2.1 / FlashAttention).
- Why a training loop diverges silently (Tier 3.1 pretraining, Tier 3.2 RL).
- Why a fused op produces a different gradient than the unfused composition.
- Why ZeRO can shard optimizer states across GPUs without changing the math (Tier 2.2).
- Why a backward pass through a KV cache or a sampled token requires care (Tier 2.3, Tier 3.2).

After this phase, the rest of the project stops having an opaque substrate underneath it. That's the unlock.

### What carries forward to later tiers

- **Graph + topological-order pattern.** Reappears in any system that composes operations — compiler IRs (torch.compile, XLA), dataflow systems, the agent harness's tool-call graph (Tier 4.1). You'll recognize the shape every time.
- **Broadcasting backward.** The hardest correctness trap in this phase is exactly the same bug class as tensor-parallel gradient reduction (Tier 2.2) and stride math in a paged-KV allocator (Tier 2.3). Get it wrong here, get it wrong everywhere.
- **Fused softmax-CE.** A numerically-stable op with a hand-derived backward, motivated by avoiding intermediate-tensor materialization. This is the warm-up pattern for FlashAttention (Tier 2.1), which fuses attention's softmax + matmul for the same reason.
- **LayerNorm.** The spine of every transformer block. You'll touch it again in Tier 1.1 (transformer integration) and Tier 1.2 (the RMSNorm variant). Interviewers will ask you to defend your normalization choice; this phase is where you earn the answer.
- **Independent oracle discipline.** The five-gate harness validation protocol you're working against here is the same discipline every later phase requires — finite differences here, full-recompute oracle for KV cache, brute-force exact search for HNSW, judge calibration for evals. The shape of "how you know your build is correct" is set here.

### What good looks like

- Your `Tensor` class has a small surface area. If you're adding a method per op, fine; if you're adding methods for helpers and utilities, the design is leaking.
- Your `.backward()` has no per-op special-casing at the top level. Each op records its own local backward when it runs; `.backward()` just walks the graph and dispatches.
- You can answer, without running the code: *"What happens if I call `.backward()` twice on the same output?"* and *"What happens if a single leaf parameter feeds two different losses summed together?"* Both are standard interview-attack questions for autograd implementations.
- The numerical errors in your harness output are at the floor expected from `float64` + central differences (~1e-9 for linear ops, ~1e-7 for finite-diff through softmax-CE). If they're 1e-5 or worse but still under TOL, something is subtly wrong — investigate.

### Why this is the shape of the deliverable

A single `.py` module + a harness that proves every gradient. Autograd is the canonical *"small library, deep correctness invariants"* problem — the library is ~200 lines, but the bugs are silent (a wrong gradient still trains the network, just toward the wrong answer). The only honest way to know it works is an independent oracle (finite differences + PyTorch). Hence the harness, hence the `(p − y)/N` clean-form check on softmax-CE, hence the `float64` tolerance.

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

Run `python3 tests/test_autograd.py` after every part. Unbuilt parts report **SKIP**; watch rows turn **PASS**.

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

## API contract (what `tests/test_autograd.py` imports)

Put your code in **`src/autograd/autograd.py`**, exposing the names below. The harness (`tests/test_autograd.py`) imports them by these names — wiring up how `tests/` resolves the `src/` module (a `conftest.py`, an editable install, or `PYTHONPATH`) is your packaging call. For each name: signature, what it computes (the observable forward behavior — i.e. the spec), why it exists in any neural-network library, and what your backward must do. The backward *implementation* is yours to design; the backward *requirement* (the shape and the fact that it must exist) is part of the contract.

### Scalar engine — `Value`

```
Value(data: float)
  .data : float (mutable)
  .grad : float (0.0 initially; accumulated after .backward())
  + - * /  and  ** const
  at least one nonlinearity: .tanh() / .relu() / .exp()
  .backward()
```

- **What it represents:** a single floating-point number that participates in a computation graph. When you do `c = a * b`, `c` is a new `Value` that remembers it was produced from `a` and `b` via a multiply.
- **Why it exists:** the simplest possible autograd. Scalar reverse-mode is the educational core of the whole engine; once it works, the Tensor version is the same idea generalized to arrays.
- **What backward must do:** calling `.backward()` on any node seeds that node's `.grad = 1.0` and then walks every ancestor in **reverse topological order**, populating their `.grad` slots. A node that's used twice (e.g. `f = a*b + a`) must **accumulate** both contributions to `a.grad` — assignment loses one of them silently.

### Tensor engine — `Tensor`

```
Tensor(data: np.ndarray, requires_grad: bool = True)
  .data : np.ndarray (float64, mutable in place)
  .grad : np.ndarray (same shape as .data) or None before backward
  + - *  (elementwise, with broadcasting)
  @      (matrix multiply)
  .sum(axis=None, keepdims=False)
  .backward(grad=None)
```

- **What it represents:** an N-dimensional array that participates in a computation graph the same way `Value` does, but element-wise. Forward ops produce new `Tensor`s; backward fills in `.grad` for every input that has `requires_grad=True`.
- **Why it exists:** real models work with batches of vectors, not scalars. Generalizing to N-D arrays introduces the load-bearing complication of this phase: **broadcasting**.
- **What backward must do:** for a scalar output, `.backward()` defaults `grad` to 1.0 and propagates. The hard part: when a forward op **broadcast** an operand (e.g. `[N,D] + [D]` broadcast the `[D]` bias across the batch axis), the gradient flowing into that operand must be **reduced back down to its original shape** by summing over the broadcast axes. If you skip this reduction, the gradient shape doesn't match the data shape and either the harness fails or, worse, training silently learns the wrong thing.

### NN primitives (compose Tensor ops so `.backward()` works automatically)

These are not new graph nodes — they're functions that compose `+`, `*`, `@`, `.sum()` from your Tensor layer. If your Tensor backward is correct, the gradients through these come for free.

#### `linear(x, W, b)`

```
x: [N, In]    W: [In, Out]    b: [Out]    →  [N, Out]
```

- **What it computes:** the affine transformation `y = xW + b`. Multiply the batched input by the weight matrix, then add the bias (broadcast across the batch).
- **Why it exists:** every fully-connected layer in every neural network is this function. The transformer's MLP block is `linear` → activation → `linear`. The attention projections are `linear`s. The classifier head is a `linear`.
- **What it forces you to debug:** matmul backward + broadcasting-add backward, composed. The bias gradient (`b.grad`) has shape `[Out]` but flows from a `[N, Out]` upstream gradient — that's the broadcast-reduce you have to get right.

#### `softmax(x, axis=-1)`

```
x: [..., C]    →  [..., C]    rows sum to 1 along `axis`
```

- **What it computes:** `softmax(x)_i = exp(x_i) / sum_j exp(x_j)` along `axis`. Output values are in (0, 1) and sum to 1 along the chosen axis — a probability distribution.
- **Why it exists:** the standard way to turn a vector of unnormalized scores (*logits*) into a probability distribution over classes. Used everywhere a model needs to produce a distribution: classifier outputs, next-token prediction in LLMs, attention weights inside the transformer.
- **Numerical-stability requirement (part of the spec, not optional):** subtract the row max from `x` before exponentiating. Mathematically `softmax(x) == softmax(x - max(x))` (the constant cancels in the ratio), but without the subtraction `exp(x_i)` overflows to `inf` for moderately-sized inputs (`exp(710)` is already `inf` in float64). Every robust softmax implementation does this.

#### `cross_entropy(logits, targets)`

```
logits: [N, C]    targets: int array [N], values in [0, C)    →  scalar
```

- **What it computes:** `mean_over_batch( -log p[target_i] )` where `p = softmax(logits, axis=-1)` and `target_i` is the integer class index for example `i`. Equivalently: take the softmax, look up the probability of the true class for each example, take negative log, average across the batch.
- **Why it exists:** the standard loss function for classification. Measures how *surprised* the model is by the true label. Together with softmax, it's the output stage of essentially every classifier and every LLM (where "classes" = vocabulary tokens, so this is the next-token-prediction loss).
- **Critical contract — `mean`, not `sum`:** the reduction is the **mean** (divide by batch size `N`). The harness's independent `(softmax(logits) − onehot(targets)) / N` oracle assumes this; if you implement sum-reduction, the row will fail by exactly a factor of `N` and you'll spend an hour staring at it.
- **Why this one is famous:** the analytic gradient of softmax-CE through `logits` collapses to the clean form `(p − onehot(target)) / N`. The fused form is dramatically simpler than chain-ruling through softmax then cross-entropy separately, and is also more numerically stable (avoids computing `log(p_i)` for tiny `p_i`). The harness checks this clean form independently — when the `cross_entropy` row's `clean(p-y)/N` error is ~1e-16, you've empirically confirmed the identity.

#### `layernorm(x, gamma, beta, eps=1e-5)`

```
x: [..., D]    gamma: [D]    beta: [D]    →  same shape as x
```

- **What it computes:** for each "row" of `x` (along the last axis), subtract the mean, divide by `sqrt(variance + eps)`, then element-wise multiply by `gamma` and add `beta`. Each row ends up with (approximately) zero mean and unit variance, then is rescaled and shifted by the learned per-feature parameters.
- **Why it exists:** stabilizes training of deep networks by keeping each layer's input distribution well-behaved (no exploding/vanishing activations). Used pervasively in transformers — before/after every attention block and every MLP block. The `eps` prevents division by zero on flat rows. The `gamma` and `beta` give the network the freedom to *undo* the normalization if it wants to (so layernorm doesn't restrict expressivity).
- **What makes the backward subtle:** the mean and variance of a row both depend on *every* element of that row, so perturbing one element shifts the mean and variance, which changes every element's normalized value. The gradient through the normalization step is therefore **not local element-wise** — each element's gradient depends on a sum across the row. Your backward has to account for this; getting the per-row reductions right is the load-bearing detail.
- **What you'll do with it later:** Tier 1.1 wires it into a real transformer block. Tier 1.2 builds RMSNorm (which drops the mean-centering — only the divide-by-rms remains) and asks you to compare. Naming the difference precisely is a standard interview question.

### Naming + execution

Named differently in your code? Edit the import shim at the top of `main()` in `tests/test_autograd.py`. Semantics must match — especially the `cross_entropy` mean reduction and `.data` being `float64` (the finite-difference oracle requires it).

**Run:** `python3 tests/test_autograd.py` → table of PASS/FAIL/SKIP, exit 0 iff no FAIL/ERROR.

---

## Acceptance criteria (phase-level "done")

1. `python3 tests/test_autograd.py` → **all rows PASS** (torch rows too, if torch is in your env), max rel error well under `1e-5` (you should see ~`1e-9`–`1e-10` for the linear/tensor ops; CE via finite-diff is looser, ~`1e-7`, which is expected).
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

1. Your `autograd.py` + the `tests/test_autograd.py` run output (the table).
2. One sentence per trap above: did it bite you, and how did you resolve it?

I'll review principal-engineer style: correctness, any overstated "it works" claims, the interview attack on your design (e.g., "what happens if a leaf feeds two different losses?"), and the next upgrade. Then we advance to Phase 1.1.

*Start Part 1 when ready — `autograd.py` is yours to write from a blank file.*
