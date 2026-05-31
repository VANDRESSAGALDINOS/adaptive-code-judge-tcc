# Equivalence Proof — Chessboard and Queens (CSES 1624)

Scope note: "formal" here means systematic and explicit, NOT a machine-checked
proof in a formal-methods system. This document establishes the cross-language
equivalence (C++ <-> Python) of the optimal solution, mapping the two programs
statement by statement, plus a semantic argument and the behavioral evidence.

## 0. Objective, algorithm, complexity

- Problem: count placements of 8 mutually non-attacking queens on an 8x8 board
  where queens may only sit on free squares (`.`); blocked squares (`*`) are
  forbidden as positions but do NOT block attacks.
- Algorithm (single optimal style): recursive backtracking, one queen per row,
  with incremental pruning on the occupied column and the two diagonals.
- Complexity: O(8!) in the worst case, heavily pruned in practice; space O(1)
  for the constraint state + O(8) recursion stack (depth fixed at 8).
- There is ONE optimal style: backtracking has no idiomatic iterative
  counterpart (an iterative version is just a manual call stack over the same
  tree), so a single beta is calibrated.

## 1. Structural equivalence (C++ <-> Python), block by block

Diagonal indexing is identical in both: the anti-diagonal id is `r + c`
(range 0..14) and the main-diagonal id is `r - c + 7` (range 0..14).

| Block | C++ (`implementations/optimal/solution.cpp`) | Python (`implementations/optimal/solution.py`) | Correspondence |
|-------|----------------------------------------------|------------------------------------------------|----------------|
| Read board | `vector<string> g(8); for(i<8) cin>>g[i];` | `board=[sys.stdin.readline().strip() for _ in range(8)]` | Both load 8 row-strings of 8 chars. `cin>>` reads one whitespace-delimited token = the row; `.strip()` drops the newline. Same 8 strings. |
| Constraint state | `bool col[8]={}, d1[15]={}, d2[15]={};` (mutated in place) | masks `cols, d1, d2` (ints), passed as args | `col[c]==1 <=> cols & (1<<c)`; `d1[r+c]==1 <=> d1 & (1<<(r+c))`; `d2[r-c+7]==1 <=> d2 & (1<<(r-c+7))`. Boolean-array bit <-> mask bit. |
| Counter | `long long ans=0;` | `ans=0` (`nonlocal`) | Same accumulator. |
| Base case | `if(r==8){++ans;return;}` | `if r==8: ans+=1; return` | Identical: a full placement (8 rows filled) counts one. |
| Column loop | `for(int c=0;c<8;++c)` | `for c in range(8)` | Same iteration order over the 8 columns of row `r`. |
| Blocked skip | `if(g[r][c]=='*')continue;` | `if board[r][c]=='*': continue` | Identical: never place on a blocked square. |
| Conflict test | `int id1=r+c,id2=r-c+7; if(col[c]||d1[id1]||d2[id2])continue;` | `bc=1<<c;b1=1<<(r+c);b2=1<<(r-c+7); if (cols&bc) or (d1&b1) or (d2&b2): continue` | Same pruning: reject if column or either diagonal already used. |
| Place + recurse + undo | `col[c]=d1[id1]=d2[id2]=true; dfs(r+1); col[c]=d1[id1]=d2[id2]=false;` | `dfs(r+1, cols\|bc, d1\|b1, d2\|b2)` | Same effect (see deviation #1): C++ sets the shared state, recurses, then restores it; Python passes a modified COPY down, leaving the caller's masks unchanged on return. Both explore row `r+1` with exactly column `c` + its diagonals marked. |
| Output | `cout<<ans<<"\n";` | `print(ans)` | Single integer + newline. |

## 2. Semantic equivalence

- Invariant (both): when `dfs` is entered for row `r`, the state marks exactly
  the columns and diagonals occupied by the `r` queens placed on rows `0..r-1`,
  which form a partial non-attacking configuration. Proof by induction on `r`:
  base `r=0` empty state holds; step — a column `c` survives the conflict test
  iff it conflicts with no previously placed queen, and the recursive call marks
  exactly `c`/`r+c`/`r-c+7`, preserving the invariant for `r+1`. At `r=8` the
  invariant says all 8 queens are mutually non-attacking, so `++ans` counts a
  valid placement, and every valid placement is reached exactly once (queens are
  fixed one per row in increasing row order). Hence both count the same set.
- Complexity (derived, identical): each node does O(8) work over columns; the
  pruned tree has the same shape in both languages (identical prune decisions),
  so both are O(8!) worst case / same pruned node count; recursion depth = 8.
- Recursion/stack: depth is fixed at 8 — no stack-limit concern in either
  language (no `setrecursionlimit` needed; no C++ stack-size issue).

## 3. Behavioral equivalence (bit-exact output)

- External: CSES submission of both optimal solutions (PASSO A) — to record.
- Local: `results/verdict.json` with 0 WRONG_ANSWER across all 10 cases — to
  fill after the bench. Expected outputs (CSES test data): case 1..10 =
  92, 74, 72, 11, 13, 10, 2, 2, 1, 1.

## 4. Documented deviations (language-driven, not algorithmic)

1. State threading: C++ mutates shared `col/d1/d2` arrays and undoes them after
   the recursive call (classic backtracking restore); Python passes immutable
   ints (`cols|bc`, ...) by value, so the caller's state is intact on return
   without an explicit undo. Same set of marked constraints during the child
   call — equivalent, just the standard mutable-vs-immutable idiom.
2. State representation: C++ boolean arrays vs Python integer bitmasks — same
   information, mapping given in block 1.
3. Input reading: `cin>>` (token) vs `readline().strip()` (line) — both yield
   the 8-character row strings.

## 5. Conclusion

The two optimal programs implement the same pruned backtracking search with a
statement-by-statement correspondence, the same loop invariant, the same pruned
search tree, and identical output. Any runtime difference reflects only the
language execution model (interpreted Python vs compiled C++), which is exactly
what beta measures.
