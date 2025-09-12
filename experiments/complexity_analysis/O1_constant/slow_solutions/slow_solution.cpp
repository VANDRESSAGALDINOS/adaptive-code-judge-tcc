#include <iostream>
#include <cmath>
using namespace std;

int main() {
    long long a, b;
    cin >> a >> b;
    
    // Algorithmically equivalent but inefficient implementation
    // Using inefficient methods for basic arithmetic operations
    
    // Inefficient sum: using repeated addition
    long long sum = a;
    if (b > 0) {
        for (long long i = 0; i < b; i++) sum++;
    } else if (b < 0) {
        for (long long i = 0; i < -b; i++) sum--;
    }
    cout << sum << endl;
    
    // Inefficient difference: using repeated subtraction  
    long long diff = a;
    if (b > 0) {
        for (long long i = 0; i < b; i++) diff--;
    } else if (b < 0) {
        for (long long i = 0; i < -b; i++) diff++;
    }
    cout << diff << endl;
    
    // Inefficient product: using repeated addition
    long long product = 0;
    long long abs_b = (b >= 0) ? b : -b;
    for (long long i = 0; i < abs_b; i++) {
        product += a;
    }
    if (b < 0) product = -product;
    cout << product << endl;
    
    // Integer division (handle division by zero)
    if (b != 0) {
        cout << a / b << endl;
    } else {
        cout << 0 << endl;
    }
    
    return 0;
}
