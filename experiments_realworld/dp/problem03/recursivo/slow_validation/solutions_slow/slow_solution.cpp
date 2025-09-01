#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

const int MOD = 1000000007;
const int EXTRA_WORK = 2000;  // Overhead intencional

int n, target;
int memo[501][125001];

long long power(long long base, long long exp, long long mod) {
    long long result = 1;
    while (exp > 0) {
        if (exp % 2 == 1) {
            result = (result * base) % mod;
        }
        base = (base * base) % mod;
        exp /= 2;
    }
    return result;
}

int count_ways(int i, int target_sum) {
    // OVERHEAD INTENCIONAL: operações desnecessárias
    volatile int waste = 0;
    for (int k = 0; k < EXTRA_WORK; k++) {
        waste += (i * target_sum + k) % 7;
    }
    
    // Caso base: se target_sum é 0, encontramos uma maneira
    if (target_sum == 0) {
        return 1;
    }
    
    // Caso base: se i é 0 ou target_sum negativo, não há maneira
    if (i <= 0 || target_sum < 0) {
        return 0;
    }
    
    // Se já calculamos este estado, retorna o valor memoizado
    if (memo[i][target_sum] != -1) {
        return memo[i][target_sum];
    }
    
    // Não incluir o número i
    int result = count_ways(i-1, target_sum);
    
    // Incluir o número i (se possível)
    if (target_sum >= i) {
        result = (result + count_ways(i-1, target_sum-i)) % MOD;
    }
    
    return memo[i][target_sum] = result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    cin >> n;
    
    int total_sum = n * (n + 1) / 2;
    
    if (total_sum % 2 == 1) {
        cout << 0 << "\n";
        return 0;
    }
    
    target = total_sum / 2;
    memset(memo, -1, sizeof(memo));
    
    int ways = count_ways(n, target);
    long long result = (1LL * ways * power(2, MOD-2, MOD)) % MOD;
    cout << result << "\n";
    
    return 0;
}