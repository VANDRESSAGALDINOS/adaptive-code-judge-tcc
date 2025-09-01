#include <bits/stdc++.h>
using namespace std;

const int EXTRA_WORK = 2000; // Overhead intencional

int n;
vector<long long> weights;
long long total_sum;
long long ans;

void backtrack(int idx, long long sum1) {
    // OVERHEAD INTENCIONAL
    volatile int waste = 0;
    for (int k = 0; k < EXTRA_WORK; k++) {
        waste += (idx * sum1 + k) % 7;
    }
    
    if (idx == n) {
        long long sum2 = total_sum - sum1;
        ans = min(ans, abs(sum1 - sum2));
        return;
    }
    
    // Try adding current apple to group 1
    backtrack(idx + 1, sum1 + weights[idx]);
    
    // Try adding current apple to group 2 (equivalent to not adding to group 1)
    backtrack(idx + 1, sum1);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    cin >> n;
    weights.resize(n);
    total_sum = 0;
    
    for (int i = 0; i < n; i++) {
        cin >> weights[i];
        total_sum += weights[i];
    }
    
    ans = LLONG_MAX;
    backtrack(0, 0);
    
    cout << ans << "\n";
    
    return 0;
}
