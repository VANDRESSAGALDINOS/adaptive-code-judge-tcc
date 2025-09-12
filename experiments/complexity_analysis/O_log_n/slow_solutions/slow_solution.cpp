#include <iostream>
#include <vector>
using namespace std;

int linearSearch(const vector<int>& arr, int target) {
    // Algorithmically equivalent but inefficient: O(n) linear search
    // Both algorithms solve the search problem, but with different complexities
    for (int i = 0; i < arr.size(); i++) {
        if (arr[i] == target) {
            return i;
        }
    }
    return -1;  // Not found
}

int main() {
    int n, target;
    cin >> n >> target;
    
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }
    
    int result = linearSearch(arr, target);
    cout << result << endl;
    
    return 0;
}
