# Two Sets Problem Specification

## Problem Statement

**Input**: An integer n where 1 ≤ n ≤ 500

**Output**: The number of ways to divide the numbers 1, 2, ..., n into two sets such that both sets have the same sum.

**Modular Arithmetic**: Answer modulo 10⁹ + 7

## Mathematical Formulation

### Problem Analysis

Given the set {1, 2, 3, ..., n}, we want to partition it into two disjoint subsets A and B such that:
- A ∪ B = {1, 2, ..., n}
- A ∩ B = ∅
- sum(A) = sum(B)

### Total Sum Calculation

The sum of numbers from 1 to n is: S = n(n+1)/2

### Feasibility Condition

For equal partition to be possible:
- S must be even (otherwise sum(A) + sum(B) = S cannot be split equally)
- If S is odd, answer = 0

### Reduction to Subset Sum

If S is even, the problem reduces to:
- Count ways to select a subset with sum = S/2
- The remaining elements automatically have sum = S/2

### Counting Correction

Since each valid partition {A, B} is counted twice as both {A, B} and {B, A}, we divide the result by 2.

## Examples

### Example 1
**Input**: n = 3
**Calculation**: 
- Numbers: {1, 2, 3}
- Total sum: 6
- Target sum per set: 3
- Valid partitions: {1,2} and {3}
- **Output**: 1

### Example 2  
**Input**: n = 4
**Calculation**:
- Numbers: {1, 2, 3, 4}
- Total sum: 10 (odd)
- **Output**: 0 (impossible)

### Example 3
**Input**: n = 7
**Calculation**:
- Numbers: {1, 2, 3, 4, 5, 6, 7}
- Total sum: 28
- Target sum per set: 14
- Valid partitions: Multiple ways to form sum 14
- **Output**: (calculated via DP)

## Constraints

- **Input Range**: 1 ≤ n ≤ 500
- **Time Limit**: Typically 1-2 seconds
- **Memory Limit**: Typically 256-512 MB
- **Output**: Result modulo 10⁹ + 7

## Algorithmic Approach

### Dynamic Programming State

**State Definition**: dp[i][j] = number of ways to form sum j using numbers from 1 to i

### Recurrence Relation

```
dp[i][j] = dp[i-1][j] + dp[i-1][j-i]  (if j ≥ i)
dp[i][j] = dp[i-1][j]                  (if j < i)
```

### Base Cases

```
dp[0][0] = 1    (one way to form sum 0 with no numbers)
dp[0][j] = 0    (for j > 0, impossible with no numbers)
```

### Final Calculation

```
ways = dp[n][target] where target = S/2
result = (ways * modular_inverse(2)) % MOD
```

## Complexity Analysis

### Time Complexity
- **States**: O(n × S/2) = O(n³)
- **Transitions**: O(1) per state
- **Total**: O(n³)

### Space Complexity
- **DP Table**: O(n × S/2) = O(n³)
- **Optimization Possible**: O(S/2) = O(n²) using rolling array

## Implementation Approaches

### 1. Iterative Bottom-Up
- Fill DP table from dp[0][0] to dp[n][target]
- Process in order: for i from 1 to n, for j from 0 to target

### 2. Recursive Top-Down
- Start from dp[n][target] and recurse with memoization
- Natural recursive structure matches problem definition

Both approaches are mathematically equivalent and produce identical results.

## Modular Arithmetic Details

### Division by 2 Modulo Prime

Since MOD = 10⁹ + 7 is prime, we use Fermat's Little Theorem:
- 2⁻¹ ≡ 2^(MOD-2) (mod MOD)
- Computed using fast exponentiation

### Implementation
```cpp
long long modular_inverse_2 = power(2, MOD-2, MOD);
result = (ways * modular_inverse_2) % MOD;
```

---

**Problem Category**: Dynamic Programming, Combinatorics  
**Difficulty**: Medium  
**Key Concepts**: Subset sum, modular arithmetic, set partitioning
