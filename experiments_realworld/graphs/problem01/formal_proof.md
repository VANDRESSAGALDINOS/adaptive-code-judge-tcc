# Equivalence Proof — problem01: Shortest Routes II (CSES 1672)

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
All-pairs shortest paths by Floyd-Warshall on an undirected weighted graph:
initialize a distance matrix, relax through every intermediate vertex `k`, then
answer each query `(a, b)` by table lookup (`-1` if unreachable). Complexity
`O(n^3)` time, `O(n^2)` space.

## 1. Structural equivalence (line-by-line static analysis)
| Element | C++ | Python |
|---|---|---|
| distance matrix | `vector<vector<long long>> dist(n+1, ...(n+1, LLONG_MAX))` | `dist = [[float('inf')]*(n+1) for _ in range(n+1)]` |
| diagonal init | `for i: dist[i][i] = 0` | `for i in 1..n: dist[i][i] = 0` |
| edge read (undirected) | `dist[a][b]=min(dist[a][b],c); dist[b][a]=min(...)` | same two `min` updates |
| FW triple loop | `for k: for i: for j:` (1..n each) | `for k: for i: for j:` (1..n each) |
| relaxation | `if dist[i][k],dist[k][j] finite: dist[i][j]=min(dist[i][j],dist[i][k]+dist[k][j])` | identical |
| query / output | `-1` if `LLONG_MAX` else `dist[a][b]`, one per line | `-1` if `inf` else `dist[a][b]`, one per line |

Same strategy, corresponding data structures (`vector` <-> `list`), same iteration
order and bounds.

## 2. Semantic equivalence (invariant + complexity)
- Floyd-Warshall invariant: after the iteration for intermediate vertex `k`,
  `dist[i][j]` holds the shortest `i->j` distance using only `{1..k}` as
  intermediates. Base case `k=0`: direct edges / infinity. Inductive step: either
  the shortest path avoids `k` (value unchanged) or uses it
  (`dist[i][k]+dist[k][j]`); both implementations take the same `min`. Maintained
  identically by both.
- The finiteness guard before adding avoids overflow on `LLONG_MAX` / `inf`
  identically.
- Complexity (derivation, identical for both): initialization `O(n^2 + m)`; the
  triple loop performs exactly `n^3` relaxations (`O(n^3)`); queries `O(q)`. Same
  loop structure (identical bounds and body) -> identical asymptotic complexity AND
  identical operation count; only the per-operation cost differs (interpreter vs
  native code). This is the semantic basis for attributing the runtime gap to the
  language, not the algorithm.
- Both are iterative (no recursion) -> no Python stack-limit divergence.

## 3. Behavioral equivalence (bit-for-bit output)
Verification procedure: parallel execution of both versions on ALL CSES test cases,
exact-match comparison against the expected output.
- External (CSES): C++ ACCEPTED 16/16; Python ACCEPTED on the cases it completes
  ({1-5, 13, 16}) and TIME LIMIT EXCEEDED on {6,7,8,9,10,11,12,14,15}. On every case
  where both terminate, both produce the accepted (correct) output, so their outputs
  agree there. The Python-TLE cases produce no CSES Python output; they are covered
  by the local check below.
- Local (bench): `results/verdict.json` (exact-match validator). WRONG_ANSWER count
  = 0 across all 16 cases -> on every case both C++ and Python produce the same
  correct output, including the large cases the CSES Python run could not reach.

## 4. Documented deviations (language constraints)
- Sentinel for "no path": C++ `LLONG_MAX`, Python `float('inf')` — semantically
  equivalent (the finiteness guard and the output check treat them identically).
  No recursion, no other language-specific construct. Naming/sentinel only — same
  logic, same output.

## Conclusion
Under the three dimensions the implementations are equivalent. The observed runtime
difference (calibration factor reported in `results/calibration.json` and
`results/realworld_summary.json`) reflects the language execution model
(interpreted vs compiled), not the algorithm.
