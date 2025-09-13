#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

const int MOD = 1000000007;

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
    
    int total_sum = n * (n + 1) / 2;
    
    if (total_sum % 2 == 1) {
        cout << 0 << "\n";
        return 0;
    }
    
    int target = total_sum / 2;
    vector<vector<long long>> dp(n + 1, vector<long long>(target + 1, 0));
    
    for (int i = 0; i <= n; i++) {
        dp[i][0] = 1;
    }
    
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j <= target; j++) {
            dp[i][j] = dp[i-1][j];
            if (j >= i) {
                dp[i][j] = (dp[i][j] + dp[i-1][j-i]) % MOD;
            }
        }
    }
    
    long long ways = dp[n][target];
    long long result = (ways * power(2, MOD-2, MOD)) % MOD;
    cout << result << "\n";
    
    return 0;
}
