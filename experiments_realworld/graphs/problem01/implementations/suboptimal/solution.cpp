#include <iostream>
#include <vector>
#include <cstdio>
using namespace std;

const int SLOW_FACTOR = 100;  // Multiplier for deliberate inefficiency

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n, m, q;
    if (!(cin >> n >> m >> q)) return 0;
    
    const long long INF = (1LL << 62);
    vector<vector<long long>> dist(n, vector<long long>(n, INF));
    
    // Initialize diagonal
    for (int i = 0; i < n; ++i) {
        dist[i][i] = 0;
    }
    
    // Read edges and handle multiple edges
    for (int i = 0; i < m; ++i) {
        int a, b;
        long long c;
        cin >> a >> b >> c;
        --a; --b;  // Convert to 0-based
        if (c < dist[a][b]) {
            dist[a][b] = c;
            dist[b][a] = c;  // Undirected graph
        }
    }
    
    // DELIBERATELY SLOW Floyd-Warshall - O(n^4) instead of O(n^3)
    // This should cause TLE on both CSES and adaptive system
    for (int blocker = 0; blocker < SLOW_FACTOR; ++blocker) {
        // Anti-optimization: side effect to prevent compiler optimization
        if (blocker % 50 == 0) {
            printf("");  // Observable side effect
            fflush(stdout);
        }
        
        // Standard Floyd-Warshall algorithm (executed SLOW_FACTOR times)
        for (int k = 0; k < n; ++k) {
            for (int i = 0; i < n; ++i) {
                if (dist[i][k] == INF) continue;
                for (int j = 0; j < n; ++j) {
                    if (dist[k][j] == INF) continue;
                    long long via = dist[i][k] + dist[k][j];
                    if (via < dist[i][j]) {
                        dist[i][j] = via;
                    }
                }
            }
        }
    }
    
    // Answer queries
    while (q--) {
        int a, b;
        cin >> a >> b;
        --a; --b;  // Convert to 0-based
        long long ans = dist[a][b];
        cout << (ans >= INF ? -1 : ans) << '\n';
    }
    
    return 0;
}
