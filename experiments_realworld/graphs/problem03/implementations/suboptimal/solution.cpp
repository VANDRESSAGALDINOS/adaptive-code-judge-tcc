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
    
    // SUBOPTIMAL: naive O(q*k) simulation instead of O(q*log k) binary lifting.
    // Walks the k teleporters one by one; for large k (up to 10^9) this is far
    // slower than the optimal, while computing the same answer.
    for (int i = 0; i < q; i++) {
        int x, k;
        cin >> x >> k;
        for (int step = 0; step < k; step++) {
            x = next[x];
        }
        cout << x << "\n";
    }

    return 0;
}


