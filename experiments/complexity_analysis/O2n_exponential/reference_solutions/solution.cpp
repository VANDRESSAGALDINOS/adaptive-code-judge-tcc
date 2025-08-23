#include <iostream>
#include <vector>
using namespace std;

bool subsetSum(const vector<int>& arr, int target, int index = 0) {
    // O(2ⁿ) exponential time: check all possible subsets recursively
    
    // Base cases
    if (target == 0) return true;  // Found exact sum
    if (index >= arr.size()) return false;  // No more elements
    
    // Two choices: include current element or exclude it
    bool include = subsetSum(arr, target - arr[index], index + 1);
    bool exclude = subsetSum(arr, target, index + 1);
    
    return include || exclude;
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
    
    // Find subset using optimal O(2ⁿ) recursive approach
    bool result = subsetSum(arr, target);
    
    cout << (result ? "YES" : "NO") << endl;
    
    return 0;
}
