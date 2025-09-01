#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

const int MOD = 1000000007;
const int EXTRA_WORK = 2000;  // Overhead intencional

long long power(long long base, long long exp, long long mod) {
    long long result = 1;
    while (exp > 0) {
        if (exp % 2 == 1) {
            result = (result * base) % mod;
        }
        base = (base * base) % mod;
        exp /= 2;
    }
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n;
    cin >> n;
    
    // Soma total dos números 1 a n
    int total_sum = n * (n + 1) / 2;
    
    // Se a soma é ímpar, não é possível dividir em dois conjuntos iguais
    if (total_sum % 2 == 1) {
        cout << 0 << "\n";
        return 0;
    }
    
    int target = total_sum / 2;
    
    // DP iterativo: dp[i][j] = número de maneiras de formar soma j usando números 1 a i
    vector<vector<long long>> dp(n + 1, vector<long long>(target + 1, 0));
    
    // Caso base: sempre há 1 maneira de formar soma 0 (conjunto vazio)
    for (int i = 0; i <= n; i++) {
        dp[i][0] = 1;
    }
    
    // Preenchimento bottom-up com overhead intencional
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j <= target; j++) {
            // OVERHEAD INTENCIONAL: operações desnecessárias
            volatile int waste = 0;
            for (int k = 0; k < EXTRA_WORK; k++) {
                waste += (i * j + k) % 7;
            }
            
            // Não incluir o número i
            dp[i][j] = dp[i-1][j];
            
            // Incluir o número i (se possível)
            if (j >= i) {
                dp[i][j] = (dp[i][j] + dp[i-1][j-i]) % MOD;
            }
        }
    }
    
    // Contar maneiras de formar target usando números 1 a n
    long long ways = dp[n][target];
    
    // Como cada partição é contada duas vezes, dividimos por 2
    long long result = (ways * power(2, MOD-2, MOD)) % MOD;
    cout << result << "\n";
    
    return 0;
}
