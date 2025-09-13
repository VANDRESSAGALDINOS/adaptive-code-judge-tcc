# Graph Problem 01: Shortest Routes II (CSES 1672)

## Overview

This directory contains experimental analysis of the All-Pairs Shortest Path problem using Floyd-Warshall algorithm, comparing C++ and Python implementations under fixed time constraints.

## Problem Specification

- **Platform**: CSES (Competitive Programming School)
- **Problem ID**: 1672
- **Algorithm**: Floyd-Warshall (O(n³))
- **Time Limit**: 1.00s
- **Memory Limit**: 512 MB

## Experimental Structure

```
problem01/
├── implementations/
│   ├── optimal/                 # Floyd-Warshall implementations
│   └── suboptimal/              # Inefficient reference implementations
├── test_data/
│   ├── input/                   # 16 official CSES test cases
│   └── output/                  # Expected outputs
├── benchmarking/                # Performance measurement scripts
├── results/                     # Experimental data and analysis
├── metadata/                    # Problem and experiment metadata
├── problem_specification.md     # Formal problem definition
├── algorithmic_analysis.md      # Mathematical equivalence proofs
└── experimental_results.md      # Empirical findings and analysis
```

## Key Findings

- **C++ Performance**: All 16 test cases within time limit
- **Python Performance**: Time Limit Exceeded (TLE) in 9/16 cases (56.25%)
- **Algorithmic Equivalence**: Formally proven identical implementations
- **Empirical Evidence**: Systematic language bias in fixed-limit evaluation

## Implementation Details

Both optimal implementations use identical Floyd-Warshall algorithm:
- **Time Complexity**: O(n³) preprocessing + O(1) per query
- **Space Complexity**: O(n²)
- **Correctness**: Verified against official CSES test cases

## Experimental Methodology

Controlled benchmarking using Docker containers with standardized resource allocation to measure execution time differences between algorithmically equivalent implementations.

## Scientific Relevance

This experiment provides empirical evidence of systematic evaluation bias in competitive programming platforms, demonstrating the need for adaptive time limit methodologies that preserve algorithmic selectivity while ensuring language-neutral assessment.
