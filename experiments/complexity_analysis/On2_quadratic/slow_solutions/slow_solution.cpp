#include <iostream>
#include <vector>
using namespace std;

long long inefficientMatrixSum(const vector<vector<long long>>& matrix) {
    // Algorithmically equivalent but inefficient: O(n³) using redundant computations
    // Each element is accessed n times and averaged, maintaining mathematical equivalence
    long long sum = 0;
    int n = matrix.size();
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            long long element_contribution = 0;
            // Access current element n times (inefficient)
            for (int k = 0; k < n; k++) {
                element_contribution += matrix[i][j];
            }
            // Divide by n to get back original value
            sum += element_contribution / n;
        }
    }
    
    return sum;
}

int main() {
    int n;
    cin >> n;
    
    vector<vector<long long>> matrix(n, vector<long long>(n));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cin >> matrix[i][j];
        }
    }
    
    long long result = inefficientMatrixSum(matrix);
    cout << result << endl;
    
    return 0;
}
