#include <iostream>
#include <vector>
using namespace std;

const int MOD = 1000000007;
const int EXTRA_WORK = 200; // Overhead intencional para garantir TLE

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n, x;
    cin >> n >> x;
    
    vector<int> coins(n);
    for (int i = 0; i < n; i++) {
        cin >> coins[i];
    }
    
    // DP iterativo bottom-up com overhead intencional
    vector<int> dp(x + 1, 0);
    dp[0] = 1; // Caso base: uma maneira de formar soma 0
    
    // Para cada soma possível de 1 até x
    for (int sum = 1; sum <= x; sum++) {
        // Tentar usar cada moeda
        for (int i = 0; i < n; i++) {
            if (sum >= coins[i]) {
                dp[sum] = (dp[sum] + dp[sum - coins[i]]) % MOD;
                
                // OVERHEAD INTENCIONAL - trabalho desnecessário
                volatile int waste = 0;
                for (int k = 0; k < EXTRA_WORK; k++) {
                    waste += k * k;
                }
            }
        }
    }
    
    cout << dp[x] << "\n";
    
    return 0;
}












