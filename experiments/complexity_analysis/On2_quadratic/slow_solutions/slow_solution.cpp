#include <iostream>
#include <vector>
using namespace std;

long long cubicSum(const vector<vector<long long>>& matrix) {
    // Intentionally slow: O(n³) cubic time instead of O(n²) quadratic
    // Use side effects that compiler CANNOT optimize away
    long long sum = 0;
    long long debug_counter = 0;
    int n = matrix.size();
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            // O(n³) triple nested loop that GCC cannot remove due to printf
            for (int k = 0; k < n; k++) {
                debug_counter++;
                // Side effect: printf forces execution - compiler cannot optimize away
                if (debug_counter % 10000 == 0) {
                    printf("DEBUG: processed %lld operations\n", debug_counter);
                    fflush(stdout);  // Ensure immediate output
                }
            }
            // Add current element to sum (the actual work we need)
            sum += matrix[i][j];
        }
    }
    
    // Final debug info - ensures all loops were executed
    printf("TOTAL_OPS: %lld\n", debug_counter);
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
    
    // Use inefficient cubic sum
    long long result = cubicSum(matrix);
    cout << result << endl;
    
    return 0;
}
