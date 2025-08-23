#include <iostream>
#include <vector>
using namespace std;

long long debug_counter = 0;

bool tripleExponentialSum(const vector<int>& arr, int target, int index = 0) {
    // Intentionally slow: O(3ⁿ) triple exponential instead of O(2ⁿ)
    // Use side effects that compiler CANNOT optimize away
    
    debug_counter++;
    // Side effect: printf forces execution - compiler cannot optimize away
    if (debug_counter % 100000 == 0) {
        printf("DEBUG: processed %lld recursive calls\n", debug_counter);
        fflush(stdout);  // Ensure immediate output
    }
    
    // Base cases
    if (target == 0) {
        printf("FOUND_SOLUTION: %lld calls\n", debug_counter);
        return true;  // Found exact sum
    }
    if (index >= arr.size()) return false;  // No more elements
    
    // Three choices instead of two (third is redundant but forces O(3ⁿ))
    bool include = tripleExponentialSum(arr, target - arr[index], index + 1);
    bool exclude = tripleExponentialSum(arr, target, index + 1);
    bool redundant = tripleExponentialSum(arr, target, index + 1);  // Same as exclude but forces extra computation
    
    return include || exclude || redundant;
}

int main() {
    int n;
    cin >> n;
    
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }
    
    int target;
    cin >> target;
    
    debug_counter = 0;
    
    // Use inefficient triple exponential approach
    bool result = tripleExponentialSum(arr, target);
    
    // Final debug info
    printf("TOTAL_CALLS: %lld\n", debug_counter);
    
    cout << (result ? "YES" : "NO") << endl;
    
    return 0;
}
