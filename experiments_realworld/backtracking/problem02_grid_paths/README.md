# backtracking/problem02 — Grid Paths (CSES 1625)

- CSES: https://cses.fi/problemset/task/1625
- Time limit: 1.00 s | Memory limit: 512 MB
- Input: one line of 48 characters over `{D,U,L,R,?}` describing a path
  template. Output: the number of paths from the upper-left to the lower-left
  corner of a 7x7 grid that visit every square exactly once and follow the
  fixed moves, with `?` free to be any direction.

## Design
- ONE optimal style: recursive backtracking over the 48-move path with three
  prunings — dead-end detection (`check`), split/trap detection (`trap`), and
  early termination when the goal is reached before move 48. Backtracking has
  no idiomatic iterative counterpart, so there is one optimal and one beta.
- Suboptimal (selectivity check): the SAME recursive search WITHOUT the
  prunings (genuine algorithmic inefficiency), created in the suboptimal phase.

## Notes
- Recursion depth is fixed at 48 (no stack issue).
- All inputs are 48-char strings; the search-tree size is driven by the number
  of `?` (free moves), not by input bytes, so the "largest input by bytes"
  selector does not distinguish cases. The calibration case is overridden to
  the heaviest tree (case 11, all 48 `?`, output 88418) via `--case 11`.

Legacy material (previous methodology, plus the previous test_data which was
mistakenly a copy of the Queens/1624 boards) is quarantined under `_legacy/`.
The correct CSES 1625 test data (20 cases) is in `test_data/`.
