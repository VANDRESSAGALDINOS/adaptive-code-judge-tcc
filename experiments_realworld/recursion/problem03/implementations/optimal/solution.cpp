#include <bits/stdc++.h>
using namespace std;

// RECURSIVE DFS rerooting (deep recursion), C++ counterpart of the Python version.
// For each node, the MAXIMUM distance to any other node. Two recursive passes:
//   dfs_down: down1[u] = longest downward path, down2[u] = second longest
//             downward path (through a DIFFERENT child); arg1[u] = the child
//             giving down1 (to exclude it for that child in the up pass).
//   dfs_up:   up[v] = 1 + max(up[u], best downward of u excluding branch v).
//   ans[u] = max(down1[u], up[u]).
// Same algorithm as the Python version; only the language differs.

int n;
vector<vector<int>> adj;
vector<int> down1, down2, arg1, up_;

void dfs_down(int u, int parent) {
    for (int v : adj[u]) {
        if (v != parent) {
            dfs_down(v, u);
            int cand = down1[v] + 1;
            if (cand > down1[u]) {
                down2[u] = down1[u];
                down1[u] = cand;
                arg1[u] = v;
            } else if (cand > down2[u]) {
                down2[u] = cand;
            }
        }
    }
}

void dfs_up(int u, int parent) {
    for (int v : adj[u]) {
        if (v != parent) {
            int best_excl = (arg1[u] == v) ? down2[u] : down1[u];
            up_[v] = max(up_[u], best_excl) + 1;
            dfs_up(v, u);
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    adj.assign(n + 1, {});
    for (int e = 0; e < n - 1; e++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    if (n == 1) {
        cout << 0 << "\n";
        return 0;
    }

    down1.assign(n + 1, 0);
    down2.assign(n + 1, 0);
    arg1.assign(n + 1, 0);
    up_.assign(n + 1, 0);

    dfs_down(1, 0);
    dfs_up(1, 0);

    for (int i = 1; i <= n; i++) {
        cout << max(down1[i], up_[i]);
        if (i < n) cout << " ";
    }
    cout << "\n";

    return 0;
}
