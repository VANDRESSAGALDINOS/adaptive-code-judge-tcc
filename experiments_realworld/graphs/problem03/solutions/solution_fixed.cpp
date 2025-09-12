#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n, q;
    cin >> n >> q;
    
    vector<int> next(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> next[i];
    }
    
    // Binary lifting: up[i][j] = destination after 2^j steps from planet i
    const int LOG = 30; // log2(10^9) ≈ 30
    vector<vector<int>> up(n + 1, vector<int>(LOG));
    
    // Initialize: up[i][0] = next[i] (after 2^0 = 1 step)
    for (int i = 1; i <= n; i++) {
        up[i][0] = next[i];
    }
    
    // Fill binary lifting table: up[i][j] = up[up[i][j-1]][j-1]
    for (int j = 1; j < LOG; j++) {
        for (int i = 1; i <= n; i++) {
            up[i][j] = up[up[i][j-1]][j-1];
        }
    }
    
    // Process queries
    for (int i = 0; i < q; i++) {
        int x, k;
        cin >> x >> k;
        
        // Binary lifting: decompose k into powers of 2
        for (int j = 0; j < LOG; j++) {
            if (k & (1 << j)) {
                x = up[x][j];
            }
        }
        
        cout << x << "\n";
    }
    
    return 0;
}













