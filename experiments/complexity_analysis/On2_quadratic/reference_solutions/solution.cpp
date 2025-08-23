#include <iostream>
#include <vector>
using namespace std;

long long matrixSum(const vector<vector<long long>>& matrix) {
    // O(n²) quadratic time: visit each element exactly once
    long long sum = 0;
    int n = matrix.size();
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            sum += matrix[i][j];
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
    
    // Calculate sum using optimal O(n²) approach
    long long result = matrixSum(matrix);
    cout << result << endl;
    
    return 0;
}
