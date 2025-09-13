#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

const int MOD = 1000000007;

int n, target;
int memo[501][125001];

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

int count_ways(int i, int target_sum) {
    if (target_sum == 0) {
        return 1;
    }
    if (i <= 0 || target_sum < 0) {
        return 0;
    }
    if (memo[i][target_sum] != -1) {
        return memo[i][target_sum];
    }
    
    int result = count_ways(i-1, target_sum);
    if (target_sum >= i) {
        result = (result + count_ways(i-1, target_sum-i)) % MOD;
    }
    
    return memo[i][target_sum] = result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    cin >> n;
    
    int total_sum = n * (n + 1) / 2;
    
    if (total_sum % 2 == 1) {
        cout << 0 << "\n";
        return 0;
    }
    
    target = total_sum / 2;
    memset(memo, -1, sizeof(memo));
    
    int ways = count_ways(n, target);
    long long result = (1LL * ways * power(2, MOD-2, MOD)) % MOD;
    cout << result << "\n";
    
    return 0;
}