#include <iostream>
#include <vector>
using namespace std;

int quadraticSearch(const vector<int>& arr, int target) {
    // Intentionally slow: O(n²) quadratic search instead of O(log n) binary search
    // Use side effects that compiler CANNOT optimize away
    long long debug_counter = 0;
    for (int i = 0; i < arr.size(); i++) {
        // O(n²) nested loop that GCC cannot remove due to printf
        for (int k = 0; k < arr.size(); k++) {
            debug_counter++;
            // Side effect: printf forces execution - compiler cannot optimize away
            if (debug_counter % 500000 == 0) {
                printf("DEBUG: processed %lld operations\n", debug_counter);
                fflush(stdout);  // Ensure immediate output
            }
        }
        if (arr[i] == target) {
            printf("TOTAL_OPS: %lld\n", debug_counter);
            return i;
        }
    }
    printf("TOTAL_OPS: %lld\n", debug_counter);
    return -1;
}

int main() {
    int n, target;
    cin >> n >> target;
    
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }
    
    // Use inefficient quadratic search
    int result = quadraticSearch(arr, target);
    cout << result << endl;
    
    return 0;
}
