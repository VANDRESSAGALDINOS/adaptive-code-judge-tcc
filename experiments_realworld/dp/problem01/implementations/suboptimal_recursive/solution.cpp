#include <iostream>
#include <vector>
using namespace std;

const int MOD = 1000000007;

int n, x;
vector<int> coins;

// SUBOPTIMAL: naive top-down recursion WITHOUT memoization.
// Same recurrence as the optimal (ways(s) = sum over coins of ways(s-coin)),
// but recomputes overlapping subproblems -> exponential in the answer size,
// while the memoized/iterative optimal is O(x*n). Computes the same value.
int solve(int remaining) {
    if (remaining == 0) return 1;
    if (remaining < 0) return 0;

    int result = 0;
    for (int i = 0; i < n; i++) {
        if (remaining >= coins[i]) {
            result = (result + solve(remaining - coins[i])) % MOD;
        }
    }
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> x;
    coins.resize(n);

    for (int i = 0; i < n; i++) {
        cin >> coins[i];
    }

    cout << solve(x) << "\n";

    return 0;
}
