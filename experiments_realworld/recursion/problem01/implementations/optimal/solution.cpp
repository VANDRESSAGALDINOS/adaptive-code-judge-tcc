#include <bits/stdc++.h>
using namespace std;

// RECURSIVE DFS rerooting (deep recursion), C++ counterpart of the Python
// reference. For each node, the sum of distances to all other nodes, via two
// recursive passes:
//   dfs1 (post-order): subtree size cnt[u] and res[1] = sum of depths from root.
//   dfs2 (pre-order):  reroot, res[v] = res[u] + (n - cnt[v]) - cnt[v].
// Same algorithm as the Python version; only the language differs. Used to
// confirm the language injustice: C++ AC vs Python TLE on the heavy cases.

int n;
vector<vector<int>> adj;
vector<long long> cnt, res;

void dfs1(int u, int parent, long long depth) {
    res[1] += depth;
    cnt[u] = 1;
    for (int v : adj[u]) {
        if (v != parent) {
            dfs1(v, u, depth + 1);
            cnt[u] += cnt[v];
        }
    }
}

void dfs2(int u, int parent) {
    for (int v : adj[u]) {
        if (v != parent) {
            res[v] = res[u] + (long long)(n - cnt[v]) - cnt[v];
            dfs2(v, u);
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    adj.assign(n + 1, {});
    cnt.assign(n + 1, 0);
    res.assign(n + 1, 0);

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

    dfs1(1, 0, 0);
    dfs2(1, 0);

    for (int i = 1; i <= n; i++) {
        cout << res[i];
        if (i < n) cout << " ";
    }
    cout << "\n";
    return 0;
}
