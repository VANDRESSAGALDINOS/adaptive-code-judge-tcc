import sys
sys.setrecursionlimit(2000000)  # Para suportar recursão profunda em grids grandes

MOD = 1000000007

def solve(i, j, grid, memo, n):
    # Fora dos limites ou trap
    if i >= n or j >= n or grid[i][j] == '*':
        return 0
    
    # Chegou ao destino
    if i == n-1 and j == n-1:
        return 1
    
    # Se já calculamos este estado, retorna o valor memoizado
    if memo[i][j] != -1:
        return memo[i][j]
    
    # Calcula o número de caminhos: direita + baixo
    result = 0
    result = (result + solve(i, j+1, grid, memo, n)) % MOD  # direita
    result = (result + solve(i+1, j, grid, memo, n)) % MOD  # baixo
    
    memo[i][j] = result
    return result

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    
    n = int(next(it))
    
    grid = []
    for _ in range(n):
        grid.append(next(it).decode('utf-8'))
    
    # Inicializar memoização com -1
    memo = [[-1 for _ in range(n)] for _ in range(n)]
    
    result = solve(0, 0, grid, memo, n)
    print(result)

if __name__ == "__main__":
    main()




