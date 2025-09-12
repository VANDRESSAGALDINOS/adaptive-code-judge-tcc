#include <iostream>
#include <vector>
using namespace std;

vector<vector<long long>> inefficientMatrixMultiply(const vector<vector<long long>>& A, const vector<vector<long long>>& B) {
    // Algorithmically equivalent but inefficient: O(n⁴) using redundant computations
    // Each dot product is computed n times and averaged, maintaining mathematical equivalence
    int n = A.size();
    vector<vector<long long>> C(n, vector<long long>(n, 0));
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            long long dot_product_sum = 0;
            // Compute dot product n times (inefficient)
            for (int repetition = 0; repetition < n; repetition++) {
                for (int k = 0; k < n; k++) {
                    dot_product_sum += A[i][k] * B[k][j];
                }
            }
            // Divide by n to get back original dot product
            C[i][j] = dot_product_sum / n;
        }
    }
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
    
    // Calculate C = A × B using inefficient approach
    vector<vector<long long>> C = inefficientMatrixMultiply(A, B);
    
    // Calculate sum of all elements in result matrix
    long long sum = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            sum += C[i][j];
        }
    }
    
    cout << sum << endl;
    
    return 0;
}
