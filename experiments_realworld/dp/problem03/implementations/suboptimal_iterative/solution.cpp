#include <iostream>
#include <vector>
using namespace std;

const int MOD = 1000000007;

// SUBOPTIMAL (deliberately slowed, NOT a worse algorithm): the optimal bottom-up
// DP (rolling two-row, O(n*target)) recomputed SLOW_FACTOR times. Same algorithm
// and same answer as the optimal iterative, just SLOW_FACTOR times slower.
// Selectivity check for the iterative style: a correct-but-too-slow submission
// that must be REJECTED (far slower than the optimal, beyond the adaptive limit).
// Same convention as graphs/problem01 and dp/problem01-02.
const int SLOW_FACTOR = 100;

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

    // volatile sink: forces the compiler to keep every repetition (the result of
    // each pass is consumed), so the deliberate slowdown is not optimized away.
    volatile long long sink = 0;
    long long ways = 0;
    for (int rep = 0; rep < SLOW_FACTOR; rep++) {
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
        ways = prev[target];
        sink += ways;
    }

    long long result = (ways * power(2, MOD - 2, MOD)) % MOD;
    cout << result << "\n";

    return 0;
}
