#include <iostream>
#include <vector>
#include <string>
#include <cstring>
using namespace std;

const int MOD = 1000000007;

int n;
vector<string> grid;
int memo[1001][1001];

int solve(int i, int j) {
    // Fora dos limites ou trap
    if (i >= n || j >= n || grid[i][j] == '*') {
        return 0;
    }
    
    // Chegou ao destino
    if (i == n-1 && j == n-1) {
        return 1;
    }
    
    // Se já calculamos este estado, retorna o valor memoizado
    if (memo[i][j] != -1) {
        return memo[i][j];
    }
    
    // Calcula o número de caminhos: direita + baixo
    int result = 0;
    result = (result + solve(i, j+1)) % MOD; // direita
    result = (result + solve(i+1, j)) % MOD; // baixo
    
    return memo[i][j] = result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    cin >> n;
    grid.resize(n);
    
    for (int i = 0; i < n; i++) {
        cin >> grid[i];
    }
    
    // Inicializar memoização com -1
    memset(memo, -1, sizeof(memo));
    
    cout << solve(0, 0) << "\n";
    
    return 0;
}




