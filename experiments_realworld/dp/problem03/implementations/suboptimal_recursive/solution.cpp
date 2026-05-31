#include <iostream>
using namespace std;

const int MOD = 1000000007;

int n, target;

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

// SUBOPTIMAL: naive top-down recursion WITHOUT memoization.
// Same recurrence as the optimal recursive (count_ways(i,t) = count_ways(i-1,t)
// + count_ways(i-1,t-i)), but recomputes overlapping subproblems -> exponential
// (~2^n nodes), while the memoized optimal is O(n*target). Computes the same
// value. Recursion depth is the same as the optimal (O(n)); only the branching
// (no memo) makes it blow up -- genuine algorithmic inefficiency, not a slowdown.
int count_ways(int i, int target_sum) {
    if (target_sum == 0) {
        return 1;
    }
    if (i <= 0 || target_sum < 0) {
        return 0;
    }
    int result = count_ways(i-1, target_sum);
    if (target_sum >= i) {
        result = (result + count_ways(i-1, target_sum-i)) % MOD;
    }
    return result;
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

    int ways = count_ways(n, target);
    long long result = (1LL * ways * power(2, MOD - 2, MOD)) % MOD;
    cout << result << "\n";

    return 0;
}
