# Slow Solutions Description - Problem03 CSES 1750

## Objective
Create intentionally slow versions of the binary lifting algorithm to validate that our adaptive benchmark preserves selectivity by rejecting inefficient solutions.

## Algorithm Modification Strategy

### Original Algorithm (Efficient)
- **Binary Lifting**: O(n log k + q log k)
- **Preprocessing**: Build 2^i jump table
- **Query Processing**: Decompose k into binary representation

### Slow Algorithm (Inefficient)
- **Naive Simulation**: O(q * k) where k can be up to 10^9
- **No Preprocessing**: Direct step-by-step simulation
- **Additional Overhead**: Extra wasteful computations

## Implementation Details

### C++ Slow Solution
```cpp
// Replace binary lifting with naive simulation
for (int step = 0; step < k; step++) {
    x = next[x];
    // Extra wasteful work with EXTRA_WORK = 50
}
```

### Python Slow Solution
```python
# Replace binary lifting with naive simulation
for step in range(k):
    x = next_planet[x]
    # Extra wasteful work with EXTRA_WORK = 50
```

## Expected Behavior

### Performance Prediction
- **Small k cases**: May still pass (k < 1000)
- **Large k cases**: Guaranteed TLE (k > 10^6)
- **Critical cases**: Should TLE even with adaptive time limits

### Validation Criteria
1. **Slow solutions must TLE** in cases where efficient solutions pass
2. **Adaptive benchmark must reject** slow solutions
3. **Selectivity preserved**: Only efficient algorithms should be accepted

## Test Strategy
1. Submit slow solutions to CSES (expect TLE)
2. Test slow solutions in local adaptive benchmark
3. Confirm TLE in critical cases (8, 12)
4. Validate that adjustment factor doesn't rescue inefficient algorithms

## Scientific Purpose
Demonstrates that adaptive benchmarks maintain algorithmic rigor by:
- Accepting efficient solutions (binary lifting)
- Rejecting inefficient solutions (naive simulation)
- Preserving competitive programming standards


