# RESULTS — Tier _ · Phase _._

**Date:** <when>  ·  **Hardware:** <CPU/GPU>  ·  **Env:** <python/torch/numpy versions>

## Harness output
```
<paste the PASS/FAIL/SKIP table here>
```
- Tolerance: <bound>  ·  Max rel error observed: <number>
- torch oracle: <ran / not available>

## The key result of this phase
<one paragraph: the load-bearing insight you proved. e.g. for 0.1: why softmax-CE
collapses to (p - y)/N, and that the harness confirmed it to ~1e-16.>

## Traps that bit me
- <trap>: <how it manifested, how I found it, the fix>

## Reproduce
```
<the exact commands a stranger runs to rerun this>
```

## Links
- Implementation: <repo/commit>
- Harness: <repo/commit>  (validated per HARNESS_VALIDATION_PROTOCOL.md)
