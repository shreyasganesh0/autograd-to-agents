#!/usr/bin/env python3
"""
Tier 0 - Phase 0.1 : Autograd conformance + gradient-check suite
=================================================================

This is an INDEPENDENT ORACLE. It does not implement autograd. It checks YOUR
implementation two ways:

  1. Central finite differences (numpy only, always runs) -- the ground truth.
     It never trusts another autograd; it only calls YOUR forward and reads
     YOUR .grad after YOUR .backward().
  2. PyTorch autograd comparison (optional; only if torch is importable) -- a
     second, stronger oracle for the nn primitives. This is the "matches
     PyTorch to numerical tolerance" proof the plan asks for.

HOW TO USE
----------
Put your implementation in a module named `autograd.py` next to this file,
exposing the names in the CONTRACT below. Then run:

    python3 gradcheck.py

The suite runs Part 1 -> Part 4 in order. Anything you haven't built yet is
reported as SKIP (caught NotImplementedError / AttributeError / TypeError), so
you can run it from the moment Part 1 exists and watch rows go green.

CONTRACT (what this harness imports and calls)
----------------------------------------------
Scalar (Part 1):
    ag.Value(data: float)
        .data : float (mutable)
        .grad : float (0.0 before backward; set/accumulated after)
        supports  + - * / and ** (constant exponent); operands may be Value or
        python number. At least one nonlinearity: .tanh() / .relu() / .exp().
        .backward(): seeds this node's grad = 1.0, accumulates grads into every
                     ancestor via reverse-topological order.

Tensor (Parts 2-3):
    ag.Tensor(data: np.ndarray, requires_grad: bool = True)
        .data : np.ndarray, dtype float64 (mutable, in place)
        .grad : np.ndarray (same shape as .data) or None before backward
        ops: + - *  (elementwise, BROADCASTING),  @  (matmul),
             .sum(axis=None, keepdims=False)
        broadcasting backward MUST reduce grads back to each operand's shape.
        .backward(grad=None): for a scalar (size-1) output, grad defaults to 1.0.

NN primitives (Part 3), composed so grads flow through .backward():
    ag.linear(x, W, b)            x:[N,In]  W:[In,Out]  b:[Out]   -> [N,Out] = x@W + b
    ag.softmax(x, axis=-1)        -> same shape, rows sum to 1
    ag.cross_entropy(logits, targets)  logits:[N,C]  targets: int array [N]
                                  -> SCALAR, the MEAN over the batch of -log p[target]
    ag.layernorm(x, gamma, beta, eps=1e-5)   normalize over the LAST axis;
                                  gamma,beta:[D]  -> same shape as x

If you name things differently, edit the thin import shim at the top of main().
Designing the internals is YOUR job; this file never shows you how.
"""

import math
import numpy as np

# ----------------------------- config -------------------------------------
SEED = 0
EPS = 1e-6            # central-difference step
TOL = 1e-5           # max relative error to PASS (float64 + central diff is generous)
np.random.seed(SEED)

try:
    import torch
    HAVE_TORCH = True
except Exception:
    HAVE_TORCH = False


# --------------------------- oracle helpers --------------------------------
def _scalar(loss):
    """Read a scalar value out of YOUR loss object's .data (size-1 expected)."""
    return float(np.asarray(loss.data).reshape(-1)[0])


def max_rel_err(analytic, numerical):
    a = np.asarray(analytic, dtype=np.float64)
    n = np.asarray(numerical, dtype=np.float64)
    if a.shape != n.shape:
        return math.inf, f"shape mismatch analytic{a.shape} vs numerical{n.shape}"
    denom = np.maximum(1e-8, np.abs(a) + np.abs(n))
    return float(np.max(np.abs(a - n) / denom)), ""


def numerical_grad(forward, param):
    """Central-difference gradient of scalar forward() wrt param.data.
    Mutates param.data in place and restores it. Works for float (scalar Value)
    or float64 ndarray (Tensor)."""
    data = param.data
    if np.ndim(data) == 0:                      # scalar Value
        orig = float(data)
        param.data = orig + EPS; fph = float(forward())
        param.data = orig - EPS; fmh = float(forward())
        param.data = orig
        return (fph - fmh) / (2 * EPS)
    if data.dtype != np.float64:
        raise TypeError(f".data dtype is {data.dtype}; the contract requires float64")
    grad = np.zeros_like(data)
    for idx in np.ndindex(data.shape):
        o = data[idx]
        data[idx] = o + EPS; fph = float(forward())
        data[idx] = o - EPS; fmh = float(forward())
        data[idx] = o
        grad[idx] = (fph - fmh) / (2 * EPS)
    return grad


# ----------------------------- reporting -----------------------------------
class Report:
    def __init__(self):
        self.rows = []  # (part, name, status, detail)

    def add(self, part, name, status, detail=""):
        self.rows.append((part, name, status, detail))

    def check(self, part, name, fn):
        """Run fn(); fn returns (ok: bool, detail: str). SKIP on NotImplemented/Attr/Type."""
        try:
            ok, detail = fn()
            self.add(part, name, "PASS" if ok else "FAIL", detail)
        except (NotImplementedError, AttributeError, TypeError) as e:
            self.add(part, name, "SKIP", f"not implemented yet ({type(e).__name__}: {e})")
        except Exception as e:
            self.add(part, name, "ERROR", f"{type(e).__name__}: {e}")

    def print(self):
        wp = max(4, max(len(r[0]) for r in self.rows))
        wn = max(4, max(len(r[1]) for r in self.rows))
        print(f"\n{'PART'.ljust(wp)}  {'CHECK'.ljust(wn)}  STATUS  DETAIL")
        print("-" * (wp + wn + 40))
        for part, name, status, detail in self.rows:
            print(f"{part.ljust(wp)}  {name.ljust(wn)}  {status:6}  {detail}")
        passed = sum(s == "PASS" for *_, s, _ in [(r[0], r[1], r[2], r[3]) for r in self.rows])
        n_pass = sum(r[2] == "PASS" for r in self.rows)
        n_fail = sum(r[2] == "FAIL" for r in self.rows)
        n_err = sum(r[2] == "ERROR" for r in self.rows)
        n_skip = sum(r[2] == "SKIP" for r in self.rows)
        print("-" * (wp + wn + 40))
        print(f"PASS {n_pass}   FAIL {n_fail}   ERROR {n_err}   SKIP {n_skip}   (tol={TOL}, eps={EPS})")
        return n_fail == 0 and n_err == 0


def _grad_of(param):
    g = param.grad
    if g is None:
        raise AssertionError(".grad is None after backward() -- did backward run for this leaf?")
    return np.asarray(g, dtype=np.float64)


# ------------------------------- PART 1 ------------------------------------
def run_part1(ag, rep):
    P = "part1"

    def reuse_accumulation():
        # f = a*b + a   -> df/da = b + 1, df/db = a   (a is used twice; tests accumulation)
        a, b = ag.Value(-2.7), ag.Value(3.1)

        def fwd():
            return _scalar(a * b + a)
        out = a * b + a
        out.backward()
        ea, _ = max_rel_err(a.grad, numerical_grad(fwd, a))
        eb, _ = max_rel_err(b.grad, numerical_grad(fwd, b))
        e = max(ea, eb)
        return e <= TOL, f"max_rel_err={e:.2e}"

    def mixed_ops_nonlinearity():
        # f = (a*b - b/ a + a**3).tanh()
        a, b = ag.Value(1.3), ag.Value(-0.7)

        def fwd():
            return _scalar((a * b - b / a + a ** 3).tanh())
        out = (a * b - b / a + a ** 3).tanh()
        out.backward()
        ea, _ = max_rel_err(a.grad, numerical_grad(fwd, a))
        eb, _ = max_rel_err(b.grad, numerical_grad(fwd, b))
        e = max(ea, eb)
        return e <= TOL, f"max_rel_err={e:.2e}"

    rep.check(P, "scalar reuse/accumulation", reuse_accumulation)
    rep.check(P, "scalar mixed ops + nonlinearity", mixed_ops_nonlinearity)


# ------------------------------- PART 2 ------------------------------------
def _const(ag, shape):
    return ag.Tensor(np.random.randn(*shape).astype(np.float64), requires_grad=False)


def run_part2(ag, rep):
    P = "part2"

    def elementwise_noscale():
        x = ag.Tensor(np.random.randn(4, 3).astype(np.float64))
        y = ag.Tensor(np.random.randn(4, 3).astype(np.float64))
        R = _const(ag, (4, 3))

        def fwd():
            return _scalar(((x * y + x) * R).sum())
        loss = ((x * y + x) * R).sum()
        loss.backward()
        ex, _ = max_rel_err(_grad_of(x), numerical_grad(fwd, x))
        ey, _ = max_rel_err(_grad_of(y), numerical_grad(fwd, y))
        e = max(ex, ey)
        return e <= TOL, f"max_rel_err={e:.2e}"

    def broadcast_add():
        # [N,D] + [D]  -> grad wrt the [D] bias must SUM over the broadcast (N) axis
        x = ag.Tensor(np.random.randn(5, 3).astype(np.float64))
        bvec = ag.Tensor(np.random.randn(3).astype(np.float64))
        R = _const(ag, (5, 3))

        def fwd():
            return _scalar(((x + bvec) * R).sum())
        loss = ((x + bvec) * R).sum()
        loss.backward()
        ex, _ = max_rel_err(_grad_of(x), numerical_grad(fwd, x))
        eb, db = max_rel_err(_grad_of(bvec), numerical_grad(fwd, bvec))
        e = max(ex, eb)
        return e <= TOL, f"max_rel_err={e:.2e} {db}"

    def broadcast_mul_2d():
        # [N,1] * [1,D]  -> outer-product style broadcast, both operands reduce
        c = ag.Tensor(np.random.randn(4, 1).astype(np.float64))
        r = ag.Tensor(np.random.randn(1, 3).astype(np.float64))
        R = _const(ag, (4, 3))

        def fwd():
            return _scalar(((c * r) * R).sum())
        loss = ((c * r) * R).sum()
        loss.backward()
        ec, _ = max_rel_err(_grad_of(c), numerical_grad(fwd, c))
        er, _ = max_rel_err(_grad_of(r), numerical_grad(fwd, r))
        e = max(ec, er)
        return e <= TOL, f"max_rel_err={e:.2e}"

    def matmul_and_sum():
        x = ag.Tensor(np.random.randn(6, 4).astype(np.float64))
        W = ag.Tensor(np.random.randn(4, 5).astype(np.float64))
        R = _const(ag, (6, 5))

        def fwd():
            return _scalar(((x @ W) * R).sum())
        loss = ((x @ W) * R).sum()
        loss.backward()
        ex, _ = max_rel_err(_grad_of(x), numerical_grad(fwd, x))
        ew, _ = max_rel_err(_grad_of(W), numerical_grad(fwd, W))
        e = max(ex, ew)
        return e <= TOL, f"max_rel_err={e:.2e}"

    def sum_axis_keepdims():
        x = ag.Tensor(np.random.randn(4, 3).astype(np.float64))
        R = _const(ag, (4, 1))

        def fwd():
            return _scalar((x.sum(axis=1, keepdims=True) * R).sum())
        loss = (x.sum(axis=1, keepdims=True) * R).sum()
        loss.backward()
        ex, _ = max_rel_err(_grad_of(x), numerical_grad(fwd, x))
        return ex <= TOL, f"max_rel_err={ex:.2e}"

    rep.check(P, "elementwise (no broadcast)", elementwise_noscale)
    rep.check(P, "broadcast add [N,D]+[D]", broadcast_add)
    rep.check(P, "broadcast mul [N,1]*[1,D]", broadcast_mul_2d)
    rep.check(P, "matmul x@W", matmul_and_sum)
    rep.check(P, "sum(axis, keepdims)", sum_axis_keepdims)


# ------------------------------- PART 3 ------------------------------------
def _softmax_np(z, axis=-1):
    z = z - z.max(axis=axis, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)


def run_part3(ag, rep):
    P = "part3"

    def linear_grads():
        N, In, Out = 5, 4, 3
        x = ag.Tensor(np.random.randn(N, In).astype(np.float64))
        W = ag.Tensor(np.random.randn(In, Out).astype(np.float64))
        b = ag.Tensor(np.random.randn(Out).astype(np.float64))
        R = _const(ag, (N, Out))

        def fwd():
            return _scalar((ag.linear(x, W, b) * R).sum())
        loss = (ag.linear(x, W, b) * R).sum()
        loss.backward()
        e = max(max_rel_err(_grad_of(x), numerical_grad(fwd, x))[0],
                max_rel_err(_grad_of(W), numerical_grad(fwd, W))[0],
                max_rel_err(_grad_of(b), numerical_grad(fwd, b))[0])
        return e <= TOL, f"max_rel_err={e:.2e}"

    def softmax_normalizes_and_grad():
        x = ag.Tensor(np.random.randn(4, 5).astype(np.float64))
        sm = ag.softmax(x, axis=-1)
        row_sums = np.asarray(sm.data).sum(axis=-1)
        if not np.allclose(row_sums, 1.0, atol=1e-6):
            return False, f"rows don't sum to 1: {row_sums}"
        R = _const(ag, (4, 5))

        def fwd():
            return _scalar((ag.softmax(x, axis=-1) * R).sum())
        loss = (ag.softmax(x, axis=-1) * R).sum()
        loss.backward()
        e, _ = max_rel_err(_grad_of(x), numerical_grad(fwd, x))
        return e <= TOL, f"max_rel_err={e:.2e}; rows sum to 1 OK"

    def cross_entropy_grad_and_cleanform():
        N, C = 6, 4
        logits = ag.Tensor(np.random.randn(N, C).astype(np.float64))
        targets = np.random.randint(0, C, size=N)

        def fwd():
            return _scalar(ag.cross_entropy(logits, targets))
        loss = ag.cross_entropy(logits, targets)
        loss.backward()
        num = numerical_grad(fwd, logits)
        e_fd, _ = max_rel_err(_grad_of(logits), num)

        # The punchline of the whole phase: for softmax-CE (MEAN reduction),
        # dL/dlogits == (softmax(logits) - onehot(targets)) / N.  Independent oracle.
        p = _softmax_np(np.asarray(logits.data), axis=-1)
        onehot = np.zeros((N, C)); onehot[np.arange(N), targets] = 1.0
        clean = (p - onehot) / N
        e_clean, _ = max_rel_err(_grad_of(logits), clean)
        e = max(e_fd, e_clean)
        return e <= TOL, f"fd={e_fd:.2e}  clean(p-y)/N={e_clean:.2e}"

    def layernorm_grads():
        N, D = 5, 4
        x = ag.Tensor(np.random.randn(N, D).astype(np.float64))
        gamma = ag.Tensor(np.random.randn(D).astype(np.float64))
        beta = ag.Tensor(np.random.randn(D).astype(np.float64))
        R = _const(ag, (N, D))

        def fwd():
            return _scalar((ag.layernorm(x, gamma, beta) * R).sum())
        loss = (ag.layernorm(x, gamma, beta) * R).sum()
        loss.backward()
        e = max(max_rel_err(_grad_of(x), numerical_grad(fwd, x))[0],
                max_rel_err(_grad_of(gamma), numerical_grad(fwd, gamma))[0],
                max_rel_err(_grad_of(beta), numerical_grad(fwd, beta))[0])
        return e <= TOL, f"max_rel_err={e:.2e}"

    rep.check(P, "linear x@W+b grads", linear_grads)
    rep.check(P, "softmax normalizes + grad", softmax_normalizes_and_grad)
    rep.check(P, "cross_entropy grad + (p-y)/N", cross_entropy_grad_and_cleanform)
    rep.check(P, "layernorm grads", layernorm_grads)


# ------------------------------- PART 4 ------------------------------------
def run_part4(ag, rep):
    P = "part4-torch"
    if not HAVE_TORCH:
        rep.add(P, "torch comparison", "SKIP", "torch not installed (optional stronger oracle)")
        return

    def torch_cross_entropy():
        N, C = 6, 4
        x_np = np.random.randn(N, C).astype(np.float64)
        tgt = np.random.randint(0, C, size=N)
        # yours
        logits = ag.Tensor(x_np.copy())
        loss = ag.cross_entropy(logits, tgt)
        loss.backward()
        mine = _grad_of(logits)
        # torch (mean reduction)
        t = torch.tensor(x_np, requires_grad=True, dtype=torch.float64)
        tl = torch.nn.functional.cross_entropy(t, torch.tensor(tgt))
        tl.backward()
        ref = t.grad.detach().numpy()
        e, _ = max_rel_err(mine, ref)
        le = abs(_scalar(loss) - float(tl)) / max(1e-8, abs(float(tl)))
        return e <= TOL and le <= TOL, f"grad_rel={e:.2e} loss_rel={le:.2e}"

    def torch_layernorm():
        N, D = 5, 4
        x_np = np.random.randn(N, D).astype(np.float64)
        g_np = np.random.randn(D).astype(np.float64)
        b_np = np.random.randn(D).astype(np.float64)
        x = ag.Tensor(x_np.copy()); g = ag.Tensor(g_np.copy()); b = ag.Tensor(b_np.copy())
        R = _const(ag, (N, D))
        loss = (ag.layernorm(x, g, b) * R).sum()
        loss.backward()
        t = torch.tensor(x_np, requires_grad=True, dtype=torch.float64)
        tg = torch.tensor(g_np, requires_grad=True, dtype=torch.float64)
        tb = torch.tensor(b_np, requires_grad=True, dtype=torch.float64)
        tR = torch.tensor(R.data, dtype=torch.float64)
        tl = (torch.nn.functional.layer_norm(t, (D,), weight=tg, bias=tb, eps=1e-5) * tR).sum()
        tl.backward()
        e = max(max_rel_err(_grad_of(x), t.grad.numpy())[0],
                max_rel_err(_grad_of(g), tg.grad.numpy())[0],
                max_rel_err(_grad_of(b), tb.grad.numpy())[0])
        return e <= TOL, f"max_rel_err={e:.2e}"

    rep.check(P, "vs torch cross_entropy", torch_cross_entropy)
    rep.check(P, "vs torch layernorm", torch_layernorm)


# --------------------------------- main ------------------------------------
def main():
    # ---- import shim: edit these names/paths if yours differ ----
    # Locate src/autograd/ relative to this file so the harness runs from the
    # repo root regardless of how you package things. (Swap for an editable
    # install / conftest / PYTHONPATH if you prefer — your packaging call.)
    import os, sys
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(_root, "src", "autograd"))
    try:
        import autograd as ag
    except Exception as e:
        print(f"Could not import your `autograd` module: {e}")
        print("Create src/autograd/autograd.py (see the spec at "
              ".curriculum/phase_specs/autograd.md).")
        raise SystemExit(2)

    rep = Report()
    np.random.seed(SEED)
    run_part1(ag, rep)
    np.random.seed(SEED + 1)
    run_part2(ag, rep)
    np.random.seed(SEED + 2)
    run_part3(ag, rep)
    np.random.seed(SEED + 3)
    run_part4(ag, rep)
    ok = rep.print()
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
