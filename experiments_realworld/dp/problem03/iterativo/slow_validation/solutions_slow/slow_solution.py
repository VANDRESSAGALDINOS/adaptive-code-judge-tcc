MOD = 1000000007
EXTRA_WORK = 2000  # Overhead intencional

def main():
    n = int(input())
    
    # Soma total dos números 1 a n
    total_sum = n * (n + 1) // 2
    
    # Se a soma é ímpar, não é possível dividir em dois conjuntos iguais
    if total_sum % 2 == 1:
        print(0)
        return
    
    target = total_sum // 2
    
    # DP iterativo: dp[i][j] = número de maneiras de formar soma j usando números 1 a i
    # Otimização de espaço: usar apenas duas linhas (anterior e atual)
    prev = [0] * (target + 1)
    curr = [0] * (target + 1)
    
    # Caso base: sempre há 1 maneira de formar soma 0 (conjunto vazio)
    prev[0] = 1
    
    # Preenchimento bottom-up com overhead intencional
    for i in range(1, n + 1):
        curr[0] = 1  # Sempre 1 maneira de formar soma 0
        
        for j in range(1, target + 1):
            # OVERHEAD INTENCIONAL: operações desnecessárias
            waste = 0
            for k in range(EXTRA_WORK):
                waste += (i * j + k) % 7
            
            # Não incluir o número i
            curr[j] = prev[j]
            
            # Incluir o número i (se possível)
            if j >= i:
                curr[j] = (curr[j] + prev[j - i]) % MOD
        
        # Trocar as linhas para a próxima iteração
        prev, curr = curr, prev
    
    # Contar maneiras de formar target usando números 1 a n
    ways = prev[target]
    
    # Como cada partição é contada duas vezes, dividimos por 2
    result = ways * pow(2, MOD-2, MOD) % MOD
    print(result)

if __name__ == "__main__":
    main()
