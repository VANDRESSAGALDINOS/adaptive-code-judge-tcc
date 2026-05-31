# recursion/problem01 — Tree Distances II (CSES 1133)

- CSES: https://cses.fi/problemset/task/1133
- Time limit: 1.00 s | Memory limit: 512 MB
- Input: `n`, then `n-1` edges `a b` of a tree. Output: for each node, the sum of
  the distances from that node to all other nodes.

## Design
- ONE optimal style: recursive DFS rerooting (two recursive passes):
  - `dfs1` (post-order): subtree sizes `cnt[u]` and `res[1]` = sum of depths from
    the root;
  - `dfs2` (pre-order): reroot, `res[v] = res[u] + (n - cnt[v]) - cnt[v]`.
- This is a DEEP-RECURSION problem (the category fenomenon): the tree can
  degenerate into a chain, giving recursion depth up to n = 2*10^5. Python pays
  the per-call interpreter overhead; the heavy cases push it over the 1.0 s limit
  while C++ stays well under it (same algorithm, only the language differs).

## CSES validation (REGRA #0, before any local bench)
- Python recursive: TLE on {6,7,8,14} (4/15); AC on the others, borderline on the
  medium cases (#9,#10 = 0.72 s, #15 = 0.69 s).
- C++ recursive: ACCEPTED 15/15 (max 0.22 s).
- Same solution, language injustice confirmed externally. Input scales (n up to
  2*10^5) -> beta is calibratable here (unlike the fixed-size backtracking cases).

## Notes
- This problem was selected by an empirical sweep of recursive tree problems:
  Subordinates (1674, 1 DFS) -> Python AC 0.59 s (too light); Tree Diameter
  (1131, 2 DFS) -> Python AC at the edge (0.94 s); Tree Distances II (1133,
  rerooting) -> Python TLE. Not every recursive problem yields TLE in Python; the
  decisiveness depends on the per-node work and the input size (QP3).
- Stack-overflow (RUNTIME ERROR) was NOT observed: the official CSES test data
  for these tree problems does not include the deep straight-chain case. The
  injustice observed here is by TIME (TLE), not by stack (RTE).
- `setrecursionlimit(300000)` is set in the Python solution for the chain depth.

The previous empty placeholders (recursion/problem01..03) are unrelated stubs and
are left untouched for now.
