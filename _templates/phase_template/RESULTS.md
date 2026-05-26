# RESULTS — Tier _ · Phase _._

**Date:** <when>  ·  **Hardware:** <CPU/GPU>  ·  **Env:** <python/torch/numpy versions>

## Harness output
```
<paste the PASS/FAIL/SKIP table here>
```
- Tolerance: <bound>  ·  Max rel error observed: <number>
- torch oracle: <ran / not available>

## The key result of this phase
<one paragraph: the load-bearing thing you built and what the harness proved
about it. e.g. for 0.1: the engine produces gradients matching central
finite differences and PyTorch to numerical tolerance across linear,
softmax-CE, and layernorm — including the (p − y)/N identity for the fused
softmax-CE row, confirmed to ~1e-16 against the independent oracle.>

## Traps that bit me
- <trap>: <how it manifested, how I found it, the fix>

## Reproduce
```
<the exact commands a stranger runs to rerun this>
```

## Links
- Implementation: <repo/commit>
- Harness: <repo/commit>  (validated per HARNESS_VALIDATION_PROTOCOL.md)
