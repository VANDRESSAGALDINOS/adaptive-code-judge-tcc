import sys

MOD = 1000000007

# SUBOPTIMAL (deliberately slowed, NOT a worse algorithm): the optimal bottom-up
# DP recomputed SLOW_FACTOR times. Same algorithm and same answer as the optimal
# iterative, just SLOW_FACTOR times slower. This is the selectivity check for the
# iterative style: a correct-but-too-slow submission that must be REJECTED (it is
# far slower than the optimal, beyond the adaptive limit). Same convention as
# graphs/problem01's SLOW_FACTOR.
SLOW_FACTOR = 100

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    n = int(next(it))
    x = int(next(it))

    coins = []
    for _ in range(n):
        coins.append(int(next(it)))

    answer = 0
    for _ in range(SLOW_FACTOR):
        dp = [0] * (x + 1)
        dp[0] = 1
        for s in range(1, x + 1):
            for coin in coins:
                if s >= coin:
                    dp[s] = (dp[s] + dp[s - coin]) % MOD
        answer = dp[x]

    print(answer)

if __name__ == "__main__":
    main()
