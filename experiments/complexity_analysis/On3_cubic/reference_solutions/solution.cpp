#include <iostream>
#include <vector>
using namespace std;

vector<vector<long long>> matrixMultiply(const vector<vector<long long>>& A, const vector<vector<long long>>& B) {
    // O(n³) cubic time: standard matrix multiplication algorithm
    int n = A.size();
    vector<vector<long long>> C(n, vector<long long>(n, 0));
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
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
    
    // Calculate C = A × B using optimal O(n³) approach
    vector<vector<long long>> C = matrixMultiply(A, B);
    
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
