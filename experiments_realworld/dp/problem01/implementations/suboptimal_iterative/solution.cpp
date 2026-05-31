#include <iostream>
#include <vector>
using namespace std;

const int MOD = 1000000007;

// SUBOPTIMAL (deliberately slowed, NOT a worse algorithm): the optimal bottom-up
// DP recomputed SLOW_FACTOR times. Same algorithm and same answer as the optimal
// iterative, just SLOW_FACTOR times slower. Selectivity check for the iterative
// style: a correct-but-too-slow submission that must be REJECTED (far slower than
// the optimal, beyond the adaptive limit). Same convention as graphs/problem01.
const int SLOW_FACTOR = 100;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, x;
    cin >> n >> x;

    vector<int> coins(n);
    for (int i = 0; i < n; i++) {
        cin >> coins[i];
    }

    // volatile sink: forces the compiler to keep every repetition (the result of
    // each pass is consumed), so the deliberate slowdown is not optimized away.
    volatile long long sink = 0;
    int answer = 0;
    for (int rep = 0; rep < SLOW_FACTOR; rep++) {
        vector<int> dp(x + 1, 0);
        dp[0] = 1;
        for (int s = 1; s <= x; s++) {
            for (int i = 0; i < n; i++) {
                if (s >= coins[i]) {
                    dp[s] = (dp[s] + dp[s - coins[i]]) % MOD;
                }
            }
        }
        answer = dp[x];
        sink += answer;
    }

    cout << answer << "\n";
    return 0;
}
