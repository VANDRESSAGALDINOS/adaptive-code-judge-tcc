#include <iostream>
#include <vector>
#include <string>
using namespace std;

const int MOD = 1000000007;

// SUBOPTIMAL (deliberately slowed, NOT a worse algorithm): the optimal bottom-up
// DP recomputed SLOW_FACTOR times. Same algorithm and same answer as the optimal
// iterative, just SLOW_FACTOR times slower. Selectivity check for the iterative
// style: a correct-but-too-slow submission that must be REJECTED. Same convention
// as graphs/problem01 and dp/problem01.
// NOTE: SLOW_FACTOR=100 was already ENOUGH for Python on CSES (TLE on {6,7,8,9,10})
// but NOT for C++ (ACCEPTED 15/15, max 0.96s) -- the language gap is so wide that a
// 100x-slowed iterative C++ still passes while a correct recursive Python TLEs.
// Raised to 300 so the C++ side is also rejected (clean selectivity for the
// iterative style in BOTH languages). See anotacoes_para_artigo.md.
const int SLOW_FACTOR = 300;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<string> grid(n);
    for (int i = 0; i < n; i++) {
        cin >> grid[i];
    }

    // volatile sink: forces the compiler to keep every repetition (the result of
    // each pass is consumed), so the deliberate slowdown is not optimized away.
    volatile long long sink = 0;
    int answer = 0;
    for (int rep = 0; rep < SLOW_FACTOR; rep++) {
        vector<vector<int>> dp(n, vector<int>(n, 0));
        if (grid[0][0] != '*') {
            dp[0][0] = 1;
        }
        for (int j = 1; j < n; j++) {
            if (grid[0][j] != '*') {
                dp[0][j] = dp[0][j-1];
            }
        }
        for (int i = 1; i < n; i++) {
            if (grid[i][0] != '*') {
                dp[i][0] = dp[i-1][0];
            }
        }
        for (int i = 1; i < n; i++) {
            for (int j = 1; j < n; j++) {
                if (grid[i][j] != '*') {
                    dp[i][j] = (dp[i-1][j] + dp[i][j-1]) % MOD;
                }
            }
        }
        answer = dp[n-1][n-1];
        sink += answer;
    }

    cout << answer << "\n";
    return 0;
}
