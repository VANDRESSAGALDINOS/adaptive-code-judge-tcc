#include <iostream>
#include <vector>
using namespace std;

vector<vector<long long>> quarticMultiply(const vector<vector<long long>>& A, const vector<vector<long long>>& B) {
    // Intentionally slow: O(n⁴) quartic time instead of O(n³) cubic
    // Use side effects that compiler CANNOT optimize away
    int n = A.size();
    vector<vector<long long>> C(n, vector<long long>(n, 0));
    long long debug_counter = 0;
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                // O(n⁴) extra nested loop that GCC cannot remove due to printf
                for (int l = 0; l < n; l++) {
                    debug_counter++;
                    // Side effect: printf forces execution - compiler cannot optimize away
                    if (debug_counter % 50000 == 0) {
                        printf("DEBUG: processed %lld operations\n", debug_counter);
                        fflush(stdout);  // Ensure immediate output
                    }
                }
                // Do the actual matrix multiplication work
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
    
    // Final debug info - ensures all loops were executed
    printf("TOTAL_OPS: %lld\n", debug_counter);
    return C;
}

int main() {
    int n;
    cin >> n;
    
    // Read matrix A
    vector<vector<long long>> A(n, vector<long long>(n));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cin >> A[i][j];
        }
    }
    
    // Read matrix B
    vector<vector<long long>> B(n, vector<long long>(n));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cin >> B[i][j];
        }
    }
    
    // Use inefficient quartic multiplication
    vector<vector<long long>> C = quarticMultiply(A, B);
    
    // Calculate sum of all elements in result matrix
    long long sum = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            sum += C[i][j];
        }
    }
    
    // Output sum
    cout << sum << endl;
    
    return 0;
}
