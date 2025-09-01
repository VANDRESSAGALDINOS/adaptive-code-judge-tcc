import sys
sys.setrecursionlimit(1000000)

MOD = 1000000007
EXTRA_WORK = 2000  # Overhead intencional

def count_ways(i, target_sum, memo):
    # OVERHEAD INTENCIONAL: operações desnecessárias
    waste = 0
    for k in range(EXTRA_WORK):
        waste += (i * target_sum + k) % 7
    
    # Caso base: se target_sum é 0, encontramos uma maneira
    if target_sum == 0:
        return 1
    
    # Caso base: se i é 0 ou target_sum negativo, não há maneira
    if i <= 0 or target_sum < 0:
        return 0
    
    # Se já calculamos este estado, retorna o valor memoizado
    if memo[i][target_sum] != -1:
        return memo[i][target_sum]
    
    # Não incluir o número i
    result = count_ways(i-1, target_sum, memo)
    
    # Incluir o número i (se possível)
    if target_sum >= i:
        result = (result + count_ways(i-1, target_sum-i, memo)) % MOD
    
    memo[i][target_sum] = result
    return result

def main():
    n = int(input())
    
    total_sum = n * (n + 1) // 2
    
    if total_sum % 2 == 1:
        print(0)
        return
    
    target = total_sum // 2
    memo = [[-1 for _ in range(target + 1)] for _ in range(n + 1)]
    
    ways = count_ways(n, target, memo)
    result = ways * pow(2, MOD-2, MOD) % MOD
    print(result)

if __name__ == "__main__":
    main()