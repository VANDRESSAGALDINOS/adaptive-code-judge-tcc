#include <iostream>
#include <vector>
#include <cstring>
#include <cstdio>
using namespace std;

const int MOD = 1000000007;

int n, x;
vector<int> coins;
int memo[1000001];

// Slow version: adicionar trabalho extra para garantir TLE
int solve(int remaining) {
    if (remaining == 0) return 1;
    if (remaining < 0) return 0;
    if (memo[remaining] != -1) return memo[remaining];
    
    int result = 0;
    
    // Trabalho extra para tornar lento
    const int EXTRA_WORK = 150;
    volatile long long waste = 0;
    
    for (int i = 0; i < n; i++) {
        if (remaining >= coins[i]) {
            result = (result + solve(remaining - coins[i])) % MOD;
            
            // Trabalho artificial extra para garantir TLE
            for (int rep = 0; rep < EXTRA_WORK; rep++) {
                waste += (long long)remaining * 1315423911LL ^ (long long)coins[i] * 2654435761LL;
                waste ^= (waste >> 16) + (waste << 8);
                
                // Forçar acesso à memória para evitar otimização
                waste ^= (memo[remaining % 1000] + coins[i % n]) & 0xFFFF;
            }
        }
    }
    
    // Usar waste para evitar otimização do compilador
    asm volatile("" : : "r"(waste) : "memory");
    
    return memo[remaining] = result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    cin >> n >> x;
    coins.resize(n);
    
    for (int i = 0; i < n; i++) {
        cin >> coins[i];
    }
    
    memset(memo, -1, sizeof(memo));
    cout << solve(x) << "\n";
    
    return 0;
}
