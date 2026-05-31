#include <iostream>
#include <vector>
#include <string>
using namespace std;

const int MOD = 1000000007;

int n;
vector<string> grid;

// SUBOPTIMAL: naive top-down recursion WITHOUT memoization.
// Same recurrence as the optimal recursive (paths(i,j) = paths(i,j+1) +
// paths(i+1,j)), but recomputes overlapping subproblems -> exponential in the
// number of paths, while the memoized/iterative optimal is O(n^2). Computes the
// same value. Recursion depth is the same as the optimal (O(n)).
int solve(int i, int j) {
    if (i >= n || j >= n || grid[i][j] == '*') return 0;
    if (i == n-1 && j == n-1) return 1;
    return (solve(i, j+1) + solve(i+1, j)) % MOD;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    grid.resize(n);

    for (int i = 0; i < n; i++) {
        cin >> grid[i];
    }

    cout << solve(0, 0) << "\n";

    return 0;
}
