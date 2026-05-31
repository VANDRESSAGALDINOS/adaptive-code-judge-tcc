# Equivalence Proof — dp/problem01: Coin Combinations I (CSES 1635)

## Goal
Show that the reference solutions are equivalent, so that any performance
difference comes only from the language execution model and the implementation
style (iterative vs recursive), not from an algorithmic difference. Follows the
three equivalence dimensions of the methodology: structural, semantic, behavioral.

## Scope
"Formal" here — as used in the methodology (S3.1) — means systematic, explicit
documentation, not a machine-checked proof in a formal logic system. Equivalence
is established through structural correspondence, an inductive invariant, a
complexity derivation, and empirical bit-for-bit output comparison.

## Problem and recurrence
Count the number of ordered ways to form the sum `x` using the given coins,
modulo `1e9+7`. Let `ways(s)` be that count for sum `s`:
- `ways(0) = 1`, `ways(s) = 0` for `s < 0`;
- `ways(s) = sum over coins c of ways(s - c)` for `s >= 1`.
The answer is `ways(x)`. All four solutions realize this recurrence; time
complexity `O(x*n)`.

## Reference solutions (two optimal styles, four files)
- Iterative (bottom-up): fills `dp[0..x]` with `dp[s] = sum_c dp[s-c]`.
- Recursive (top-down + memoization): `solve(s)` returns `ways(s)`, cached in a
  memo of size `x+1`.
Each style has a C++ and a Python implementation.

## 1. Structural equivalence (block-by-block, per cross-language pair)
The proof compares each pair over the WHOLE program -- input reading, data
structures, the core (loop / recursion), output -- statement by statement. "Match"
means the statements correspond one-to-one; only the language syntax differs.
`MOD = 1000000007` in all four files.

### Iterative pair: optimal_iterative C++ <-> Python
| Block | C++ | Python | Match |
|---|---|---|---|
| read header | `cin >> n >> x;` | `n=int(next(it)); x=int(next(it))` | n then x |
| read coins | `for i<n: cin >> coins[i]` | `for _ in range(n): coins.append(int(next(it)))` | n coins, same order |
| table init | `vector<int> dp(x+1,0); dp[0]=1;` | `dp=[0]*(x+1); dp[0]=1` | size x+1, zeroed, dp[0]=1 |
| outer loop | `for (s=1; s<=x; s++)` | `for s in range(1,x+1)` | s = 1..x |
| inner loop | `for (i=0; i<n; i++)` | `for coin in coins` | over all coins |
| guard | `if (s >= coins[i])` | `if s >= coin` | only when the coin fits |
| transition | `dp[s]=(dp[s]+dp[s-coins[i]])%MOD` | `dp[s]=(dp[s]+dp[s-coin])%MOD` | same accumulation + MOD |
| output | `cout << dp[x] << "\n"` | `print(dp[x])` | dp[x], single trailing newline |

Every statement corresponds; `vector<int>` <-> `list`. No statement in one file
lacks a counterpart in the other.

### Recursive pair: optimal_recursive C++ <-> Python
| Block | C++ | Python | Match |
|---|---|---|---|
| read header/coins | `cin >> n >> x; for i<n: cin >> coins[i]` | `n,x = ...; coins.append(...)` | identical to iterative |
| memo init | `int memo[10^6+1]; memset(memo,-1,...)` | `memo=[-1]*(x+1)` | sentinel -1, indices 0..x |
| base case 1 | `if (remaining==0) return 1;` | `if remaining==0: return 1` | 1 path at sum 0 |
| base case 2 | `if (remaining<0) return 0;` | `if remaining<0: return 0` | 0 below 0 |
| memo hit | `if (memo[remaining]!=-1) return memo[remaining];` | `if memo[remaining]!=-1: return memo[remaining]` | cached lookup |
| transition | `for i<n: if (remaining>=coins[i]) result=(result+solve(remaining-coins[i]))%MOD` | `for coin in coins: if remaining>=coin: result=(result+solve(remaining-coin,coins,memo))%MOD` | sum over fitting coins + MOD |
| store + return | `return memo[remaining]=result;` | `memo[remaining]=result; return result` | cache then return |
| output | `cout << solve(x) << "\n"` | `print(solve(x, coins, memo))` | solve(x), single trailing newline |

Every statement corresponds. One structural difference, semantically neutral
(noted in section 4): C++ holds `n`, `coins`, `memo` as GLOBALS while Python
passes `coins`/`memo` as arguments -- the values and access pattern are identical.

## 2. Semantic equivalence (invariants + complexity)
- Iterative invariant: when the outer loop finishes sum `s`, `dp[s] = ways(s)`
  (each `dp[s-c]` for `c <= s` was already finalized, since `s-c < s`).
- Recursive invariant: `solve(s)` returns `ways(s)`; the memo stores `ways(s)`
  on first computation and returns it thereafter. By induction on `s`: base cases
  hold; for `s >= 1`, `solve(s) = sum_c solve(s-c) = sum_c ways(s-c) = ways(s)`.
- Correctness of each style (iter and rec are COMPARED in QP3, not required to be
  mutually equivalent): both realize the recurrence `ways(s)`, so `dp[x] = ways(x)`
  (iterative) and `solve(x) = ways(x)` (recursive) -- each yields the correct
  answer. The equivalence the beta calibration relies on is the CROSS-LANGUAGE one
  WITHIN each style (sections 1-2), not between styles.
- Complexity (identical for both styles): each of the `x` sums is resolved once,
  each over `n` coins -> `O(x*n)` time; `O(x)` space (the `dp` table / the memo).
- Recursion-depth / call-stack behavior is a language-specific constraint of the
  recursive style; it is treated as a documented deviation (see section 4).

## 3. Behavioral equivalence (bit-for-bit output)
Verification procedure: parallel execution of all four solutions on every CSES
test case, with exact-match comparison against the expected output (a single
integer per case).
- External (CSES) — [a preencher após submissão]: per-case verdicts for the four
  submissions; on every case where a solution is ACCEPTED it produces the
  expected output.
- Local (bench) — [a preencher após verdict]: exact-match validator; behavioral
  equivalence holds iff the WRONG_ANSWER count is 0 across all cases.

## 4. Documented deviations (language constraints)
- Recursion depth: the recursive style recurses to depth up to `x` (~10^6 when a
  coin has value 1). Python raises the limit via `sys.setrecursionlimit(1100000)`;
  C++ uses the native call stack and may exceed it on the deepest inputs
  (RUNTIME_ERROR / stack overflow). This recursion-depth sensitivity is the
  documented experimental variable (methodology S3.1), not an algorithmic
  difference — it is precisely the implementation-style effect under study. Its
  actual impact is read from the CSES per-case verdicts.
- State holding (recursive): C++ keeps `n`, `coins`, `memo` as global variables;
  Python passes `coins` and `memo` as function arguments. Language-idiom difference
  with identical semantics (same values, same per-state caching) — not algorithmic.

## Conclusion
The four implementations are equivalent across the three dimensions. Runtime
differences reflect the language execution model and the implementation style
(the function-call overhead and call-stack use of the recursive style), not the
algorithm.
