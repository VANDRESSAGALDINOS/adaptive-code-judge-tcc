# Apple Division Problem Specification

## Problem Statement

**Input**: 
- First line: integer n (number of apples)
- Second line: n integers representing apple weights

**Output**: 
- Single integer representing the minimum possible difference between two groups

**Constraints**:
- 1 ≤ n ≤ 20
- 1 ≤ weight[i] ≤ 10^9

## Mathematical Formulation

Given a set of n apples with weights W = {w₁, w₂, ..., wₙ}, find a partition of W into two disjoint subsets A and B such that:

- A ∪ B = W
- A ∩ B = ∅
- |sum(A) - sum(B)| is minimized

Where sum(A) represents the total weight of apples in subset A.

## Algorithm Description

### Recursive Backtracking Approach

The solution employs recursive backtracking to explore all possible partitions:

```
backtrack(index, sum1):
    if index == n:
        sum2 = total_sum - sum1
        update_minimum(|sum1 - sum2|)
        return
    
    backtrack(index + 1, sum1 + weight[index])  // add to group 1
    backtrack(index + 1, sum1)                  // add to group 2
```

### State Space Analysis
- **Total states**: 2^n possible partitions
- **Recursion depth**: n levels
- **Branching factor**: 2 at each level

## Examples

### Example 1
**Input**:
```
5
3 2 7 4 1
```

**Analysis**:
- Total sum: 17
- Optimal partition: {3, 2, 4} (sum=9) and {7, 1} (sum=8)
- Difference: |9 - 8| = 1

**Output**: `1`

### Example 2
**Input**:
```
4
1 1 1 1
```

**Analysis**:
- Total sum: 4
- Optimal partition: {1, 1} (sum=2) and {1, 1} (sum=2)
- Difference: |2 - 2| = 0

**Output**: `0`

## Complexity Analysis

### Time Complexity
- **Worst case**: O(2^n)
- **Best case**: O(2^n) (must explore all partitions)
- **Average case**: O(2^n)

### Space Complexity
- **Recursion stack**: O(n)
- **Additional space**: O(1)

## Implementation Considerations

### C++ Implementation
- Uses `long long` for weight accumulation to handle large sums
- Employs `LLONG_MAX` for initial minimum value
- Optimized I/O with `ios::sync_with_stdio(false)`

### Python Implementation
- Uses `float('inf')` for initial minimum value
- Requires `sys.setrecursionlimit(10000)` for deep recursion
- Employs list wrapper for mutable minimum tracking

## Algorithmic Properties

### Completeness
The algorithm is complete - it explores all possible partitions and is guaranteed to find the optimal solution.

### Optimality
The algorithm is optimal - it finds the minimum possible difference by exhaustive search.

### Termination
The algorithm terminates when all 2^n partitions have been evaluated.

---

**Source**: CSES Problem Set #1623  
**Category**: Backtracking, Combinatorial Optimization  
**Difficulty**: Medium to Hard (due to exponential complexity)
