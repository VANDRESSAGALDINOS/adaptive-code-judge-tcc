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
    
    // SLOW VERSION: Naive simulation instead of binary lifting
    // This will be O(q * k) instead of O(q * log k)
    // For large k (up to 10^9), this becomes extremely slow
    
    const int EXTRA_WORK = 50; // Additional wasteful computation
    volatile long long waste = 0;
    
    for (int i = 0; i < q; i++) {
        int x, k;
        cin >> x >> k;
        
        // Naive approach: simulate k steps one by one
        for (int step = 0; step < k; step++) {
            x = next[x];
            
            // Add extra wasteful work to ensure TLE
            for (int extra = 0; extra < EXTRA_WORK; extra++) {
                waste += (long long)x * 1315423911LL ^ (long long)step * 2654435761LL;
                waste ^= (waste >> 16) + (waste << 8);
            }
        }
        
        cout << x << "\n";
    }
    
    // Prevent compiler from optimizing away waste
    asm volatile("" : : "r"(waste) : "memory");
    
    return 0;
}


