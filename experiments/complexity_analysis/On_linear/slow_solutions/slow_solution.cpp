#include <iostream>
#include <vector>
using namespace std;

long long quadraticSum(const vector<long long>& arr) {
    // Intentionally slow: O(n²) quadratic time instead of O(n) linear
    // Use side effects that compiler CANNOT optimize away
    long long sum = 0;
    long long debug_counter = 0;
    
    for (int i = 0; i < arr.size(); i++) {
        // O(n²) nested loop that GCC cannot remove due to printf
        for (int j = 0; j < arr.size(); j++) {
            debug_counter++;
            // AGGRESSIVE anti-optimization: printf every 10K operations
            if (debug_counter % 10000 == 0) {
                printf("DEBUG: processed %lld operations\n", debug_counter);
                fflush(stdout);  // Ensure immediate output
            }
        }
        // Add current element to sum (the actual work we need)
        sum += arr[i];
    }
    
    // Final debug info - ensures all loops were executed
    printf("TOTAL_OPS: %lld\n", debug_counter);
    return sum;
}

int main() {
    int n;
    cin >> n;
    
    vector<long long> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }
    
    // Use inefficient quadratic sum
    long long result = quadraticSum(arr);
    cout << result << endl;
    
    return 0;
}
