// CSES 1197: Cycle Finding
// Bellman-Ford Negative Cycle Detection - O(nm)

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n, m;
    if (!(cin >> n >> m)) return 0;

    struct Edge {
        int a, b;
        long long c;
    };
    
    vector<Edge> edges(m);
    for (int i = 0; i < m; ++i) {
        cin >> edges[i].a >> edges[i].b >> edges[i].c;
    }

    vector<long long> dist(n + 1, 0);   // Implicit super-source
    vector<int> parent(n + 1, -1);

    int x = -1;
    
    // Bellman-Ford: n iterations of edge relaxation
    for (int i = 0; i < n; ++i) {
        x = -1;
        for (auto &e : edges) {
            if (dist[e.a] + e.c < dist[e.b]) {
                dist[e.b] = dist[e.a] + e.c;
                parent[e.b] = e.a;
                x = e.b;
            }
        }
    }

    if (x == -1) {
        cout << "NO\n";
        return 0;
    }

    // Find node guaranteed to be in negative cycle
    int y = x;
    for (int i = 0; i < n; ++i) {
        y = parent[y];
    }

    // Reconstruct cycle
    vector<int> cycle;
    for (int v = y;; v = parent[v]) {
        cycle.push_back(v);
        if (v == y && cycle.size() > 1) break;
    }
    reverse(cycle.begin(), cycle.end());

    cout << "YES\n";
    for (size_t i = 0; i < cycle.size(); ++i) {
        if (i) cout << ' ';
        cout << cycle[i];
    }
    cout << "\n";
    
    return 0;
}
