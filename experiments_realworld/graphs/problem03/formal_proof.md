# Equivalence Proof — problem03: Planets Queries I (CSES 1750)

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
Binary lifting on a functional graph. Preprocess `up[i][j]` = vertex reached
after `2^j` steps from `i`; each query `(x, k)` decomposes `k` in binary and
applies the jumps. Complexity `O((n + q) · log k)`.

## 1. Structural equivalence (line-by-line static analysis)
| Element | C++ | Python |
|---|---|---|
| jump table | `vector<vector<int>> up(n+1, vector<int>(LOG))` | `up = [[0]*LOG for _ in range(n+1)]` |
| base case | `up[i][0] = next[i]` | `up[i][0] = next_planet[i]` |
| recurrence | `up[i][j] = up[up[i][j-1]][j-1]` | `up[i][j] = up[up[i][j-1]][j-1]` |
| fill order | `j: 1..LOG-1`, `i: 1..n` | `j: 1..LOG-1`, `i: 1..n` |
| query jump | `if (k & (1<<j)) x = up[x][j]` | `if k & (1<<j): x = up[x][j]` |
| output | one answer per line | one answer per line |

Same strategy, corresponding data structures (`vector` <-> `list`), same
iteration order.

## 2. Semantic equivalence (invariant + complexity)
- Binary-lifting invariant: after processing bits `0..j` of `k`, `x` is the
  vertex reached after `sum_{i<=j} b_i·2^i` steps. Holds by the base case
  (`up[i][0] = next[i]`, one step) and induction (`up[i][j] = up[up[i][j-1]][j-1]`
  composes two `2^(j-1)` jumps into `2^j`). Both implementations maintain it
  identically.
- `LOG = 30` covers `k <= 10^9` (`2^30 ≈ 1.07×10^9 > 10^9`); `k = 0` leaves `x`
  unchanged (no bit set).
- Complexity (derivation, identical for both implementations):
  - Preprocessing: the table `up` has `(n+1)·LOG` entries. `up[i][0]` is set in a
    single pass over `i` (`O(n)`); every remaining entry `up[i][j]` is computed in
    `O(1)` by one lookup `up[up[i][j-1]][j-1]`. Total `O(n·LOG)`.
  - Queries: each query scans the `LOG` bits of `k`; a set bit triggers one `O(1)`
    jump `x = up[x][j]`. Hence `O(LOG)` per query and `O(q·LOG)` for all `q`.
  - Since `LOG = ceil(log2(k_max))` (30 for `k <= 10^9`), `O(n·LOG) = O(n·log k)`
    and `O(q·LOG) = O(q·log k)`; total time `O((n + q)·log k)`.
  - Space: the jump table dominates, `O(n·LOG) = O(n·log k)`; everything else is
    `O(1)`.
  - Concrete bound (max constraints n = q = 2×10^5, LOG = 30): ~6×10^6 table
    assignments + ~6×10^6 bit tests/jumps ≈ 1.2×10^7 fundamental operations.
  - Both implementations have the SAME loop structure (identical bounds and body)
    -> identical asymptotic complexity AND identical operation count; only the
    per-operation cost differs (interpreter vs native code). This is the semantic
    basis for attributing the runtime gap to the language, not the algorithm.
- Both are iterative (no recursion) -> no Python stack-limit divergence.

## 3. Behavioral equivalence (bit-for-bit output)
Verification procedure: parallel execution of both versions on ALL CSES test
cases, with exact-match comparison against the expected output.
- External (CSES, 2026-05-30): C++ ACCEPTED 14/14; Python ACCEPTED on cases
  #1-5, #11, #13, #14 (TLE on #6-10, #12). On every case where both terminate
  (the 8 accepted cases) both produce the accepted (correct) output, so their
  outputs agree there. On the Python-TLE cases CSES yields no Python output;
  those are covered by the local check below, where Python completes under the
  adaptive limit.
- Local (bench, 2026-05-30): `verdict.json` (3 reps/case, exact-match validator).
  WRONG_ANSWER count = 0 across all 14 cases -> on every case both C++ and Python
  produce the same correct output. This confirms behavioral equivalence under
  parallel execution, including the large cases the CSES Python run could not
  reach (TLE).

## 4. Documented deviations (language constraints)
- Targets array name: C++ `next`, Python `next_planet` (avoids shadowing the
  Python builtin `next`, used by the input iterator). Naming only — same logic,
  same output. No other deviation (no recursion, no language-specific type).

## Conclusion
Under the three dimensions the implementations are equivalent. The observed
runtime difference reflects the language execution model (interpreted vs
compiled), not the algorithm.
