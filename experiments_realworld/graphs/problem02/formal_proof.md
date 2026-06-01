# Equivalence Proof — problem02: Cycle Finding (CSES 1197)

## Goal
Show that the C++ and Python reference solutions are equivalent, so that any
performance difference comes ONLY from the language execution model, not from an
algorithmic difference. Follows the three equivalence dimensions of the
methodology: structural, semantic, behavioral.

## Scope
"Formal" here — as used in the methodology (S3.1) — means systematic, explicit
documentation, not a machine-checked proof in a formal logic system. Equivalence
is established through structural correspondence, an inductive invariant, a
complexity derivation, and empirical bit-for-bit output comparison.

## Algorithm
Negative-cycle detection by Bellman-Ford with an implicit super-source
(`dist[i]=0` for all i). Relax every edge for `n` iterations, tracking the last
relaxed vertex `x`; if some edge still relaxes on the n-th pass a negative cycle
exists. Walk `n` parent steps from `x` to land inside the cycle, then follow
parents to reconstruct it. Output `NO`, or `YES` and the closed cycle. Complexity
`O(n*m)` time, `O(n+m)` space.

## 1. Structural equivalence (line-by-line static analysis)
| Element | C++ | Python |
|---|---|---|
| state | `dist(n+1,0)`, `parent(n+1,-1)`, `x=-1` | `dist=[0]*(n+1)`, `parent=[-1]*(n+1)`, `x=-1` |
| relax loop | `for i in 0..n-1: x=-1; for e in edges:` | `for _ in range(n): x=-1; for a,b,w in edges:` |
| relax test | `if dist[a]+c < dist[b]: dist[b]=...; parent[b]=a; x=b` | identical |
| no-cycle | `if x==-1: print "NO"` | `if x==-1: print("NO")` |
| enter cycle | `y=x; n times y=parent[y]` | `y=x; n times y=parent[y]` |
| reconstruct | follow `parent` until closure, then reverse | follow `parent` until closure, then reverse |
| output | `YES` + closed cycle | `YES` + closed cycle |

Same strategy, corresponding data structures (`vector` <-> `list`), same iteration
order and bounds.

## 2. Semantic equivalence (invariant + complexity)
- Bellman-Ford invariant: after `k` outer iterations, `dist[v]` is the minimum
  weight of a walk from the implicit super-source to `v` using at most `k` edges.
  Base case `k=0`: `dist[v]=0`. Inductive step: each pass relaxes every edge once
  (`dist[b] = min(dist[b], dist[a]+w)`), extending shortest walks by one edge; both
  implementations apply the same conditional update and parent assignment.
- After `n` passes, a still-relaxable edge (`x != -1`) certifies a negative cycle
  reachable from the super-source; walking `n` parents from `x` reaches a vertex
  guaranteed to lie on the cycle (standard argument). Both reconstruct by following
  `parent` until the start repeats, producing the same closed cycle.
- Complexity (derivation, identical for both): `n` passes over `m` edges -> `O(n*m)`
  relaxations; detection `O(1)`; reconstruction `O(n)`. Same loop structure
  (identical bounds and body) -> identical asymptotic complexity AND identical
  operation count; only the per-operation cost differs (interpreter vs native code).
  This is the semantic basis for attributing the runtime gap to the language, not
  the algorithm.
- Both are iterative (no recursion) -> no Python stack-limit divergence.

## 3. Behavioral equivalence (bit-for-bit output)
Verification procedure: parallel execution of both versions on ALL CSES test cases,
exact-match comparison against the expected output (any valid negative cycle is
accepted by the CSES checker; both reference solutions reconstruct the same cycle
via identical parent logic).
- External (CSES): C++ ACCEPTED 27/27; Python ACCEPTED on the cases it completes and
  TIME LIMIT EXCEEDED on {6,7,8,9,10,27}. On every case where both terminate, both
  produce an accepted (correct) output. The Python-TLE cases produce no CSES Python
  output; they are covered by the local check below.
- Local (bench): `results/verdict.json` (exact-match validator). WRONG_ANSWER count
  = 0 across all 27 cases -> on every case both C++ and Python produce the same
  correct output, including the large cases the CSES Python run could not reach.

## 4. Documented deviations (language constraints)
- Cycle-closure bookkeeping differs only in surface form (C++ breaks when the start
  vertex repeats with `size>1`; Python appends the closing vertex then breaks) —
  both emit the same closed cycle. No recursion, no language-specific type. Form
  only — same logic, same output.

## Conclusion
Under the three dimensions the implementations are equivalent. The observed runtime
difference (calibration factor reported in `results/calibration.json` and
`results/realworld_summary.json`) reflects the language execution model
(interpreted vs compiled), not the algorithm.
