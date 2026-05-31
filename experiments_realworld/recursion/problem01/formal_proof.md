# Equivalence Proof — Tree Distances II (CSES 1133)

Scope note: "formal" here means systematic and explicit, NOT a machine-checked
proof in a formal-methods system. This document establishes the cross-language
equivalence (C++ <-> Python) of the optimal solution, mapping the two programs
statement by statement, plus a semantic argument and the behavioral evidence.

## 0. Objective, algorithm, complexity

- Problem: for each node of a tree (n nodes), output the sum of distances from
  that node to all other nodes.
- Algorithm (single optimal style): recursive DFS rerooting, two passes:
  - `dfs1` (post-order, rooted at 1): compute subtree sizes `cnt[u]` and the sum
    of depths from the root, accumulated into `res[1]`;
  - `dfs2` (pre-order): move the root from `u` to a child `v`; the `cnt[v]` nodes
    in v's subtree get one step closer (each -1) and the other `n - cnt[v]` nodes
    get one step farther (each +1), so `res[v] = res[u] + (n - cnt[v]) - cnt[v]`.
- Complexity: O(n) time, O(n) space + O(depth) recursion stack; depth up to n
  (chain) -> deep recursion (the category fenomenon).
- ONE optimal style: recursion is the natural form of a tree DFS; a single beta
  is calibrated.

## 1. Structural equivalence (C++ <-> Python), block by block

| Block | C++ (`implementations/optimal/solution.cpp`) | Python (`implementations/optimal/solution.py`) | Correspondence |
|-------|----------------------------------------------|------------------------------------------------|----------------|
| Read input | `cin>>n; loop n-1: cin>>a>>b; adj[a].push_back(b); adj[b].push_back(a);` | `data=read().split(); n=...; loop: adj[a].append(b); adj[b].append(a)` | Both build the same undirected adjacency list from n and the n-1 edges. |
| State | `vector<long long> cnt(n+1), res(n+1);` | `cnt=[1]*(n+1); res=[0]*(n+1)` | Same per-node arrays. (C++ sets cnt[u]=1 inside dfs1; Python pre-fills 1 — same effect, see deviation #1.) |
| n==1 guard | `if(n==1){cout<<0;return;}` | `if n==1: print(0); return` | Same edge case. |
| dfs1 body | `res[1]+=depth; cnt[u]=1; for v in adj[u]: if v!=parent: dfs1(v,u,depth+1); cnt[u]+=cnt[v];` | `res[1]+=depth; for v: if v!=parent: dfs1(v,u,depth+1); cnt[u]+=cnt[v]` | Same post-order: accumulate depth into res[1], recurse, sum child subtree sizes. |
| dfs2 body | `for v in adj[u]: if v!=parent: res[v]=res[u]+(n-cnt[v])-cnt[v]; dfs2(v,u);` | identical | Same reroot recurrence, same pre-order recursion. |
| Output | `for i=1..n: cout<<res[i] (space-separated) <<"\n";` | `" ".join(str(res[i]))` | Same n integers on one line. |

## 2. Semantic equivalence

- Invariant dfs1: after `dfs1(1,0,0)`, `cnt[u]` = size of u's subtree (rooted at
  1) and `res[1]` = sum over all nodes of their depth = sum of distances from the
  root to every node. Proof: post-order sums `1 + sum(cnt[children])` and each
  node contributes its depth once.
- Invariant dfs2: `res[u]` is the correct answer for u; moving to child v changes
  every distance by +-1 as argued in block 0, so `res[v] = res[u] + (n-cnt[v]) -
  cnt[v]` is exact. By induction from the root, all `res[*]` are correct. Both
  languages apply the identical recurrence in the same pre-order, so they produce
  identical arrays.
- Complexity (derived, identical): each node visited O(1) times per pass, two
  passes -> O(n) both; recursion depth = tree depth (up to n).
- Recursion/stack: Python sets `setrecursionlimit(300000)`; C++ uses the default
  stack. The depth (up to n) is the language-stressing variable documented in the
  article (S3.1). On the official CSES data no stack overflow occurred (no deep
  chain case); the observed injustice is by time.

## 3. Behavioral equivalence (bit-exact output)

- External: CSES submissions (PASSO A): C++ AC 15/15; Python TLE {6,7,8,14}, AC
  elsewhere — same answers where both run.
- Local: example (n=5) gives `6 9 5 8 8` in both. `results/verdict.json` with 0
  WRONG_ANSWER across the cases — to fill after the bench.

## 4. Documented deviations (language-driven, not algorithmic)

1. `cnt` initialization: C++ sets `cnt[u]=1` at the start of dfs1; Python
   pre-fills the whole array with 1. Same value when used; just where the 1 is
   written.
2. Integer width: C++ uses `long long` for `cnt`/`res` (the distance sum reaches
   ~4*10^10 for n=2*10^5); Python ints are unbounded — same arithmetic.
3. Input reading: C++ `cin>>`; Python bulk `sys.stdin.buffer.read().split()` —
   both parse the same integers.

## 5. Conclusion

The two optimal programs implement the same DFS-rerooting algorithm with a
statement-by-statement correspondence, the same invariants, the same O(n) cost,
and identical output. Any runtime difference reflects only the language execution
model (interpreted Python vs compiled C++) — which is what beta measures.
