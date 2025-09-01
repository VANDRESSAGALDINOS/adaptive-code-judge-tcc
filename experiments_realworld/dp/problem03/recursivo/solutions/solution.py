import sys
sys.setrecursionlimit(1000000)

MOD = 1000000007

def count_ways(i, target_sum, memo):
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
    
    # Soma total dos números 1 a n
    total_sum = n * (n + 1) // 2
    
    # Se a soma é ímpar, não é possível dividir em dois conjuntos iguais
    if total_sum % 2 == 1:
        print(0)
        return
    
    target = total_sum // 2
    
    # Inicializar memoização
    memo = [[-1 for _ in range(target + 1)] for _ in range(n + 1)]
    
    # Contar maneiras de formar target usando números 1 a n
    ways = count_ways(n, target, memo)
    
    # Como cada partição é contada duas vezes, dividimos por 2
    result = ways * pow(2, MOD-2, MOD) % MOD
    print(result)

if __name__ == "__main__":
    main()