#include <iostream>
using namespace std;

int main() {
    long long a, b;
    cin >> a >> b;
    
    // Sum
    cout << a + b << endl;
    
    // Difference  
    cout << a - b << endl;
    
    // Product
    cout << a * b << endl;
    
    // Integer division (handle division by zero)
    if (b != 0) {
        cout << a / b << endl;
    } else {
        cout << 0 << endl;
    }
    
    return 0;
}
