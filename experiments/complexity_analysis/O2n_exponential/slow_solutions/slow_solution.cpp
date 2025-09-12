#include <iostream>
#include <vector>
using namespace std;

bool inefficientSubsetSum(const vector<int>& arr, int target, int index = 0) {
    // Algorithmically equivalent but inefficient: O(3ⁿ) using redundant recursive calls
    // Each decision point explores three paths: include, exclude, and duplicate exclude
    
    // Base cases
    if (target == 0) return true;  // Found exact sum
    if (index >= arr.size()) return false;  // No more elements
    
    // Three recursive calls: include, exclude, and redundant exclude
    // The redundant call computes the same result as exclude but forces O(3ⁿ) complexity
    bool include = inefficientSubsetSum(arr, target - arr[index], index + 1);
    bool exclude = inefficientSubsetSum(arr, target, index + 1);
    bool redundant_exclude = inefficientSubsetSum(arr, target, index + 1);  // Identical to exclude
    
    // Mathematical equivalence: (A || B || B) = (A || B)
    return include || exclude || redundant_exclude;
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
    
    bool result = inefficientSubsetSum(arr, target);
    
    cout << (result ? "YES" : "NO") << endl;
    
    return 0;
}
