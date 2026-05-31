# backtracking/problem01 — Chessboard and Queens (CSES 1624)

- CSES: https://cses.fi/problemset/task/1624
- Time limit: 1.00 s | Memory limit: 512 MB
- Input: 8x8 board, each square free (`.`) or blocked (`*`). Output: number of
  ways to place 8 non-attacking queens on free squares.

## Design
- ONE optimal style: recursive backtracking (DFS row by row) with column and
  two-diagonal pruning. Backtracking has no idiomatic iterative counterpart
  (an "iterative" version would just be a hand-rolled call stack over the same
  decision tree), so there is one optimal and one beta.
- Suboptimal (selectivity check): the SAME recursive search WITHOUT the
  column/diagonal pruning (genuine algorithmic inefficiency), created in the
  suboptimal phase.

## Notes
- Recursion depth is fixed at 8 (no stack issue).
- All inputs are 72 bytes (fixed 8x8 board), so the "largest input by bytes"
  selector does not distinguish cases; the calibration case is overridden to
  the heaviest search tree (case 1, the empty board, 92 solutions) via `--case 1`.
- The optimal is trivial in both languages on CSES (both AC, ~0 ms), so the
  unjust-TLE dimension does not appear on the optimal here; queens contributes
  on the SELECTIVITY dimension (the unpruned suboptimal).

Legacy material (previous methodology) is quarantined under `_legacy/`.
