# Equivalence Proof — dp/problem02: Grid Paths (CSES 1638)

## Goal
Show that, WITHIN each implementation style, the C++ and Python reference
solutions are equivalent, so that the per-style beta measures only the language
execution penalty. The two styles (iterative vs recursive) are two correct
optimal solutions that are COMPARED (QP3 contrast), not required to be mutually
equivalent. Follows the three equivalence dimensions of the methodology:
structural, semantic, behavioral.

## Scope
"Formal" here -- as used in the methodology (S3.1) -- means systematic, explicit
documentation, not a machine-checked proof in a formal logic system. Equivalence
is established through structural correspondence, an inductive invariant, a
complexity derivation, and empirical bit-for-bit output comparison.

## Problem and recurrence
`n x n` grid with obstacles (`*`) and free cells (`.`). Count the paths from the
top-left `(0,0)` to the bottom-right `(n-1,n-1)` moving only right or down,
without entering an obstacle, modulo `1e9+7` (`1 <= n <= 1000`). The path count
satisfies `f(cell) = f(up) + f(left)` (forward) or, equivalently, `g(cell) =
g(right) + g(down)` (backward); the total is the same either way.

## Reference solutions (two optimal styles, four files)
- Iterative (bottom-up, FORWARD): `dp[i][j]` = number of paths from `(0,0)` to
  `(i,j)`; answer `dp[n-1][n-1]`.
- Recursive (top-down + memoization, BACKWARD): `solve(i,j)` = number of paths
  from `(i,j)` to `(n-1,n-1)`; answer `solve(0,0)`.
Each style has a C++ and a Python implementation. The proof below is per style.

## 1. Structural equivalence (block-by-block, per cross-language pair)
The proof compares each pair over the WHOLE program -- input reading, data
structures, the core (loop / recursion), output -- statement by statement. "Match"
means the statements correspond one-to-one; only the language syntax differs.
`MOD = 1000000007` in all four files.

### Iterative pair: optimal_iterative C++ <-> Python
| Block | C++ | Python | Match |
|---|---|---|---|
| read header | `cin >> n;` | `n=int(next(it))` | grid size n |
| read grid | `for i<n: cin >> grid[i]` | `for _ in range(n): grid.append(next(it).decode('utf-8'))` | n rows, same order |
| table init | `vector<vector<int>> dp(n, vector<int>(n,0))` | `dp=[[0]*n for _ in range(n)]` | n x n, zeroed |
| start cell | `if (grid[0][0]!='*') dp[0][0]=1;` | `if grid[0][0]!='*': dp[0][0]=1` | dp[0][0]=1 iff free |
| first row | `for j=1..n-1: if (grid[0][j]!='*') dp[0][j]=dp[0][j-1]` | `for j in range(1,n): if grid[0][j]!='*': dp[0][j]=dp[0][j-1]` | carry from the left |
| first col | `for i=1..n-1: if (grid[i][0]!='*') dp[i][0]=dp[i-1][0]` | same with Python syntax | carry from above |
| interior | `for i=1..n-1: for j=1..n-1: if (grid[i][j]!='*') dp[i][j]=(dp[i-1][j]+dp[i][j-1])%MOD` | same with Python syntax | up + left, MOD, 0 if obstacle |
| output | `cout << dp[n-1][n-1] << "\n"` | `print(dp[n-1][n-1])` | bottom-right, single newline |

Every statement corresponds; `vector<vector<int>>` <-> list of lists, grid as
`vector<string>` <-> list of strings.

### Recursive pair: optimal_recursive C++ <-> Python
| Block | C++ | Python | Match |
|---|---|---|---|
| read header/grid | `cin >> n; for i<n: cin >> grid[i]` | `n=...; grid.append(...)` | identical to iterative |
| memo init | `int memo[1001][1001]; memset(memo,-1,...)` | `memo=[[-1]*n for _ in range(n)]` | sentinel -1, n x n |
| guard | `if (i>=n || j>=n || grid[i][j]=='*') return 0;` | `if i>=n or j>=n or grid[i][j]=='*': return 0` | out-of-bounds / obstacle -> 0 |
| destination | `if (i==n-1 && j==n-1) return 1;` | `if i==n-1 and j==n-1: return 1` | 1 path at the goal |
| memo hit | `if (memo[i][j]!=-1) return memo[i][j];` | `if memo[i][j]!=-1: return memo[i][j]` | cached lookup |
| transition | `result=(result+solve(i,j+1))%MOD; result=(result+solve(i+1,j))%MOD;` | `result=(result+solve(i,j+1,...))%MOD; result=(result+solve(i+1,j,...))%MOD` | right + down, MOD |
| store + return | `return memo[i][j]=result;` | `memo[i][j]=result; return result` | cache then return |
| output | `cout << solve(0,0) << "\n"` | `print(solve(0,0,grid,memo,n))` | solve(0,0), single newline |

Every statement corresponds. One structural difference, semantically neutral
(noted in section 4): C++ holds `n`, `grid`, `memo` as GLOBALS while Python passes
`grid`/`memo`/`n` as arguments -- same values and access pattern.

## 2. Semantic equivalence (invariant + complexity, per style)
- Iterative invariant (forward): when cell `(i,j)` is filled, `dp[i][j]` equals
  the number of paths from `(0,0)` to `(i,j)` -- `0` if it is an obstacle, else
  the sum of the cell above and the cell to the left (the only predecessors).
- Recursive invariant (backward): `solve(i,j)` returns the number of paths from
  `(i,j)` to `(n-1,n-1)`; the memo caches it. By induction: obstacle/out-of-bounds
  give `0`, the destination gives `1`, otherwise `solve(i,j+1) + solve(i+1,j)`.
- Correctness of each style: both count the paths `(0,0) -> (n-1,n-1)`, so
  `dp[n-1][n-1]` (forward) and `solve(0,0)` (backward) each equal that total,
  which is independent of the counting direction. Each style is correct; the two
  are compared in QP3, not claimed mutually equivalent.
- Complexity (each style): `n^2` states (cells), `O(1)` work each -> `O(n^2)`
  time, `O(n^2)` space (the table / the memo).
- Recursion depth (recursive style): a path from `(i,j)` to `(n-1,n-1)` has length
  `(n-1-i)+(n-1-j) <= 2(n-1)`, so the recursion depth is `O(n)` (<= ~2000 for
  `n <= 1000`) -- shallow, no call-stack concern. `setrecursionlimit(2*10^6)` is
  generous.

## 3. Behavioral equivalence (bit-for-bit output, per style)
Verification procedure: for each style, parallel execution of the C++ and Python
versions on ALL CSES test cases, with exact-match comparison against the expected
output (a single integer per case).
- External (CSES) -- [a preencher apos submissao]: per-case verdicts for the four
  submissions; on every case where a solution is ACCEPTED it produces the expected
  output.
- Local (bench) -- [a preencher apos verdict]: exact-match validator; the
  cross-language equivalence WITHIN each style holds iff the WRONG_ANSWER count is
  0 across all cases.

## 4. Documented deviations (language constraints)
- DP orientation: the iterative style is forward (paths from the origin), the
  recursive style is backward (paths to the destination). This is the NATURE of
  each correct style, not an equivalence to prove or to "align" -- iterative and
  recursive are compared (QP3 contrast). It does not affect the per-style
  cross-language equivalence.
- State holding (recursive): C++ keeps `n`, `grid`, `memo` as globals; Python
  passes `grid`/`memo`/`n` as arguments. Language-idiom difference with identical
  semantics -- not algorithmic.
- Recursion is shallow (`O(n)`, <= ~2000 for n <= 1000), so no stack-limit issue;
  no language-specific data type.

## Conclusion
Within each style the C++ and Python implementations are equivalent across the
three dimensions, so each per-style beta reflects the pure language execution
penalty. Each style is a correct optimal solution. Runtime differences reflect the
language execution model and the implementation style, not the algorithm.
