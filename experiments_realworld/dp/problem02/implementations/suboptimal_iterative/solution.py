import sys

MOD = 1000000007

# SUBOPTIMAL (deliberately slowed, NOT a worse algorithm): the optimal bottom-up
# DP recomputed SLOW_FACTOR times. Same algorithm and same answer as the optimal
# iterative, just SLOW_FACTOR times slower. Selectivity check for the iterative
# style: a correct-but-too-slow submission that must be REJECTED. Same convention
# as graphs/problem01 and dp/problem01.
# NOTE: SLOW_FACTOR=100 was already ENOUGH for Python on CSES (TLE on {6,7,8,9,10})
# but NOT for C++ (ACCEPTED 15/15, max 0.96s) -- the language gap is so wide that a
# 100x-slowed iterative C++ still passes while a correct recursive Python TLEs.
# Raised to 300 so the C++ side is also rejected (clean selectivity for the
# iterative style in BOTH languages). See anotacoes_para_artigo.md.
SLOW_FACTOR = 300

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    n = int(next(it))

    grid = []
    for _ in range(n):
        grid.append(next(it).decode('utf-8'))

    answer = 0
    for _ in range(SLOW_FACTOR):
        dp = [[0 for _ in range(n)] for _ in range(n)]
        if grid[0][0] != '*':
            dp[0][0] = 1
        for j in range(1, n):
            if grid[0][j] != '*':
                dp[0][j] = dp[0][j-1]
        for i in range(1, n):
            if grid[i][0] != '*':
                dp[i][0] = dp[i-1][0]
        for i in range(1, n):
            for j in range(1, n):
                if grid[i][j] != '*':
                    dp[i][j] = (dp[i-1][j] + dp[i][j-1]) % MOD
        answer = dp[n-1][n-1]

    print(answer)

if __name__ == "__main__":
    main()
