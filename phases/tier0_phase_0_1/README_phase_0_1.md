# Tier 0 · Phase 0.1 — Autograd from scratch (scaffold)

**Deliverable of this phase:** a reverse-mode automatic-differentiation engine you wrote from scratch, plus a published gradient-check suite proving your gradients match an independent oracle (finite differences, and PyTorch where available) to numerical tolerance.

**What you'll own afterward:** every gradient in the rest of this plan stops being magic. When attention or a fused kernel or an RL loss misbehaves three tiers from now, you will debug it at the level of "which Jacobian is wrong," not "the framework did something."

**Ground rule:** I gave you the **contract** and the **conformance suite** (`gradcheck.py`), not a skeleton. Designing the computation graph, the topological order, and the backward wiring is the entire point — that's where the understanding lives. Write every line yourself.

---

## Exam questions this phase targets

Two are **build-proven** here (the suite is your proof); one is **derive-on-paper** here and gets *built* in a later optimizer phase.

1. **[build-proven]** Derive backprop through a linear layer (the three Jacobians: ∂L/∂W, ∂L/∂b, ∂L/∂x). Implement reverse-mode autodiff and pass a numerical gradient check vs PyTorch.
2. **[build-proven]** Derive the gradient of softmax-cross-entropy by hand; explain *why* the combined gradient is so clean. (The suite's `cross_entropy` check verifies your analytic grad equals `(p − y)/N` — that clean form *is* the answer; you must be able to say why.)
3. **[derive-on-paper now]** Why does Adam work? Write the update rule from memory, explain bias correction, and map how its moment states create the memory bottleneck ZeRO attacks. No code this phase — but write the derivation now while the gradient machinery is fresh.

---

## The build, in five parts (each gated independently by the suite)

Run `python3 gradcheck.py` after every part. Unbuilt parts report **SKIP**; watch rows turn **PASS**.

### Part 0 — Derivations on paper (before any code) → `DERIVATIONS.md`
Do not write code yet. Derive, by hand, in a markdown file:
- ∂L/∂W, ∂L/∂b, ∂L/∂x for `y = xW + b` followed by a scalar loss. State each as a matrix expression and **check the shapes match the operands** (this is your debugging invariant forever).
- Softmax `p = softmax(z)`, then cross-entropy `L = −log p[target]`. Derive ∂L/∂z **fused**, and show it collapses to `p − onehot(target)`. Write one paragraph on *why* the exp in softmax and the log in CE cancel — this is the exam answer.
- The Adam update + bias correction (exam item 3).
**Acceptance:** paste `DERIVATIONS.md`; I review it as a reviewer would — looking for shape errors, hand-waving at the softmax-CE cancellation, and whether you can defend the clean form.

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
**Suite rows:** the four `part3` checks. The `cross_entropy` row also verifies the `(p − y)/N` clean form independently — when that passes, you've *empirically* confirmed your Part-0 derivation.

### Part 4 — The gradient-check suite as a published artifact 🔨
The suite is provided; your job is to make **every row PASS** and then turn the run into the proof: a short `RESULTS.md` with the passing table, the tolerance, and one paragraph on the `(p−y)/N` result. If `torch` is installed in your env, the `part4-torch` rows light up as the stronger oracle — get those green too (that's the literal "matches PyTorch" proof the plan calls for).
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

1. `DERIVATIONS.md` reviewed and correct, including a defensible "why softmax-CE is clean."
2. `python3 gradcheck.py` → **all rows PASS** (torch rows too, if torch is in your env), max rel error well under `1e-5` (you should see ~`1e-9`–`1e-10` for the linear/tensor ops; CE via finite-diff is looser, ~`1e-7`, which is expected).
3. `RESULTS.md` published with the table + the `(p−y)/N` paragraph. The suite is in the repo so a stranger can rerun it.

---

## Principal-engineer notes / traps (no solutions — just where people bleed)

- **Accumulate, don't assign.** If `.grad = ...` instead of `.grad += ...`, a node used twice loses a term. The `reuse/accumulation` row exists specifically to catch this. Decide how grads get zeroed between independent backward passes and write it down.
- **Topological order is not optional.** Running `_backward` in the wrong order means a node's grad isn't fully accumulated before it's used. Build the topo sort explicitly; don't rely on insertion order.
- **Broadcasting backward is the whole difficulty of Part 2.** Forward broadcasting is free (numpy does it); the gradient must travel *back* through the broadcast by summing over the expanded axes and reshaping to the operand. If `[N,D]+[D]` passes but the bias grad is subtly off, you're not reducing correctly.
- **Numerical stability in softmax is a correctness issue, not a nicety.** Subtract the row-max before `exp`. Skipping it can still pass small-logit tests and then blow up later — do it now.
- **float32 will fail the tolerance.** Central differences on float32 won't hit `1e-5`. Keep `.data` float64 this phase.
- **Don't fuse softmax-CE just to pass the row.** You *may* implement a fused stable CE with a hand-written backward — but only after Part 0, so the fusion is a thing you understood and chose, not a thing you copied to make a number go green.

---

## What you hand back for review

1. `DERIVATIONS.md` (after Part 0 — before you write engine code).
2. Your `autograd.py` + the `gradcheck.py` run output (the table).
3. One sentence per trap above: did it bite you, and how did you resolve it?

I'll review principal-engineer style: correctness, any overstated "it works" claims, the interview attack on your design (e.g., "what happens if a leaf feeds two different losses?"), and the next upgrade. Then we advance to Phase 1.1.

*Start Part 0 now. Paste `DERIVATIONS.md` when ready — engine code comes after the derivations are sound.*
