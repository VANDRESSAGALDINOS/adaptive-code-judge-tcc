#include <iostream>
#include <vector>
using namespace std;

// ANTI-OPTIMIZATION (language-specific, C++ only): the slow makes a third recursive
// call identical to the second one to force O(3^n). Because that call is pure, -O2
// eliminates it by common-subexpression elimination (CSE), collapsing O(3^n) -> O(2^n).
// A volatile side effect per call makes the function observably non-pure, so the
// duplicate call may not be elided. Output is unchanged. Python (no CSE) needs none.
static volatile long long call_sink = 0;

bool inefficientSubsetSum(const vector<int>& arr, int target, int index = 0) {
    // Algorithmically equivalent but inefficient: O(3^n) using redundant recursive calls.
    // Each decision point explores three paths: include, exclude, and duplicate exclude.
    call_sink = call_sink + 1;  // observable side effect: blocks CSE of the duplicate call

    // Base cases
    if (target == 0) return true;  // Found exact sum
    if (index >= arr.size()) return false;  // No more elements

    // Three recursive calls: include, exclude, and redundant exclude
    // The redundant call computes the same result as exclude but forces O(3^n) complexity
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
