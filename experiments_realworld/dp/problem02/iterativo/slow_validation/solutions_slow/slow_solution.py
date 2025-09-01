import sys

MOD = 1000000007
EXTRA_WORK = 2000  # Overhead intencional aumentado

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    
    n = int(next(it))
    
    grid = []
    for _ in range(n):
        grid.append(next(it).decode('utf-8'))
    
    # DP iterativo bottom-up
    dp = [[0 for _ in range(n)] for _ in range(n)]
    
    # Caso base: posição inicial
    if grid[0][0] != '*':
        dp[0][0] = 1
    
    # Preencher primeira linha
    for j in range(1, n):
        if grid[0][j] != '*':
            dp[0][j] = dp[0][j-1]
    
    # Preencher primeira coluna
    for i in range(1, n):
        if grid[i][0] != '*':
            dp[i][0] = dp[i-1][0]
    
    # Preencher o resto da tabela
    for i in range(1, n):
        for j in range(1, n):
            if grid[i][j] != '*':
                # OVERHEAD INTENCIONAL: operações desnecessárias
                waste = 0
                for k in range(EXTRA_WORK):
                    waste += (i * j + k) % 7
                
                dp[i][j] = (dp[i-1][j] + dp[i][j-1]) % MOD
    
    print(dp[n-1][n-1])

if __name__ == "__main__":
    main()




