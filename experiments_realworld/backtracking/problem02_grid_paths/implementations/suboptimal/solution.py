s = ""
vis = [[False] * 7 for _ in range(7)]
count_paths = 0

# SUBOPTIMAL: the SAME recursive Hamiltonian-path search as the optimal, but
# WITHOUT the efficiency prunings (the four dead-end `check` probes and the
# `trap`/split test). It still marks visited cells, still treats the goal (6,0)
# as terminal (a path may reach it only as the final, 48th move), and counts the
# same valid covers -> identical answer. Removing the prunings is a genuine
# algorithmic inefficiency: the search no longer cuts branches that cannot
# complete a cover, so the explored tree blows up (~O(4^48) in the worst case).
# Selectivity check for backtracking: a correct-but-too-slow submission that must
# be REJECTED even under the adaptive limit.

def backtrack(move, i, j):
    global count_paths

    if vis[i][j]:
        return

    vis[i][j] = True

    # Goal cell is terminal (correctness rule, NOT an efficiency pruning): a path
    # may stand on (6,0) only as its last cell. Count iff it is the 48th move.
    if i == 6 and j == 0:
        if move == 48:
            count_paths += 1
        vis[i][j] = False
        return

    if move < 48:
        if s[move] == '?':
            if i-1 >= 0:
                backtrack(move+1, i-1, j)
            if i+1 < 7:
                backtrack(move+1, i+1, j)
            if j-1 >= 0:
                backtrack(move+1, i, j-1)
            if j+1 < 7:
                backtrack(move+1, i, j+1)
        else:
            if s[move] == 'L' and j-1 >= 0:
                backtrack(move+1, i, j-1)
            elif s[move] == 'R' and j+1 < 7:
                backtrack(move+1, i, j+1)
            elif s[move] == 'U' and i-1 >= 0:
                backtrack(move+1, i-1, j)
            elif s[move] == 'D' and i+1 < 7:
                backtrack(move+1, i+1, j)

    vis[i][j] = False

def main():
    global s
    s = input().strip()
    backtrack(0, 0, 0)
    print(count_paths)

if __name__ == "__main__":
    main()
