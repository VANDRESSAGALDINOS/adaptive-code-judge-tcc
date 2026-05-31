MOD = 1000000007

# SUBOPTIMAL (deliberately slowed, NOT a worse algorithm): the optimal bottom-up
# DP (rolling two-row, O(n*target)) recomputed SLOW_FACTOR times. Same algorithm
# and same answer as the optimal iterative, just SLOW_FACTOR times slower. This is
# the selectivity check for the iterative style: a correct-but-too-slow submission
# that must be REJECTED (far slower than the optimal, beyond the adaptive limit).
# Same convention as graphs/problem01 and dp/problem01-02.
SLOW_FACTOR = 100

def main():
    n = int(input())

    total_sum = n * (n + 1) // 2

    if total_sum % 2 == 1:
        print(0)
        return

    target = total_sum // 2

    ways = 0
    for _ in range(SLOW_FACTOR):
        prev = [0] * (target + 1)
        curr = [0] * (target + 1)
        prev[0] = 1
        for i in range(1, n + 1):
            curr[0] = 1
            for j in range(1, target + 1):
                curr[j] = prev[j]
                if j >= i:
                    curr[j] = (curr[j] + prev[j - i]) % MOD
            prev, curr = curr, prev
        ways = prev[target]

    result = ways * pow(2, MOD - 2, MOD) % MOD
    print(result)

if __name__ == "__main__":
    main()
