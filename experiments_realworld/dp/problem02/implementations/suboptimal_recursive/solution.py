import sys
sys.setrecursionlimit(2000000)

MOD = 1000000007

# SUBOPTIMAL: naive top-down recursion WITHOUT memoization.
# Same recurrence as the optimal recursive (paths(i,j) = paths(i,j+1) +
# paths(i+1,j)), but recomputes overlapping subproblems -> exponential in the
# number of paths (~C(2n,n)), while the memoized/iterative optimal is O(n^2).
# Computes the same value. Recursion depth is the same as the optimal (O(n)).
def solve(i, j, grid, n):
    if i >= n or j >= n or grid[i][j] == '*':
        return 0
    if i == n-1 and j == n-1:
        return 1
    return (solve(i, j+1, grid, n) + solve(i+1, j, grid, n)) % MOD

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    n = int(next(it))

    grid = []
    for _ in range(n):
        grid.append(next(it).decode('utf-8'))

    print(solve(0, 0, grid, n))

if __name__ == "__main__":
    main()
