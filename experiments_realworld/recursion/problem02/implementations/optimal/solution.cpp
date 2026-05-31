#include <bits/stdc++.h>
using namespace std;

// RECURSIVE DFS + small-to-large merging, C++ counterpart of the Python version.
// For each node, the number of distinct colors in its subtree. The DFS returns
// (via a pointer to) a set of the subtree's colors; a parent merges each child's
// set into its own, always iterating the SMALLER set into the LARGER one
// (small-to-large) -> O(n log n) total. Same algorithm as the Python version;
// only the language differs. Used to confirm the language injustice (C++ AC vs
// Python TLE on the heavy cases).

int n;
vector<int> color;
vector<vector<int>> adj;
vector<int> ans;
vector<set<int>*> sub;   // sub[u] = set of colors in u's subtree

void dfs(int u, int parent) {
    set<int>* s = new set<int>();
    s->insert(color[u]);
    for (int v : adj[u]) {
        if (v != parent) {
            dfs(v, u);
            set<int>* cs = sub[v];
            // small-to-large: merge the smaller set into the larger
            if (cs->size() > s->size()) swap(s, cs);
            for (int x : *cs) s->insert(x);
            delete cs;
            sub[v] = nullptr;
        }
    }
    ans[u] = (int)s->size();
    sub[u] = s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    color.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> color[i];
    adj.assign(n + 1, {});
    ans.assign(n + 1, 0);
    sub.assign(n + 1, nullptr);

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
