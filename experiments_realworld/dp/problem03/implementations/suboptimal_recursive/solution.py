import sys
sys.setrecursionlimit(1000000)

MOD = 1000000007

# SUBOPTIMAL: naive top-down recursion WITHOUT memoization.
# Same recurrence as the optimal recursive (count_ways(i,t) = count_ways(i-1,t)
# + count_ways(i-1,t-i)), but recomputes overlapping subproblems -> exponential
# (~2^n nodes), while the memoized optimal is O(n*target). Computes the same
# value. Recursion depth is the same as the optimal (O(n)); only the branching
# (no memo) makes it blow up -- genuine algorithmic inefficiency, not a slowdown.
def count_ways(i, target_sum):
    if target_sum == 0:
        return 1
    if i <= 0 or target_sum < 0:
        return 0
    result = count_ways(i-1, target_sum)
    if target_sum >= i:
        result = (result + count_ways(i-1, target_sum-i)) % MOD
    return result

def main():
    n = int(input())

    total_sum = n * (n + 1) // 2

    if total_sum % 2 == 1:
        print(0)
        return

    target = total_sum // 2

    ways = count_ways(n, target)
    result = ways * pow(2, MOD-2, MOD) % MOD
    print(result)

if __name__ == "__main__":
    main()
