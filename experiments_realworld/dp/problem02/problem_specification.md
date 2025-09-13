# Grid Paths Problem Specification

## Problem Statement

**Input**: Integer n followed by n×n grid containing '.' (free) and '*' (obstacle)
**Output**: Number of paths from (0,0) to (n-1,n-1) modulo 10⁹+7
**Movement**: Only right and down allowed

## Mathematical Definition

Given grid G[i][j], find number of paths P where:
- Path starts at G[0][0] 
- Path ends at G[n-1][n-1]
- Each step: (i,j) → (i+1,j) or (i,j) → (i,j+1)
- Path avoids all obstacles G[i][j] = '*'

## Dynamic Programming Formulation

**State Definition**: dp[i][j] = number of valid paths to reach cell (i,j)

**Recurrence Relation**:
```
dp[i][j] = 0                              if G[i][j] = '*'
dp[i][j] = dp[i-1][j] + dp[i][j-1]        if G[i][j] = '.' and i,j > 0
dp[0][0] = 1                              if G[0][0] = '.'
```

**Boundary Conditions**:
- dp[0][j] = dp[0][j-1] if G[0][j] ≠ '*'
- dp[i][0] = dp[i-1][0] if G[i][0] ≠ '*'

## Example

**Input**:
```
4
....
.*.
..*.
...
```

**Output**: 3

**Valid Paths**:
1. Right→Right→Right→Down→Down→Down
2. Right→Down→Right→Right→Down→Down  
3. Down→Down→Right→Right→Right→Down

## Constraints

- 1 ≤ n ≤ 1000
- Grid contains only '.' and '*'
- Answer modulo 10⁹+7

## Complexity Analysis

**Time**: O(n²) - each cell computed once
**Space**: O(n²) - DP table storage

---

**Source**: CSES Problem Set #1638
**Category**: Dynamic Programming, Path Counting
