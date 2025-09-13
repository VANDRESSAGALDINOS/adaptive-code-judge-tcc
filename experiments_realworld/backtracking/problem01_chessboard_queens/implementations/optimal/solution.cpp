#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<string> g(8);
    for (int i = 0; i < 8; ++i) cin >> g[i];

    bool col[8] = {}, d1[15] = {}, d2[15] = {};
    long long ans = 0;

    function<void(int)> dfs = [&](int r) {
        if (r == 8) {
            ++ans;
            return;
        }
        for (int c = 0; c < 8; ++c) {
            if (g[r][c] == '*') continue;
            int id1 = r + c, id2 = r - c + 7;
            if (col[c] || d1[id1] || d2[id2]) continue;
            col[c] = d1[id1] = d2[id2] = true;
            dfs(r + 1);
            col[c] = d1[id1] = d2[id2] = false;
        }
    };

    dfs(0);
    cout << ans << "\n";
    return 0;
}