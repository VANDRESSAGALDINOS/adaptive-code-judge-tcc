import sys
sys.setrecursionlimit(1100000)

MOD = 1000000007

# SUBOPTIMAL: naive top-down recursion WITHOUT memoization.
# Same recurrence as the optimal (ways(s) = sum over coins of ways(s-coin)),
# but recomputes overlapping subproblems -> exponential in the answer size,
# while the memoized/iterative optimal is O(x*n). Computes the same value.
def solve(remaining, coins):
    if remaining == 0:
        return 1
    if remaining < 0:
        return 0
    result = 0
    for coin in coins:
        if remaining >= coin:
            result = (result + solve(remaining - coin, coins)) % MOD
    return result

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    n = int(next(it))
    x = int(next(it))

    coins = []
    for _ in range(n):
        coins.append(int(next(it)))

    print(solve(x, coins))

if __name__ == "__main__":
    main()
