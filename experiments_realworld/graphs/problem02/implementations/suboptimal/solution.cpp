// CSES 1197: Cycle Finding - Suboptimal Implementation
// Includes artificial computational overhead for TLE validation

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct Edge {
    int a, b;
    long long w;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;

    vector<Edge> edges(m);
    for (int i = 0; i < m; ++i) {
        int a, b; 
        long long c;
        cin >> a >> b >> c;
        edges[i] = {a, b, c};
    }

    // Bellman-Ford with implicit super-source
    vector<long long> dist(n + 1, 0);
    vector<int> parent(n + 1, -1);

    int x = -1;

    // Volatile to prevent compiler optimizations
    volatile long long waste = 0;

    // Extra passes for artificial slowdown (increased for stronger TLE)
    const int EXTRA_PASSES = 150;

    for (int it = 0; it < n; ++it) {
        x = -1;

        // 1) Real relaxation pass
        for (const auto &e : edges) {
            long long nd = dist[e.a] + e.w;
            if (nd < dist[e.b]) {
                dist[e.b] = nd;
                parent[e.b] = e.a;
                x = e.b;
            }
        }

        // 2) Artificial extra work to consume time
        for (int rep = 0; rep < EXTRA_PASSES; ++rep) {
            for (const auto &e : edges) {
                // Cheap arithmetic operations to ensure work
                waste += ((long long)e.a * 1315423911LL
                           ^ (long long)e.b * 2654435761LL
                           ^ (e.w & 0xFFFF));
                // Memory access to prevent dead-code elimination
                waste ^= (dist[e.a] & 0xFF) + (dist[e.b] & 0x7F);
            }
        }
    }

    if (x == -1) {
        cout << "NO\n";
        return 0;
    }

    // Find node in cycle
    int y = x;
    for (int i = 0; i < n; ++i) y = parent[y];

    // Reconstruct and print closed cycle
    vector<int> cyc;
    int v = y;
    while (true) {
        cyc.push_back(v);
        v = parent[v];
        if (v == y) {
            cyc.push_back(v); // Close cycle
            break;
        }
    }
    reverse(cyc.begin(), cyc.end());

    cout << "YES\n";
    for (size_t i = 0; i < cyc.size(); ++i) {
        if (i) cout << ' ';
        cout << cyc[i];
    }
    cout << '\n';

    // Prevent compiler from optimizing away waste variable
    asm volatile("" : : "r"(waste) : "memory");
    return 0;
}

// Reference: https://cses.fi/paste/6368f44720cc7cb3db2370/
