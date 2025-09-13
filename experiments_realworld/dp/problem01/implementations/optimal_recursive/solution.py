import sys
sys.setrecursionlimit(1100000)

MOD = 1000000007

def solve(remaining, coins, memo):
    if remaining == 0:
        return 1
    if remaining < 0:
        return 0
    if memo[remaining] != -1:
        return memo[remaining]
    
    result = 0
    for coin in coins:
        if remaining >= coin:
            result = (result + solve(remaining - coin, coins, memo)) % MOD
    
    memo[remaining] = result
    return result

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    
    n = int(next(it))
    x = int(next(it))
    
    coins = []
    for _ in range(n):
        coins.append(int(next(it)))
    
    memo = [-1 for _ in range(x + 1)]
    
    result = solve(x, coins, memo)
    print(result)

if __name__ == "__main__":
    main()
