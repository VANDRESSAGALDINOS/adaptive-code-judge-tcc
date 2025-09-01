#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

const int MOD = 1000000007;

int n, x;
vector<int> coins;
int memo[1000001];

int solve(int remaining) {
    // Caso base: se remaining == 0, encontramos uma maneira
    if (remaining == 0) return 1;
    
    // Se remaining < 0, não há solução
    if (remaining < 0) return 0;
    
    // Se já calculamos este estado, retorna o valor memoizado
    if (memo[remaining] != -1) return memo[remaining];
    
    int result = 0;
    
    // Tentar usar cada moeda
    for (int i = 0; i < n; i++) {
        if (remaining >= coins[i]) {
            result = (result + solve(remaining - coins[i])) % MOD;
        }
    }
    
    return memo[remaining] = result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    cin >> n >> x;
    coins.resize(n);
    
    for (int i = 0; i < n; i++) {
        cin >> coins[i];
    }
    
    // Inicializar memoização com -1
    memset(memo, -1, sizeof(memo));
    
    cout << solve(x) << "\n";
    
    return 0;
}
