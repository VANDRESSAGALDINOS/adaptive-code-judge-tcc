# Grid Paths Problem Analysis

## Overview

Analysis of iterative versus recursive dynamic programming approaches for the Grid Paths problem (CSES 1638). Demonstrates algorithmic equivalence with performance comparison.

## Problem Definition

**Input**: n×n grid with obstacles ('*') and free cells ('.')
**Output**: Number of paths from top-left to bottom-right (modulo 10⁹+7)
**Constraints**: 1 ≤ n ≤ 1000

## Algorithm Categories

### Iterative Approach
- **Method**: Bottom-up tabulation
- **Complexity**: O(n²) time, O(n²) space
- **Characteristics**: Sequential cell processing

### Recursive Approach  
- **Method**: Top-down memoization
- **Complexity**: O(n²) time, O(n²) space + O(n) stack
- **Characteristics**: Path exploration with caching

## Mathematical Framework

**State**: dp[i][j] = number of paths to reach cell (i,j)
**Recurrence**: dp[i][j] = dp[i-1][j] + dp[i][j-1] if grid[i][j] ≠ '*'
**Base Case**: dp[0][0] = 1 if grid[0][0] ≠ '*'

## File Structure

```
problem02/
├── README.md                    # This overview
├── implementations/
│   ├── optimal_iterative/      # Bottom-up implementations
│   └── optimal_recursive/      # Top-down implementations
├── test_data/                  # Test cases
└── results/                    # Performance data
```

## Key Findings

Both approaches demonstrate identical correctness with measurable performance differences due to implementation overhead.

---

**Problem**: CSES 1638 - Grid Paths
**Category**: Dynamic Programming
**Complexity**: O(n²)
