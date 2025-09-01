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
    
    # Trabalho extra para tornar lento
    EXTRA_WORK = 150
    waste = 0
    
    for coin in coins:
        if remaining >= coin:
            result = (result + solve(remaining - coin, coins, memo)) % MOD
            
            # Trabalho artificial extra para garantir TLE
            for rep in range(EXTRA_WORK):
                waste += remaining * 1315423911 ^ coin * 2654435761
                waste ^= (waste >> 16) + (waste << 8)
                waste &= 0xFFFFFFFFFFFFFFFF  # Keep as 64-bit
                
                # Forçar acesso à memória para evitar otimização
                waste ^= (memo[remaining % len(memo)] + coin) & 0xFFFF
    
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
