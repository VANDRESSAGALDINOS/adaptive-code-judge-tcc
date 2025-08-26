// C++ Reference Solution - CSES 1672: Shortest Routes II
// Algorithmically equivalent to Python solution (see formal_proof.md)
// Floyd-Warshall All-Pairs Shortest Path - O(n³)

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, q;
    if (!(cin >> n >> m >> q)) return 0;

    const long long INF = (1LL<<62);
    vector<vector<long long>> dist(n, vector<long long>(n, INF));
    for (int i = 0; i < n; ++i) dist[i][i] = 0;

    for (int i = 0; i < m; ++i) {
        int a, b; long long c;
        cin >> a >> b >> c;
        --a; --b;
        if (c < dist[a][b]) {
            dist[a][b] = c;
            dist[b][a] = c; // undirected graph
        }
    }

    // Floyd–Warshall with INF check to avoid overflow
    for (int k = 0; k < n; ++k) {
        for (int i = 0; i < n; ++i) {
            if (dist[i][k] == INF) continue;
            for (int j = 0; j < n; ++j) {
                if (dist[k][j] == INF) continue;
                long long via = dist[i][k] + dist[k][j];
                if (via < dist[i][j]) dist[i][j] = via;
            }
        }
    }

    while (q--) {
        int a, b; cin >> a >> b; --a; --b;
        long long ans = dist[a][b];
        cout << (ans >= INF ? -1 : ans) << '\n';
    }
    return 0;
}
