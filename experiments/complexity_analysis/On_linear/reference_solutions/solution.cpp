#include <iostream>
#include <vector>
using namespace std;

long long arraySum(const vector<long long>& arr) {
    // O(n) linear time: visit each element exactly once
    long long sum = 0;
    for (int i = 0; i < arr.size(); i++) {
        sum += arr[i];
    }
    return sum;
}

int main() {
    int n;
    cin >> n;
    
    vector<long long> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }
    
    // Calculate sum using optimal O(n) approach
    long long result = arraySum(arr);
    cout << result << endl;
    
    return 0;
}
