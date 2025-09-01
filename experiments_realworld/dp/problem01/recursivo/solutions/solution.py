import sys
sys.setrecursionlimit(1100000)  # Aumentar para suportar x até 10^6

MOD = 1000000007

def solve(remaining, coins, memo):
    # Caso base: se remaining == 0, encontramos uma maneira
    if remaining == 0:
        return 1
    
    # Se remaining < 0, não há solução
    if remaining < 0:
        return 0
    
    # Se já calculamos este estado, retorna o valor memoizado
    if memo[remaining] != -1:
        return memo[remaining]
    
    result = 0
    
    # Tentar usar cada moeda
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
    
    # Inicializar memoização com -1
    memo = [-1 for _ in range(x + 1)]
    
    result = solve(x, coins, memo)
    print(result)

if __name__ == "__main__":
    main()
