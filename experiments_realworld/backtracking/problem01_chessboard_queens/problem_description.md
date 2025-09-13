# CSES 1624 - Chessboard and Queens

## Problem Specification

**Source**: CSES Problem Set  
**Problem ID**: 1624  
**Category**: Backtracking  
**Difficulty**: Medium  
**Time Limit**: 1.00s  
**Memory Limit**: 512 MB  

## Problem Statement

Place eight queens on a chessboard such that no two queens attack each other. Additionally, some squares are blocked (*) and others are free (.), and queens can only be placed on free squares. Blocked squares do not prevent queens from attacking each other.

Count the number of valid ways to place the eight queens.

## Input Format

Eight lines, each containing eight characters. Each square is either free (.) or blocked (*).

## Output Format

Print one integer: the number of ways to place the queens.

## Example

**Input:**
```
........
........
..*.....
........
........
.....**.
...*....
........
```

**Output:**
```
65
```

## Algorithmic Analysis

### Algorithmic Approach: Classical Backtracking

**Algorithm Steps**:
1. Place queens row by row (one per row)
2. For each position, verify validity:
   - Square is not blocked (*)
   - No conflict with previously placed queens
3. Use constraint tracking for optimization:
   - Column occupancy tracking
   - Diagonal occupancy tracking (both directions)
4. Backtrack when no valid positions remain

### Complexity Analysis

**Time Complexity**: O(8!) worst case, significantly reduced by pruning  
**Space Complexity**: O(8) for constraint arrays + O(8) recursion stack  

### Problem Characteristics

- **Fixed Size**: 8×8 board (non-scaling)
- **Intensive Pruning**: Constraint checking eliminates many possibilities
- **Limited Recursion**: Maximum 8 recursion levels
- **Deterministic**: Identical input produces identical output

## Research Relevance for Language Bias Analysis

### Initial Hypotheses

1. **Intensive recursion** may cause overhead in Python
2. **Backtracking** with multiple calls may amplify performance disparities
3. **Frequent constraint checking** may favor compiled C++

### Empirical Findings

**Algorithmic Bias**: Not observed for optimal implementations  
**Differential Selectivity**: Confirmed for suboptimal implementations  

- Both languages successfully execute optimal algorithms
- Python demonstrates extreme sensitivity to intentional algorithmic overhead
- C++ tolerates identical overhead with controlled degradation

### Scientific Significance

This problem reveals differential algorithm selectivity, complementing traditional algorithmic bias cases. The findings suggest that evaluation systems may inadvertently penalize Python even when algorithms are functionally equivalent and correct, particularly when implementations are suboptimal.
