#include <bits/stdc++.h>
using namespace std;

// SUBOPTIMAL: the SAME recursive DFS as the optimal, but WITHOUT small-to-large.
// It always merges the CHILD's set into the PARENT's set (never swapping the
// smaller into the larger). Same answer as the optimal, but the merge work is no
// longer bounded: on a chain (each node a distinct color) the accumulated set is
// carried up and re-copied at every level -> O(n^2) in the worst case, vs the
// optimal's O(n log n). Genuine algorithmic inefficiency (worse complexity, not a
// fake slowdown). Selectivity check: a correct-but-too-slow submission that must
// be REJECTED even under the adaptive limit.

int n;
vector<int> color;
vector<vector<int>> adj;
vector<int> ans;

set<int> dfs(int u, int parent) {
    set<int> s;
    s.insert(color[u]);
    for (int v : adj[u]) {
        if (v != parent) {
            set<int> cs = dfs(v, u);
            // NAIVE merge: always child-into-parent, NO small-to-large.
            for (int x : cs) s.insert(x);
        }
    }
    ans[u] = (int)s.size();
    return s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    color.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> color[i];
    adj.assign(n + 1, {});
    ans.assign(n + 1, 0);

    for (int e = 0; e < n - 1; e++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    dfs(1, 0);

    for (int i = 1; i <= n; i++) {
        cout << ans[i];
        if (i < n) cout << " ";
    }
    cout << "\n";

    return 0;
}
