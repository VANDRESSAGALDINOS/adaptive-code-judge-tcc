#include <iostream>
#include <vector>
#include <cstring>
using namespace std;

const int MOD = 1000000007;

int n, target;
int memo[501][125001]; // n até 500, target até 500*501/4 = 62625

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
    
    // Soma total dos números 1 a n
    int total_sum = n * (n + 1) / 2;
    
    // Se a soma é ímpar, não é possível dividir em dois conjuntos iguais
    if (total_sum % 2 == 1) {
        cout << 0 << "\n";
        return 0;
    }
    
    target = total_sum / 2;
    
    // Inicializar memoização
    memset(memo, -1, sizeof(memo));
    
    // Contar maneiras de formar target usando números 1 a n
    int ways = count_ways(n, target);
    
    // Como cada partição é contada duas vezes, dividimos por 2
    long long result = (1LL * ways * power(2, MOD-2, MOD)) % MOD;
    cout << result << "\n";
    
    return 0;
}