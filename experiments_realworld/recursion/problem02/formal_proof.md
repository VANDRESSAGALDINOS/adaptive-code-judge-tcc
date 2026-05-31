# Equivalence Proof — Distinct Colors (CSES 1139)

Scope note: "formal" here means systematic and explicit, NOT a machine-checked
proof in a formal-methods system. This document establishes the cross-language
equivalence (C++ <-> Python) of the optimal solution, mapping the two programs
statement by statement, plus a semantic argument and the behavioral evidence.

## 0. Objective, algorithm, complexity

- Problem: rooted tree (root = 1), each node has a color; for each node output the
  number of DISTINCT colors in its subtree.
- Algorithm (single optimal style): recursive DFS returning the set of colors of
  the subtree; at each node, merge the children's sets using small-to-large
  (always iterate the smaller set into the larger). `ans[u]` = size of the merged
  set.
- Complexity: O(n log n) time (small-to-large bound), O(n) space + O(depth)
  recursion stack; depth up to n (chain) -> deep recursion.
- ONE optimal style: recursion is the natural form of the tree DFS; a single beta
  is calibrated. NOTE: the per-node cost mixes recursion with set operations
  (data structure), a different profile from problem01's pure O(n) rerooting.

## 1. Structural equivalence (C++ <-> Python), block by block

| Block | C++ (`implementations/optimal/solution.cpp`) | Python (`implementations/optimal/solution.py`) | Correspondence |
|-------|----------------------------------------------|------------------------------------------------|----------------|
| Read input | `cin>>n; for i: cin>>color[i]; loop n-1: cin>>a>>b; adj[a].push_back(b); adj[b].push_back(a);` | `data=read().split(); n; color[1..n]; loop: adj[a].append(b); adj[b].append(a)` | Same n, n colors, n-1 undirected edges. |
| State | `vector<int> color, ans; vector<set<int>*> sub;` | `color[], ans[]; dfs returns a set` | Per-node color, answer; subtree color-set held per node (C++ via pointer, Python via return value) — see deviation #1. |
| Leaf/own color | `s=new set; s->insert(color[u]);` | `s = {color[u]}` | Start the node's set with its own color. |
| Recurse children | `for v in adj[u]: if v!=parent: dfs(v,u); cs=sub[v];` | `for v: if v!=parent: cs=dfs(v,u)` | Same DFS over children (skip parent). |
| Small-to-large | `if(cs->size()>s->size()) swap(s,cs); for x in *cs: s->insert(x);` | `if len(cs)>len(s): s,cs=cs,s; s.update(cs)` | Identical rule: ensure `s` is the larger set, then merge the smaller `cs` into it. |
| Record answer | `ans[u]=s->size(); sub[u]=s;` | `ans[u]=len(s); return s` | Same: answer = size of merged set; the set propagates upward. |
| Output | `for i=1..n: cout<<ans[i] (space) <<"\n";` | `" ".join(str(ans[i]))` | Same n integers on one line. |

## 2. Semantic equivalence

- Invariant: `dfs(u)` returns exactly the set of distinct colors appearing in u's
  subtree. Proof by induction: a leaf returns `{color[u]}`; an internal node
  starts with `{color[u]}` and unions every child's subtree-color-set, which by
  hypothesis are exactly the children's subtree colors — the union is exactly u's
  subtree colors. Hence `ans[u]` = number of distinct colors in u's subtree, in
  both languages.
- small-to-large does not change the RESULT (set union is commutative); it only
  bounds the total merge work at O(n log n). Both languages apply the same
  swap-then-merge, so they compute identical sets and identical sizes.
- Complexity (derived, identical): each element is moved into a strictly larger
  set at most O(log n) times -> O(n log n) inserts both; recursion depth = tree
  depth (up to n).
- Recursion/stack: Python sets `setrecursionlimit(300000)`; the engine applies
  `ulimit -s 256MB` so the recursive C++ matches the CSES large stack (depth up
  to n). The depth is the language-stressing variable (S3.1).

## 3. Behavioral equivalence (bit-exact output)

- External: CSES submissions (PASSO A): C++ AC 16/16; Python TLE {6,7,8}, AC
  elsewhere (borderline) — same answers where both run.
- Local: example (n=5) gives `3 1 2 1 1` in both. `results/verdict.json` with 0
  WRONG_ANSWER across the cases — to fill after the bench.

## 4. Documented deviations (language-driven, not algorithmic)

1. Set ownership: C++ holds each subtree's set via a heap pointer (`set<int>*`,
   freed after merge) to allow O(1) swap and avoid copies; Python returns the set
   object by value (reference) from the recursive call. Same logical set and same
   small-to-large semantics; only the ownership mechanism differs.
2. Set type: C++ `std::set<int>` (balanced tree, ordered); Python `set` (hash).
   Both are exact sets of the same elements; ordering is irrelevant (only the
   distinct count is used).
3. Colors up to 1e9: both store colors directly in the set (no array indexing by
   color value), so the large color range is handled identically.
4. Input reading: C++ `cin>>`; Python bulk `sys.stdin.buffer.read().split()`.

## 5. Conclusion

The two optimal programs implement the same DFS + small-to-large algorithm with a
statement-by-statement correspondence, the same invariant, the same O(n log n)
cost, and identical output. Any runtime difference reflects only the language
execution model (interpreted Python vs compiled C++) — which is what beta
measures.
