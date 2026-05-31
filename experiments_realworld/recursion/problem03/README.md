# recursion/problem03 — Tree Distances I (CSES 1132)

- CSES: https://cses.fi/problemset/task/1132
- Time limit: 1.00 s | Memory limit: 512 MB
- Input: `n`, then `n-1` edges `a b` of a tree. Output: for each node, the maximum
  distance from that node to any other node.

## Design
- ONE optimal style: recursive DFS rerooting, two passes:
  - `dfs_down`: down1[u] (longest downward path), down2[u] (second longest, via a
    different child), arg1[u] (child giving down1);
  - `dfs_up`: up[v] = 1 + max(up[u], best downward of u excluding the branch v);
  - ans[u] = max(down1[u], up[u]).
- DEEP-RECURSION problem. Same rerooting TECHNIQUE as problem01 (Tree Distances
  II) but a DIFFERENT task — maximum distance (needs down1/down2/up) vs sum of
  distances. Recursion depth up to n = 2*10^5 (chain).

## CSES validation (REGRA #0, before any local bench)
- C++ recursive: ACCEPTED 16/16.
- Python recursive: TLE on {6,7,8,14} (4/16); AC on the rest, borderline
  (#9,#10=0.78 s, #16=0.80 s). setrecursionlimit(300000).
- Same solution, language injustice confirmed externally. Input scales (n up to
  2*10^5) -> beta is calibratable.

## Notes
- Recursion depth up to n (chain); the engine applies ulimit -s 256MB so the
  recursive C++ matches the CSES large stack (same as problem01 / dp01).
- Honest note: this shares the rerooting technique with problem01 — a sibling in
  method, distinct in task. Kept as a third recursion case at the user's request.
