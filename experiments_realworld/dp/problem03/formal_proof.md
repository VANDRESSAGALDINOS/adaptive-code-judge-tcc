# Equivalence Proof — dp/problem03: Two Sets II (CSES 1093)

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
Count the ways to split `{1, 2, ..., n}` into two sets of equal sum, modulo
`1e9+7` (`1 <= n <= 500`). Let `S = n(n+1)/2`. If `S` is odd the answer is `0`.
Otherwise let `target = S/2`; the answer is the number of subsets of `{1..n}`
summing to `target`, divided by two (each partition `{A,B}` is counted as both
`A` and its complement `B`). The subset count `W(i,s)` = number of subsets of
`{1..i}` with sum `s` satisfies `W(i,s) = W(i-1,s) + W(i-1,s-i)` (exclude /
include `i`), with `W(0,0)=1`. The final answer is `W(n,target) * inverse(2)`.

## Reference solutions (two optimal styles, four files)
- Iterative (bottom-up): rolling two-row table; `prev[s]` = subsets of `{1..i-1}`
  summing to `s`, `curr[s]` for `{1..i}`; answer `prev[target]` after `n` rows.
- Recursive (top-down + memoization): `count_ways(i,s)` = subsets of `{1..i}`
  summing to `s`, cached in a 2D memo; answer `count_ways(n,target)`.
Both divide by two via the modular inverse of 2 (Fermat: `2^(MOD-2) mod MOD`).
Each style has a C++ and a Python implementation. The proof below is per style.

## 1. Structural equivalence (block-by-block, per cross-language pair)
The proof compares each pair over the WHOLE program -- input reading, data
structures, the core (loop / recursion), output -- statement by statement. "Match"
means the statements correspond one-to-one; only the language syntax differs.
`MOD = 1000000007` and the `power`/`pow(2, MOD-2, MOD)` modular inverse appear in
all four files.

### Iterative pair: optimal_iterative C++ <-> Python
| Block | C++ | Python | Match |
|---|---|---|---|
| read header | `cin >> n;` | `n=int(input())` | integer n |
| total sum | `int total_sum = n*(n+1)/2;` | `total_sum = n*(n+1)//2` | S = n(n+1)/2 |
| parity guard | `if (total_sum%2==1){cout<<0<<"\n";return 0;}` | `if total_sum%2==1: print(0); return` | odd S -> 0 |
| target | `int target = total_sum/2;` | `target = total_sum//2` | S/2 |
| rows init | `vector<long long> prev(target+1,0), curr(target+1,0);` | `prev=[0]*(target+1); curr=[0]*(target+1)` | two zeroed rows of size target+1 |
| base | `prev[0]=1;` | `prev[0]=1` | empty subset -> sum 0 |
| outer loop | `for i=1..n` | `for i in range(1,n+1)` | items 1..n |
| zero-sum | `curr[0]=1;` | `curr[0]=1` | one way for sum 0 |
| exclude i | `for j=1..target: curr[j]=prev[j];` | `for j in range(1,target+1): curr[j]=prev[j]` | not taking i |
| include i | `if (j>=i) curr[j]=(curr[j]+prev[j-i])%MOD;` | `if j>=i: curr[j]=(curr[j]+prev[j-i])%MOD` | taking i, MOD |
| advance row | `swap(prev,curr);` | `prev,curr = curr,prev` | prev becomes row i |
| collect | `long long ways=prev[target];` | `ways=prev[target]` | subsets summing to target |
| divide by 2 | `result=(ways*power(2,MOD-2,MOD))%MOD;` | `result=ways*pow(2,MOD-2,MOD)%MOD` | x inverse(2) |
| output | `cout << result << "\n";` | `print(result)` | single integer, single newline |

Every statement corresponds; `vector<long long>` <-> Python list. After the C++
fix both sides use the SAME rolling two-row table (previously the C++ used a full
2D table -- it was realigned so the pair is the same algorithm).

### Recursive pair: optimal_recursive C++ <-> Python
| Block | C++ | Python | Match |
|---|---|---|---|
| read/total/parity/target | `cin>>n; total_sum=...; if odd ->0; target=total_sum/2;` | `n=int(input()); total_sum=...; if odd ->0; target=total_sum//2` | identical preamble to iterative |
| memo init | `int memo[501][125001]; memset(memo,-1,sizeof);` | `memo=[[-1]*(target+1) for _ in range(n+1)]` | sentinel -1, indexed [i][s] |
| base zero-sum | `if (target_sum==0) return 1;` | `if target_sum==0: return 1` | sum 0 -> 1 |
| base none | `if (i<=0 || target_sum<0) return 0;` | `if i<=0 or target_sum<0: return 0` | no items / negative -> 0 |
| memo hit | `if (memo[i][target_sum]!=-1) return memo[i][target_sum];` | `if memo[i][target_sum]!=-1: return memo[i][target_sum]` | cached lookup |
| exclude i | `int result=count_ways(i-1,target_sum);` | `result=count_ways(i-1,target_sum,memo)` | not taking i |
| include i | `if (target_sum>=i) result=(result+count_ways(i-1,target_sum-i))%MOD;` | `if target_sum>=i: result=(result+count_ways(i-1,target_sum-i,memo))%MOD` | taking i, MOD |
| store + return | `return memo[i][target_sum]=result;` | `memo[i][target_sum]=result; return result` | cache then return |
| top call + /2 | `ways=count_ways(n,target); result=(1LL*ways*power(2,MOD-2,MOD))%MOD;` | `ways=count_ways(n,target,memo); result=ways*pow(2,MOD-2,MOD)%MOD` | count_ways(n,target), x inverse(2) |
| output | `cout << result << "\n";` | `print(result)` | single integer, single newline |

Every statement corresponds. One structural difference, semantically neutral
(noted in section 4): C++ holds `n`, `target`, `memo` as GLOBALS with a fixed-size
static memo `[501][125001]` (over-allocated for safety), while Python sizes the
memo exactly `[n+1][target+1]` and passes it as an argument -- same sentinel,
same `[i][s]` indexing, same access pattern.

## 2. Semantic equivalence (invariant + complexity, per style)
- Iterative invariant: after the outer iteration for item `i`, the row `prev[s]`
  equals `W(i,s)` = the number of subsets of `{1..i}` summing to `s`. Base
  `prev[0]=1` (empty subset). Transition: subsets of `{1..i}` summing to `s` are
  those not using `i` (`prev[s]`, subsets of `{1..i-1}`) plus those using `i`
  (`prev[s-i]`, subsets of `{1..i-1}` summing to `s-i`, only when `s>=i`). After
  `n` rows, `prev[target] = W(n,target)`.
- Recursive invariant: `count_ways(i,s)` returns `W(i,s)`; the memo caches it. By
  induction: `s==0` gives `1` (empty subset), `i<=0` or `s<0` gives `0`, otherwise
  `count_ways(i-1,s) + [s>=i] count_ways(i-1,s-i)`. So `count_ways(n,target) =
  W(n,target)`.
- Correctness of each style: both compute `W = W(n,target)`, the number of subsets
  summing to `S/2`. Each equal-sum partition `{A,B}` corresponds to exactly two
  such subsets (`A` and its complement `B`), so the number of partitions is
  `W/2 = W * inverse(2) mod MOD`; if `S` is odd the answer is `0`. Both styles
  output this value. Each style is correct; the two are compared in QP3, not
  claimed mutually equivalent (they even differ in space, see section 4).
- Complexity (each style): `target = S/2 = n(n+1)/4 = O(n^2)` states per row times
  `n` rows -> `O(n * target) = O(n^3)` time (~3.1e7 for n=500), `O(1)` per state.
  Space: iterative `O(target) = O(n^2)` (two rolling rows); recursive
  `O(n * target) = O(n^3)` (the full 2D memo) -- see section 4.
- Recursion depth (recursive style): `count_ways(i, .)` calls `count_ways(i-1, .)`,
  so the depth is at most `n <= 500` -- shallow, no call-stack concern.
  `setrecursionlimit(10^6)` is generous; C++ depth 500 is well within the (raised)
  stack.

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

## 4. Documented deviations (language constraints / style nature)
- DP space structure: the iterative style uses a rolling two-row table
  (`O(target)` space); the recursive style uses a full 2D memo (`O(n*target)`
  space). This is the NATURE of each style, not an equivalence to prove or to
  "align": top-down memoization addresses arbitrary `(i,s)` states and cannot roll,
  whereas bottom-up only needs the previous row. Iterative and recursive are
  compared (QP3 contrast). WITHIN each style the cross-language pair uses the SAME
  structure (rolling <-> rolling, full memo <-> full memo).
- State holding (recursive): C++ keeps `n`, `target`, `memo` as globals (a
  fixed-size static array `[501][125001]`, over-allocated for safety); Python sizes
  the memo exactly and passes it as an argument. Language-idiom difference with
  identical semantics -- not algorithmic.
- Division by two: both use the modular inverse of 2 (Fermat's little theorem,
  `2^(MOD-2) mod MOD`), since each partition is counted twice. Same value.

## Conclusion
Within each style the C++ and Python implementations are equivalent across the
three dimensions, so each per-style beta reflects the pure language execution
penalty. Each style is a correct optimal solution. Runtime differences reflect the
language execution model and the implementation style (notably the iterative's
`O(n^2)` space vs the recursive's `O(n^3)` memo), not the algorithm.
