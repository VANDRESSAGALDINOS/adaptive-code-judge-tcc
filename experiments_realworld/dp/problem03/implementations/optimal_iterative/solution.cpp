#include <iostream>
#include <vector>
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

    // Rolling two-row DP (matches the Python optimal_iterative): prev = row i-1,
    // curr = row i; dp[j] = number of ways to form sum j using numbers 1..i.
    // O(target) space, vs the O(n*target) full 2D table -- both compute
    // dp[n][target] identically. The space-optimized form is the canonical
    // iterative optimal and keeps the cross-language pair (cpp <-> py) the same
    // algorithm, so beta measures only the language penalty.
    vector<long long> prev(target + 1, 0);
    vector<long long> curr(target + 1, 0);

    prev[0] = 1;

    for (int i = 1; i <= n; i++) {
        curr[0] = 1;
        for (int j = 1; j <= target; j++) {
            curr[j] = prev[j];
            if (j >= i) {
                curr[j] = (curr[j] + prev[j - i]) % MOD;
            }
        }
        swap(prev, curr);
    }

    long long ways = prev[target];
    long long result = (ways * power(2, MOD - 2, MOD)) % MOD;
    cout << result << "\n";

    return 0;
}
