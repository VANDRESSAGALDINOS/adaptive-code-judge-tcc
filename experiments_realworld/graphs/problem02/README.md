# Graph Problem 02: Cycle Finding (CSES 1197)

## Overview

This directory contains experimental analysis of the negative cycle detection problem using Bellman-Ford algorithm, comparing C++ and Python implementations under fixed time constraints. This experiment represents the first successful application of binary verdict analysis methodology.

## Problem Specification

- **Platform**: CSES (Competitive Programming School)
- **Problem ID**: 1197
- **Algorithm**: Bellman-Ford negative cycle detection (O(nm))
- **Time Limit**: 1.00s
- **Memory Limit**: 512 MB

## Experimental Structure

```
problem02/
├── implementations/
│   ├── optimal/                 # Bellman-Ford implementations
│   └── suboptimal/              # Inefficient reference implementations
├── test_data/
│   ├── input/                   # 27 official CSES test cases
│   └── output/                  # Expected outputs
├── benchmarking/                # Performance measurement and analysis scripts
├── results/                     # Experimental data and binary verdict analysis
├── metadata/                    # Problem and experiment metadata
├── problem_specification.md     # Formal problem definition
├── algorithmic_analysis.md      # Mathematical equivalence proofs
└── experimental_results.md      # Empirical findings and binary verdict analysis
```

## Key Findings

- **C++ Performance**: All test cases within time limit (traditional system)
- **Python Performance**: Time Limit Exceeded in critical cases (traditional system)
- **Adaptive Factor**: 4.33x time limit adjustment required for Python
- **Binary Verdict**: Systematic bias detected and corrected through adaptive methodology
- **Algorithmic Equivalence**: Formally proven identical implementations

## Implementation Details

Both optimal implementations use identical Bellman-Ford algorithm:
- **Time Complexity**: O(nm) where n = nodes, m = edges
- **Space Complexity**: O(n + m)
- **Correctness**: Verified against official CSES test cases

## Critical Test Cases

Test cases that demonstrate systematic evaluation bias:
- **Cases 6, 7, 8, 9, 10**: Large dense graphs causing Python TLE
- **Cases 13, 19, 21, 27**: Additional critical cases with high computational load

## Experimental Methodology

Binary verdict analysis using controlled Docker environments with standardized resource allocation. This methodology enables detection of systematic language bias while preserving algorithmic selectivity through TLE validation of deliberately inefficient implementations.

## Scientific Relevance

This experiment provides the first empirical validation of binary verdict methodology for detecting and correcting systematic evaluation bias in competitive programming platforms. The 4.33x adjustment factor demonstrates quantifiable language performance differential while maintaining algorithmic rigor.
