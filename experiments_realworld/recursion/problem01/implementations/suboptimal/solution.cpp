#include <bits/stdc++.h>
using namespace std;

// SUBOPTIMAL: naive O(n^2) instead of the O(n) rerooting. For EACH node we run a
// separate recursive DFS that sums the distances from that node to all others.
// Same recursive DFS shape and the same answer as the optimal, but without the
// rerooting trick -> the total work is O(n^2) (n independent DFS traversals).
// Genuine algorithmic inefficiency (worse complexity, not a fake slowdown).
// Selectivity check: a correct-but-too-slow submission that must be REJECTED even
// under the adaptive limit.

int n;
vector<vector<int>> adj;

long long dfs(int u, int parent, long long depth) {
    long long total = depth;
    for (int v : adj[u]) {
        if (v != parent) {
            total += dfs(v, u, depth + 1);
        }
    }
    return total;
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

    for (int s = 1; s <= n; s++) {
        cout << dfs(s, 0, 0);
        if (s < n) cout << " ";
    }
    cout << "\n";

    return 0;
}
