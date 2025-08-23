#include <iostream>
using namespace std;

int main() {
    long long a, b;
    cin >> a >> b;
    
    // Intentionally slow: unnecessary nested loops O(n²) where n=50000
    // This should definitely exceed time limits calibrated for O(1)
    for(int i = 0; i < 50000; i++) {
        for(int j = 0; j < 50000; j++) {
            // Waste CPU time with meaningless computation
            volatile long long x = (i * j + a * b) % 1000000;
        }
    }
    
    // Still produce correct output
    cout << a + b << endl;
    cout << a - b << endl;
    cout << a * b << endl;
    
    if (b != 0) {
        cout << a / b << endl;
    } else {
        cout << 0 << endl;
    }
    
    return 0;
}
