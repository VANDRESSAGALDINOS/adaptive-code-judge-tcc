# Two Sets Problem Analysis

## Overview

This experiment analyzes the equivalence and performance characteristics of iterative versus recursive dynamic programming approaches for the Two Sets problem. The study demonstrates algorithmic equivalence while quantifying implementation-specific performance differences.

## Research Objectives

1. **Algorithmic Equivalence**: Prove mathematical equivalence between iterative and recursive DP implementations
2. **Performance Analysis**: Quantify performance differences between implementation approaches  
3. **Combinatorial Counting**: Analyze DP approaches for set partition problems
4. **Modular Arithmetic**: Examine division by 2 using modular inverse

## Problem Specification

**Input**: Integer n (1 ≤ n ≤ 500)
**Output**: Number of ways to divide numbers 1,2,...,n into two sets with equal sums

**Mathematical Framework**:
- Total sum: S = n(n+1)/2
- If S is odd: answer = 0 (impossible to divide equally)
- If S is even: count ways to form subset with sum S/2, then divide by 2

## Key Findings

### Implementation Approach Comparison

| Approach | Time Complexity | Space Complexity | Performance Characteristics |
|----------|----------------|------------------|----------------------------|
| **Iterative** | O(n × S/2) | O(n × S/2) | Better cache locality |
| **Recursive** | O(n × S/2) | O(n × S/2) + O(n) stack | Function call overhead |

### Algorithmic Equivalence

Both implementations solve the identical recurrence:
- **State**: dp[i][j] = ways to form sum j using numbers 1 to i
- **Transition**: dp[i][j] = dp[i-1][j] + dp[i-1][j-i] (if j ≥ i)
- **Base Case**: dp[i][0] = 1 for all i

## File Structure

```
coin_combinations_analysis/
├── README.md                           # This overview
├── implementations/                    # Algorithm implementations
│   ├── optimal_iterative/             # Bottom-up DP implementations
│   │   ├── solution.cpp               # C++ iterative implementation
│   │   └── solution.py                # Python iterative implementation
│   └── optimal_recursive/             # Top-down DP implementations
│       ├── solution.cpp               # C++ recursive implementation
│       └── solution.py                # Python recursive implementation
├── test_data/                         # Validation test cases
├── benchmarking/                      # Experimental execution scripts
├── results/                           # Experimental data
└── metadata/                          # Problem metadata
```

## Mathematical Analysis

### Problem Complexity
- **Input Size**: n ≤ 500
- **State Space**: O(n²) states (i from 0 to n, j from 0 to n(n+1)/4)
- **Transition**: O(1) per state
- **Total Complexity**: O(n³) worst case

### Modular Arithmetic
- **Division by 2**: Uses modular inverse 2^(MOD-2) mod MOD
- **Reason**: Each partition counted twice (A,B) and (B,A) are equivalent
- **Implementation**: Fast exponentiation for modular inverse

## Research Contributions

### Algorithmic Insights
1. **Set Partition DP**: Standard subset sum variation with division correction
2. **Modular Division**: Practical application of Fermat's Little Theorem
3. **Implementation Equivalence**: Iterative and recursive approaches yield identical results

### Performance Characteristics
- **Memory Access**: Iterative approach shows better cache performance
- **Function Calls**: Recursive approach has measurable overhead
- **Scalability**: Both approaches handle maximum constraints effectively

## Usage

### Running Comparative Analysis
```bash
cd benchmarking/
python run_two_sets_analysis.py
```

### Performance Measurement
```bash
cd benchmarking/
python measure_performance.py --max-n 500
```

## Research Impact

This analysis contributes to understanding dynamic programming implementation trade-offs in combinatorial counting problems. The research demonstrates that:

1. **Mathematical equivalence is preserved across implementation styles**
2. **Performance differences are measurable but moderate for this problem size**
3. **Both approaches are viable for competitive programming constraints**
4. **Modular arithmetic implementation is consistent across approaches**

The findings provide empirical foundation for algorithm selection in educational and competitive programming contexts.

---

**Algorithm Category**: Dynamic Programming  
**Problem Type**: Set Partitioning  
**Complexity**: O(n³) time, O(n²) space  
**Mathematical Rigor**: Formal equivalence established
