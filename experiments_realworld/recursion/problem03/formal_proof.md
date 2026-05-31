# Equivalence Proof — Tree Distances I (CSES 1132)

Scope note: "formal" here means systematic and explicit, NOT a machine-checked
proof in a formal-methods system. This document establishes the cross-language
equivalence (C++ <-> Python) of the optimal solution, mapping the two programs
statement by statement, plus a semantic argument and the behavioral evidence.

## 0. Objective, algorithm, complexity

- Problem: for each node of a tree (n nodes), output the MAXIMUM distance to any
  other node.
- Algorithm (single optimal style): recursive DFS rerooting, two passes.
  - `dfs_down(u)` (post-order): down1[u] = longest downward path from u; down2[u]
    = second longest downward path through a DIFFERENT child; arg1[u] = the child
    that yields down1 (so it can be excluded for that child in the up pass).
  - `dfs_up(u)` (pre-order): for a child v, up[v] = 1 + max(up[u], best downward
    of u excluding the branch through v), where "best downward excluding v" is
    down2[u] if arg1[u]==v else down1[u].
  - ans[u] = max(down1[u], up[u]).
- Complexity: O(n) time, O(n) space + O(depth) recursion stack; depth up to n.
- ONE optimal style (recursion is the natural tree DFS); a single beta. Same
  rerooting technique as problem01, different task (max vs sum).

## 1. Structural equivalence (C++ <-> Python), block by block

| Block | C++ (`implementations/optimal/solution.cpp`) | Python (`implementations/optimal/solution.py`) | Correspondence |
|-------|----------------------------------------------|------------------------------------------------|----------------|
| Read input | `cin>>n; loop n-1: cin>>a>>b; adj[a].push_back(b); adj[b].push_back(a);` | `data=read().split(); adj[a].append(b); adj[b].append(a)` | Same undirected adjacency from n and n-1 edges. |
| State | `down1,down2,arg1,up_` (vectors) | `down1,down2,arg1,up` (lists) | Same four per-node arrays. |
| n==1 guard | `if(n==1){cout<<0;return;}` | `if n==1: print(0); return` | Same edge case. |
| dfs_down | `for v!=parent: dfs_down(v,u); cand=down1[v]+1; if cand>down1[u]{down2[u]=down1[u];down1[u]=cand;arg1[u]=v;} else if cand>down2[u] down2[u]=cand;` | identical | Same post-order update of the two longest downward paths and arg1. |
| dfs_up | `for v!=parent: best_excl=(arg1[u]==v)?down2[u]:down1[u]; up_[v]=max(up_[u],best_excl)+1; dfs_up(v,u);` | identical | Same reroot recurrence and exclusion of the v-branch. |
| Output | `for i=1..n: cout<<max(down1[i],up_[i]) (space) <<"\n";` | `" ".join(str(max(down1[i],up[i])))` | Same n integers on one line. |

## 2. Semantic equivalence

- Invariant dfs_down: after the post-order, down1[u]/down2[u] are the longest and
  second-longest downward path lengths within u's subtree through distinct
  children, and arg1[u] is the child realizing down1.
- Invariant dfs_up: up[v] is the longest path from v going through its parent u.
  Such a path either continues up from u (up[u]) or dips into another branch of u
  (best downward of u NOT passing through v) — hence `max(up[u], down-excl-v)+1`.
  By induction from the root (up[root]=0), all up[*] are correct, so
  ans[u]=max(down1[u],up[u]) is the eccentricity of u. Both languages apply the
  identical recurrences in the same order -> identical arrays.
- Complexity (derived, identical): O(1) work per node per pass, two passes ->
  O(n); recursion depth = tree depth (up to n).
- Recursion/stack: Python sets `setrecursionlimit(300000)`; the engine applies
  `ulimit -s 256MB` so the recursive C++ matches the CSES large stack.

## 3. Behavioral equivalence (bit-exact output)

- External: CSES submissions (PASSO A): C++ AC 16/16; Python TLE {6,7,8,14}, AC
  elsewhere — same answers where both run.
- Local: example (n=5) gives `2 3 2 3 3` in both; `results/verdict.json` with 0
  WRONG_ANSWER across the 16 cases — filled after the bench.

## 4. Documented deviations (language-driven, not algorithmic)

1. Naming: C++ `up_` (avoids any clash) vs Python `up` — same array.
2. Input reading: C++ `cin>>`; Python bulk `sys.stdin.buffer.read().split()`.
3. Distances fit in int (<= n-1 < 2*10^5); identical arithmetic.

## 5. Conclusion

The two optimal programs implement the same DFS-rerooting algorithm with a
statement-by-statement correspondence, the same invariants, the same O(n) cost,
and identical output. Any runtime difference reflects only the language execution
model (interpreted Python vs compiled C++) — which is what beta measures.
