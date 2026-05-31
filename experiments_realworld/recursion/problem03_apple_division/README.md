# Apple Division Problem Analysis

## Overview

Analysis of backtracking algorithm performance for the Apple Division problem (CSES 1623). This study examines the comparative performance characteristics between C++ and Python implementations for subset partitioning algorithms with exponential time complexity.

## Problem Definition

**Input**: n apples with known weights
**Output**: Minimum possible difference between two groups when apples are divided
**Constraints**: 1 ≤ n ≤ 20, 1 ≤ weight ≤ 10^9

## Algorithm Characteristics

### Computational Approach
- **Method**: Recursive backtracking with complete state space exploration
- **Complexity**: O(2^n) theoretical time complexity
- **Space**: O(n) recursion stack depth

### Problem Structure
The algorithm explores all possible ways to partition n apples into two groups, computing the absolute difference between group sums for each partition and tracking the minimum difference encountered.

## Implementation Analysis

### Optimal Implementations
Both C++ and Python implementations use identical recursive backtracking logic:
- Recursive exploration of all 2^n possible partitions
- State tracking through recursion parameters
- Minimum difference calculation and updating

### Suboptimal Implementations
Modified versions include additional computational overhead (EXTRA_WORK = 2000 operations per recursive call) to analyze performance sensitivity under increased computational load.

## File Structure

```
problem03_apple_division/
├── README.md                    # This overview
├── implementations/
│   ├── optimal/                 # Primary algorithm implementations
│   │   ├── solution.cpp         # C++ backtracking implementation
│   │   └── solution.py          # Python backtracking implementation
│   └── suboptimal/              # Modified implementations with overhead
│       ├── solution.cpp         # C++ with computational overhead
│       └── solution.py          # Python with computational overhead
├── test_data/                   # Validation test cases
│   ├── input/                   # Problem instances (18 test cases)
│   └── output/                  # Expected results
├── benchmarking/                # Performance measurement scripts
├── results/                     # Experimental data and validation results
└── metadata/                    # Problem specification and metadata
```

## Key Findings

### Performance Characteristics
External validation through CSES online judge demonstrates that both C++ and Python implementations achieve successful completion within time constraints for this problem size and complexity.

### Algorithm Equivalence
Both language implementations employ mathematically equivalent recursive backtracking approaches, ensuring identical solution correctness across all test cases.

### Practical Implications
The study provides empirical data on language performance characteristics for exponential-time recursive algorithms in competitive programming contexts.

## Research Contributions

This analysis contributes to understanding performance trade-offs in recursive algorithm implementations across different programming languages, with specific focus on subset partitioning problems with exponential complexity.

The research provides quantitative performance data for algorithm selection considerations in computational contexts with strict time and resource constraints.

---

**Problem**: CSES 1623 - Apple Division  
**Category**: Backtracking, Subset Partitioning  
**Complexity**: O(2^n) time, O(n) space
