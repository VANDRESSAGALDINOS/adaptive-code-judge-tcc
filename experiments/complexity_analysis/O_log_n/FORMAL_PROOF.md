# Formal Proof of Algorithmic Equivalence - O(log n) vs O(n) Search

## Problem Statement

**Input**: Array A[0..n-1] of sorted integers, target value t ∈ ℤ
**Output**: Index i such that A[i] = t, or -1 if t ∉ A

## Algorithm Categories

### Category 1: Optimal Solutions O(log n)

#### Binary Search Algorithm (C++ and Python)
```
Algorithm BINARY_SEARCH(A, t):
1. left ← 0, right ← n-1
2. while left ≤ right do:
3.   mid ← left + ⌊(right-left)/2⌋
4.   if A[mid] = t then return mid
5.   else if A[mid] < t then left ← mid + 1
6.   else right ← mid - 1
7. return -1
```

#### Equivalence Proof - Optimal Category
**Theorem 1**: C++ binary_search ≡ Python binary_search

**Proof**: Both implementations follow identical algorithmic steps:
- Same initialization: left = 0, right = n-1
- Same loop condition: left ≤ right  
- Same midpoint calculation: mid = left + (right-left)//2
- Same comparison logic and index updates
- Same termination conditions

**Invariant**: At each iteration, if target exists, it lies in range [left, right]

### Category 2: Inefficient Solutions O(n)

#### Linear Search Algorithm (C++ and Python)
```
Algorithm LINEAR_SEARCH(A, t):
1. for i = 0 to n-1 do:
2.   if A[i] = t then return i
3. return -1
```

#### Equivalence Proof - Inefficient Category  
**Theorem 2**: C++ linear_search ≡ Python linear_search

**Proof**: Both implementations follow identical algorithmic steps:
- Same iteration: i from 0 to n-1
- Same comparison: A[i] = t
- Same early termination on match
- Same return value when not found

**Invariant**: At iteration i, target has not been found in A[0..i-1]

## Cross-Category Functional Equivalence

### Theorem 3: Functional Equivalence Across Categories
**Statement**: ∀A, t: BINARY_SEARCH(A, t) = LINEAR_SEARCH(A, t)

**Proof**:
Both algorithms solve the same computational problem with identical semantics:

**Case 1** (t ∈ A at position k):
- BINARY_SEARCH: Returns k after O(log n) comparisons
- LINEAR_SEARCH: Returns k after O(k+1) comparisons  
- **Result**: Both return k ✓

**Case 2** (t ∉ A):
- BINARY_SEARCH: Returns -1 after O(log n) comparisons
- LINEAR_SEARCH: Returns -1 after O(n) comparisons
- **Result**: Both return -1 ✓

## Complexity Analysis

### Time Complexity
- **Binary Search**: O(log n) - halves search space each iteration
- **Linear Search**: O(n) - examines each element sequentially

### Space Complexity
- **Both algorithms**: O(1) - constant additional space

## Loop Invariants

### Binary Search Invariant
**Invariant**: If target exists in array, then target ∈ A[left..right]

**Initialization**: left = 0, right = n-1, so target ∈ A[0..n-1] ✓
**Maintenance**: Each iteration maintains target within updated bounds ✓  
**Termination**: left > right implies target not found, or target found at mid ✓

### Linear Search Invariant  
**Invariant**: Target has not been found in A[0..i-1]

**Initialization**: i = 0, no elements checked yet ✓
**Maintenance**: If A[i] ≠ target, increment i and invariant holds ✓
**Termination**: Either target found at position i, or all elements checked ✓

## Correctness Proof

### Theorem 4: Both Algorithms Are Correct
**Statement**: Both algorithms correctly solve the search problem

**Proof for Binary Search**:
- **Partial Correctness**: If algorithm terminates, it returns correct result
- **Termination**: Search space halves each iteration, guaranteed to reach left > right

**Proof for Linear Search**:
- **Partial Correctness**: Sequential check ensures first occurrence found
- **Termination**: Loop bound i < n guarantees termination

## Experimental Validation Framework

The algorithms are **functionally equivalent** but have different time complexities:

1. **Same Input/Output Behavior**: Both produce identical results
2. **Different Performance Characteristics**: O(log n) vs O(n) execution time
3. **Validation Method**: Large arrays will show performance difference
4. **Time Limit Calibration**: System can distinguish between complexities

## Implementation Language Equivalence

### Within Each Category:
- **C++ Binary Search ≡ Python Binary Search**: Same algorithm, different syntax
- **C++ Linear Search ≡ Python Linear Search**: Same algorithm, different syntax

### Cross-Language Performance:
- Language-specific optimizations may affect constants
- Algorithmic complexity remains unchanged across languages
- Time limits must account for language performance factors

## Conclusion

The proof establishes:
1. **Intra-category equivalence**: Same algorithms across languages
2. **Inter-category functional equivalence**: Same problem solution
3. **Complexity differentiation**: O(log n) vs O(n) performance characteristics
4. **Correctness guarantee**: Both approaches solve the search problem correctly

This validates the experimental design for complexity analysis comparing algorithmic efficiency while maintaining functional equivalence.
