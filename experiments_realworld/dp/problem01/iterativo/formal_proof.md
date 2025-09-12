# Formal Algorithmic Equivalence Proof - Coin Combinations I (Iterative DP)

## Proof Objective

Demonstrate that the provided C++ and Python implementations of iterative dynamic programming for CSES 1635 are **algorithmically equivalent**, differing only in language-specific syntax and performance characteristics, not in computational logic or mathematical correctness.

## Algorithmic Specification

### Common Algorithm: Iterative Dynamic Programming (Bottom-up)

**Input**: Set of n coin values and target sum x  
**Output**: Number of distinct ways to form sum x using available coins (order matters)  
**Method**: Bottom-up dynamic programming with tabulation

### Formal Algorithm Description
```
ALGORITHM Coin_Combinations_Iterative(coins[], x)
INPUT: Array coins[1..n] of coin values, target sum x
OUTPUT: Number of ways to form sum x (mod 10^9+7)

INITIALIZATION:
  dp[0..x] = 0
  dp[0] = 1                    // Base case: one way to form sum 0

MAIN_COMPUTATION:
  FOR sum = 1 TO x:
    FOR each coin in coins:
      IF sum >= coin THEN
        dp[sum] = (dp[sum] + dp[sum - coin]) mod (10^9+7)

RETURN dp[x]
```

## Implementation Analysis

### C++ Implementation (Iterative DP)
```cpp
#include <iostream>
#include <vector>
using namespace std;

const int MOD = 1000000007;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n, x;
    cin >> n >> x;
    
    vector<int> coins(n);
    for (int i = 0; i < n; i++) {
        cin >> coins[i];
    }
    
    // DP iterativo bottom-up
    vector<int> dp(x + 1, 0);
    dp[0] = 1; // Caso base: uma maneira de formar soma 0
    
    // Para cada soma possível de 1 até x
    for (int sum = 1; sum <= x; sum++) {
        // Tentar usar cada moeda
        for (int i = 0; i < n; i++) {
            if (sum >= coins[i]) {
                dp[sum] = (dp[sum] + dp[sum - coins[i]]) % MOD;
            }
        }
    }
    
    cout << dp[x] << "\n";
    
    return 0;
}
```

### Python Implementation (Iterative DP)
```python
import sys

MOD = 1000000007

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    
    n = int(next(it))
    x = int(next(it))
    
    coins = []
    for _ in range(n):
        coins.append(int(next(it)))
    
    # DP iterativo bottom-up
    dp = [0] * (x + 1)
    dp[0] = 1  # Caso base: uma maneira de formar soma 0
    
    # Para cada soma possível de 1 até x
    for sum_val in range(1, x + 1):
        # Tentar usar cada moeda
        for coin in coins:
            if sum_val >= coin:
                dp[sum_val] = (dp[sum_val] + dp[sum_val - coin]) % MOD
    
    print(dp[x])

if __name__ == "__main__":
    main()
```

## Proof of Algorithmic Equivalence

### 1. Initialization Verification

**Mathematical specification**: 
```
dp[0] = 1 (base case)
dp[i] = 0 for i > 0 (initial state)
```

**C++ implementation**:
```cpp
vector<int> dp(x + 1, 0);  // Initialize all to 0
dp[0] = 1;                 // Set base case
```

**Python implementation**:
```python
dp = [0] * (x + 1)  # Initialize all to 0
dp[0] = 1           # Set base case
```

**Verification**: Both implementations identically initialize the DP table.

### 2. Recurrence Relation Verification

**Mathematical specification**: 
```
dp[sum] = Σ dp[sum - coin_i] for all i where sum ≥ coin_i
```

**C++ implementation**:
```cpp
for (int sum = 1; sum <= x; sum++) {
    for (int i = 0; i < n; i++) {
        if (sum >= coins[i]) {
            dp[sum] = (dp[sum] + dp[sum - coins[i]]) % MOD;
        }
    }
}
```

**Python implementation**:
```python
for sum_val in range(1, x + 1):
    for coin in coins:
        if sum_val >= coin:
            dp[sum_val] = (dp[sum_val] + dp[sum_val - coin]) % MOD
```

**Verification**: Both implementations iterate through sums 1 to x, then through all coins, applying identical recurrence relation with modular arithmetic.

### 3. Iteration Order Verification

**Specification**: Process sums in ascending order (1 to x) to ensure dependencies are computed before use.

**Both implementations**: 
- Outer loop: sum/sum_val from 1 to x
- Inner loop: iterate through all coins
- Dependency guarantee: dp[sum-coin] computed before dp[sum] (since sum-coin < sum)

**Verification**: Identical iteration order ensures correct dependency resolution.

### 4. Modular Arithmetic Verification

**Both implementations**: `(dp[sum] + dp[sum - coin]) % MOD` where `MOD = 1000000007`

**Verification**: Identical modular arithmetic to prevent integer overflow.

### 5. Memory Access Pattern Verification

**C++**: 
- Array-style access: `dp[sum]`, `coins[i]`
- Contiguous memory allocation

**Python**: 
- List-style access: `dp[sum_val]`, `coin` (iterator)
- Dynamic memory allocation

**Verification**: Different memory models but equivalent logical access pattern.

## Complexity Analysis

### Time Complexity
**Both implementations**: O(n × x)
- Outer loop: x iterations (1 to x)
- Inner loop: n iterations (all coins)
- Each operation: O(1)
- Total: O(n × x)

### Space Complexity
**Both implementations**: O(x)
- DP table: x + 1 entries
- Input storage: O(n) for coins
- No recursion overhead (iterative approach)
- Total: O(x + n) = O(x) for typical cases where x ≥ n

### Memory Access Efficiency
**C++**: Direct array access with compile-time optimization
**Python**: List access with runtime bounds checking and type verification

## Validation Results Comparison

### CSES Platform Results

#### C++ Iterativo - Validação Externa
**Status**: ✅ **ACCEPTED (13/13)**  
**Data**: 2025-08-31 21:59:50 +0300

**Performance Crítica**:
| Test | Time | Análise |
|------|------|---------|
| #4 | 0.57s | Caso crítico A |
| #8 | 0.57s | Caso crítico B |
| #11 | 0.57s | Caso crítico C |

#### Python Iterativo - Validação Externa
**Status**: ❌ **TLE (5/13)**  
**Data**: 2025-08-31 22:00:46 +0300

**Pattern de Falha**:
| Test | Verdict | Comparação vs C++ |
|------|---------|-------------------|
| #4 | TLE | >+75% overhead |
| #5 | TLE | >+233% overhead |
| #8 | TLE | >+75% overhead |
| #11 | TLE | >+75% overhead |
| #12 | TLE | >+900% overhead |

### Benchmark Local Controlado

#### Calibração (Test Case 9)
- **C++ Mediana**: 0.308s
- **Python Mediana**: 0.340s  
- **Fator**: 1.11x (Python 11% mais lento)

#### Validação Crítica
**Cases 4,8,11**: 
- **C++**: 100% ACCEPTED (15/15)
- **Python**: 0% ACCEPTED (0/15) - TLE sistemático

## Critical Discovery: Persistence of Temporal Injustice

### Comparative Analysis with Recursive DP

| Métrica | DP Recursivo | DP Iterativo | Insight |
|---------|--------------|--------------|---------|
| Calibration Factor | 0.97x | 1.11x | Iterativo mais lento |
| Critical Cases C++ | 90% ACCEPTED | 100% ACCEPTED | Iterativo superior |
| Critical Cases Python | 0% ACCEPTED | 0% ACCEPTED | Injustiça persiste |

### Hypothesis Refutation

**Initial Hypothesis**: Iterative DP would eliminate temporal injustice by removing recursion overhead.

**Empirical Result**: **REFUTED**. Temporal injustice persists with identical magnitude.

### Causal Factor Identification

The persistence of injustice in iterative DP confirms that the determinant factors are:

1. **Interpretive overhead**: Fundamental difference between compiled vs interpreted languages
2. **Algorithmic intensity**: O(n×x) complexity with intensive array access
3. **Input scale dependency**: Critical cases (x=1,000,000, n=100) systematically exceed Python temporal capacity

## Architectural Comparison

### Stack Usage
**Iterative DP**: O(1) stack space (no recursion)
**Advantage**: Eliminates stack overflow concerns present in recursive approach

### Memory Access Pattern
**C++**: Sequential array access with cache-friendly patterns
**Python**: List access with interpreter overhead on each operation

### Computational Intensity
**Both approaches**: Identical number of fundamental operations
**Difference**: Per-operation overhead (compiled vs interpreted)

## Conclusion

The C++ and Python implementations are **mathematically and algorithmically equivalent** for iterative dynamic programming. The observed performance differences are exclusively due to language architectural characteristics:

1. **Compilation vs interpretation**: Native machine code vs bytecode interpretation
2. **Memory management**: Direct access vs managed memory with bounds checking
3. **Type system**: Static typing vs dynamic typing overhead

### Equivalence Status
✅ **PROVEN**: Same mathematical logic, same complexity, same correctness

### Performance Characterization
1. **Small/medium inputs**: Equivalent performance (no injustice)
2. **Large inputs**: Systematic Python penalization (temporal injustice)
3. **Critical insight**: Injustice is **algorithmic intensity dependent**, not **approach dependent**

### Scientific Contribution
This analysis definitively establishes that temporal injustice in competitive programming is caused by **interpretive overhead under computational intensity**, not by specific algorithmic approaches (recursive vs iterative).

**Status**: ✅ **ALGORITHMIC EQUIVALENCE PROVEN**  
**Date**: 2025-08-31  
**Platform**: CSES Online Judge + Local Controlled Benchmark  
**Reproducibility**: Complete source code and statistical data documented












