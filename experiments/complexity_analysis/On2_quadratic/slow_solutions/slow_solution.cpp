#include <iostream>
#include <vector>
using namespace std;

long long inefficientMatrixSum(const vector<vector<long long>>& matrix) {
    // Algorithmically equivalent but inefficient: O(n^3) using redundant computations.
    // Each element is accessed n times and averaged, maintaining mathematical equivalence.
    // ANTI-OPTIMIZATION (language-specific, C++ only): the innermost loop adds a value
    // constant in k, which -O2 strength-reduces to a single multiply (collapsing
    // O(n^3) -> O(n^2)). A volatile sink written every iteration is an observable side
    // effect the compiler may not elide, forcing all n^3 iterations. Output is unchanged
    // (the sink is never read back). Python needs no sink.
    volatile long long sink = 0;
    long long sum = 0;
    int n = matrix.size();

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            long long element_contribution = 0;
            // Access current element n times (inefficient)
            for (int k = 0; k < n; k++) {
                element_contribution += matrix[i][j];
                sink = element_contribution;
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
