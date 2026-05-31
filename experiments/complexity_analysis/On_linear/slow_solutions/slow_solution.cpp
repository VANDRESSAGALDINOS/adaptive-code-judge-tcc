#include <iostream>
#include <vector>
using namespace std;

long long inefficientSum(const vector<long long>& arr) {
    // Algorithmically equivalent but inefficient: O(n^2) using nested summation.
    // Each element is added arr.size() times, then divided by n.
    // ANTI-OPTIMIZATION (language-specific, C++ only): the inner loop adds a value
    // that is constant in j, which -O2 strength-reduces to a single multiply
    // (collapsing O(n^2) -> O(n)). A volatile sink written every iteration is an
    // observable side effect the compiler may not elide, forcing all n^2 iterations.
    // Output is unchanged (the sink is never read back). Python needs no sink.
    volatile long long sink = 0;
    long long total = 0;
    int n = arr.size();

    for (int i = 0; i < n; i++) {
        long long element_contribution = 0;
        // Add current element n times (inefficient)
        for (int j = 0; j < n; j++) {
            element_contribution += arr[i];
            sink = element_contribution;
        }
        // Divide by n to get back original value
        total += element_contribution / n;
    }

    return total;
}

int main() {
    int n;
    cin >> n;
    
    vector<long long> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }
    
    long long result = inefficientSum(arr);
    cout << result << endl;
    
    return 0;
}
