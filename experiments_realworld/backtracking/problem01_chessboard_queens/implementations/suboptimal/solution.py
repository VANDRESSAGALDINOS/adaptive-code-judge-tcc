import sys

# SUBOPTIMAL: the SAME recursive search as the optimal, but WITHOUT the
# incremental column/diagonal pruning. It still places one queen per row on a
# free square, but it does NOT reject conflicting columns/diagonals during the
# descent; instead it validates the full placement only at the leaf (r == 8).
# This is a genuine algorithmic inefficiency (no early branch cutting): it
# explores the entire tree of one-queen-per-row placements (~product of free
# cells per row, up to 8^8) and checks all pairs at the end. Same answer as the
# optimal; only the pruning is removed. Selectivity check for backtracking.

def main():
    board = [sys.stdin.readline().strip() for _ in range(8)]

    cols = [0] * 8
    ans = 0

    def dfs(r: int):
        nonlocal ans
        if r == 8:
            # No pruning during descent: validate the complete placement here.
            for i in range(8):
                for j in range(i + 1, 8):
                    if cols[i] == cols[j]:
                        return
                    if abs(cols[i] - cols[j]) == abs(i - j):
                        return
            ans += 1
            return
        for c in range(8):
            if board[r][c] == '*':
                continue
            cols[r] = c
            dfs(r + 1)

    dfs(0)
    print(ans)

if __name__ == "__main__":
    main()
