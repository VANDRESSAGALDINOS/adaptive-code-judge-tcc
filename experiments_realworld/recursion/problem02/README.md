# recursion/problem02 — Distinct Colors (CSES 1139)

- CSES: https://cses.fi/problemset/task/1139
- Time limit: 1.00 s | Memory limit: 512 MB
- Input: `n`, then `n` colors `c_1..c_n`, then `n-1` edges `a b` of a rooted tree
  (root = node 1). Output: for each node, the number of distinct colors in its
  subtree.

## Design
- ONE optimal style: recursive DFS + small-to-large merging. Each DFS call
  returns the set of colors in the subtree; a parent merges each child's set into
  its own, always iterating the SMALLER set into the LARGER (small-to-large) ->
  O(n log n) total.
- This is a DEEP-RECURSION problem with a DIFFERENT profile from problem01 (Tree
  Distances II, pure O(n) rerooting): here the per-node work combines the
  recursion with data-structure operations (set merges). The injustice is by
  TIME (TLE), driven by both the recursive call overhead and the set work in
  Python.

## CSES validation (REGRA #0, before any local bench)
- C++ recursive: ACCEPTED 16/16 (max 0.41 s).
- Python recursive: TLE on {6,7,8} (3/16); AC on the others but BORDERLINE —
  #15 = 1.00 s (exactly at the limit), #9 = 0.94 s, #14 = 0.85 s, #13 = 0.83 s.
  setrecursionlimit(300000).
- Same solution, language injustice confirmed externally. Honest caveat: this is
  a borderline case (Python near the limit on several cases) — less clean than
  problem01, but a legitimate point on the spectrum where the injustice starts to
  appear, with a different profile (recursion + data structure).

## Notes
- Input scales (n up to 2*10^5) -> beta is calibratable.
- Colors up to 1e9 (use a hash set / std::set; no array indexing by color).
- Recursion depth up to n (chain); the engine applies ulimit -s 256MB so the
  recursive C++ matches the CSES large stack (same as problem01 / dp01).
