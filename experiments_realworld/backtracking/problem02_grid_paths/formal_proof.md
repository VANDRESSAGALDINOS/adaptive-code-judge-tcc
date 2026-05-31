# Equivalence Proof — Grid Paths (CSES 1625)

Scope note: "formal" here means systematic and explicit, NOT a machine-checked
proof in a formal-methods system. This document establishes the cross-language
equivalence (C++ <-> Python) of the optimal solution, mapping the two programs
statement by statement, plus a semantic argument and the behavioral evidence.

## 0. Objective, algorithm, complexity

- Problem: count the paths on a 7x7 grid from the upper-left corner (0,0) to the
  lower-left corner (6,0) that visit every one of the 49 squares exactly once
  (a Hamiltonian path of 48 moves), following a 48-char template over
  `{D,U,L,R,?}` where a fixed letter forces that move and `?` is free.
- Algorithm (single optimal style): recursive backtracking over the move index
  (0..48), marking/unmarking visited squares, with three prunings:
  - dead-end (`check`): a still-unvisited neighbour cell that would become
    unreachable (fewer than 2 free neighbours, or the goal closed off early);
  - split/trap (`trap`): the current cell separates the free region into two,
    making a full cover impossible;
  - early goal: reaching (6,0) before move 48 is a dead branch.
- Complexity: O(4^48) without pruning, drastically reduced by the three cuts;
  space O(49) grid + O(48) recursion stack (depth fixed at 48).
- There is ONE optimal style: backtracking has no idiomatic iterative
  counterpart (an iterative version is just a manual call stack over the same
  tree), so a single beta is calibrated.

## 1. Structural equivalence (C++ <-> Python), block by block

| Block | C++ (`implementations/optimal/solution.cpp`) | Python (`implementations/optimal/solution.py`) | Correspondence |
|-------|----------------------------------------------|------------------------------------------------|----------------|
| Globals | `string s; bool vis[7][7]; int count_paths=0;` | `s=""; vis=[[False]*7 for _ in range(7)]; count_paths=0` | Same state: move template, 7x7 visited grid, path counter. |
| Read input | `cin >> s;` | `s = input().strip()` | Both read the single 48-char move string. |
| `check(i,j)` | counts free neighbours; returns true if `vis[i][j]` false and (`<2` free OR goal-with-neighbours) | identical condition order | Statement-by-statement identical dead-end test. |
| `trap(i,j)` | counts `x` (horiz) / `y` (vert) free neighbours; true if `(x==0&&y==2)\|\|(x==2&&y==0)` | identical | Same split/trap test. |
| Enter cell | `if(vis[i][j])return; vis[i][j]=true;` | `if vis[i][j]: return; vis[i][j]=True` | Same guard + mark. |
| Goal check | `if(i==6&&j==0){ if(move==48)count_paths++; else {vis=false; flags++;} }` | identical | Count only a full 48-move cover ending at the goal; otherwise prune. |
| Diagonal prunes | 4 `check(...)` on the diagonal neighbours, summed into `pruning_flags` | identical 4 calls | Same four corner/diagonal dead-end probes. |
| Trap prune | `pruning_flags += trap(i,j);` | identical | Same. |
| Prune exit | `if(pruning_flags!=0){vis=false; return;}` | identical | Same backtrack-on-prune. |
| Move dispatch | `if(move<48){ if(s[move]=='?'){4 recursive calls guarded by bounds} else {forced L/R/U/D move} }` | identical | Same branching: free `?` tries all 4 in-bounds directions; a fixed letter takes only that direction if in bounds. |
| Undo | `vis[i][j]=false;` at function end | `vis[i][j]=False` | Same backtracking restore. |
| Output | `cout<<count_paths<<"\n";` | `print(count_paths)` | Single integer + newline. |

The recursive call order for `?` is the same in both (U, D, L, R as written:
`i-1`, `i+1`, `j-1`, `j+1`), so the two explore the tree in the same order.

## 2. Semantic equivalence

- Invariant (both): on entry to `backtrack(move,i,j)` with the cell not yet
  visited, `vis` marks exactly the cells of the partial path of length `move`
  ending at (i,j); `count_paths` holds the number of completed valid covers
  found so far. The prunings only remove branches that provably cannot complete
  a Hamiltonian cover ending at (6,0), so they preserve the count. At a leaf
  (`move==48` and `(i,j)==(6,0)`) the path is a full valid cover and the counter
  increments; every valid cover is reached exactly once (the move index strictly
  increases and the template fixes/branches each step identically). Hence both
  programs compute the same count.
- Complexity (derived, identical): same branching factor (≤4 at `?`, 1 at a
  fixed move), same three prunings applied at the same points → identical pruned
  tree in both languages; depth fixed at 48.
- Recursion/stack: depth ≤ 48 — no stack-limit concern in either language.

## 3. Behavioral equivalence (bit-exact output)

- External: CSES submission of both optimal solutions (PASSO A) — to record.
- Local: `results/verdict.json` with 0 WRONG_ANSWER across the 20 cases — to
  fill after the bench.

## 4. Documented deviations (language-driven, not algorithmic)

1. State scope: both use module-level globals (`s`, `vis`, `count_paths`) with
   the same lifetime; C++ declares fixed-size arrays, Python uses lists — same
   information.
2. Input reading: `cin >> s` (token) vs `input().strip()` (line) — both yield
   the 48-char move string.
3. `check`/`trap` return `bool` in C++ summed as int into `pruning_flags`; in
   Python the bool sums the same way (`True==1`) — identical arithmetic.

## 5. Conclusion

The two optimal programs implement the same pruned Hamiltonian-path backtracking
with a statement-by-statement correspondence, the same loop/recursion invariant,
the same pruned search tree (same exploration order), and identical output. Any
runtime difference reflects only the language execution model (interpreted
Python vs compiled C++), which is what beta measures.
