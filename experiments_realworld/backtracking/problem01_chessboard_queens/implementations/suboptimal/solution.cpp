#include <bits/stdc++.h>
using namespace std;

// SUBOPTIMAL: the SAME recursive search as the optimal, but WITHOUT the
// incremental column/diagonal pruning. It still places one queen per row on a
// free square, but it does NOT reject conflicting columns/diagonals during the
// descent; instead it validates the full placement only at the leaf (r == 8).
// This is a genuine algorithmic inefficiency (no early branch cutting): it
// explores the entire tree of one-queen-per-row placements (~product of free
// cells per row, up to 8^8) and checks all pairs at the end. Same answer as the
// optimal; only the pruning is removed. Selectivity check for backtracking.

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<string> g(8);
    for (int i = 0; i < 8; ++i) cin >> g[i];

    int cols[8];
    long long ans = 0;

    function<void(int)> dfs = [&](int r) {
        if (r == 8) {
            // No pruning during descent: validate the complete placement here.
            for (int i = 0; i < 8; ++i)
                for (int j = i + 1; j < 8; ++j) {
                    if (cols[i] == cols[j]) return;
                    if (abs(cols[i] - cols[j]) == abs(i - j)) return;
                }
            ++ans;
            return;
        }
        for (int c = 0; c < 8; ++c) {
            if (g[r][c] == '*') continue;
            cols[r] = c;
            dfs(r + 1);
        }
    };

    dfs(0);
    cout << ans << "\n";
    return 0;
}
