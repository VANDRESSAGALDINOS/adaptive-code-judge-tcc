# Graph Problem 03: Planets Queries I (CSES 1750)

## Overview

This directory contains experimental analysis of the functional graph traversal problem using binary lifting algorithm, comparing C++ and Python implementations under fixed time constraints. This experiment represents a unique case where both language implementations fail under traditional evaluation systems, demonstrating algorithmic complexity limits that transcend language-specific performance characteristics.

## Problem Specification

- **Platform**: CSES (Competitive Programming School)
- **Problem ID**: 1750
- **Algorithm**: Binary lifting on functional graphs (O(n log k + q log k))
- **Time Limit**: 1.00s
- **Memory Limit**: 512 MB

## Experimental Structure

```
problem03/
├── implementations/
│   ├── optimal/                 # Binary lifting implementations
│   └── suboptimal/              # Inefficient reference implementations
├── test_data/
│   ├── input/                   # 14 official CSES test cases
│   └── output/                  # Expected outputs
├── benchmarking/                # Performance measurement and analysis scripts
├── results/                     # Experimental data and binary verdict analysis
├── metadata/                    # Problem and experiment metadata
├── problem_specification.md     # Formal problem definition
├── algorithmic_analysis.md      # Mathematical equivalence proofs
└── experimental_results.md      # Empirical findings and unique case analysis
```

## Key Findings

- **C++ Performance**: Failed in critical test cases (binary verdict: REJECTED)
- **Python Performance**: Failed in critical test cases (binary verdict: REJECTED)
- **External Validation**: C++ achieves 100% success on CSES platform, Python achieves 57.1%
- **Algorithmic Complexity**: O(n log k + q log k) with k ≤ 10⁹ creates computational burden
- **Unique Scientific Case**: Both implementations fail locally, demonstrating platform-dependent performance characteristics

## Implementation Details

Both optimal implementations use identical binary lifting algorithm:
- **Preprocessing**: O(n log k) for building jump table
- **Query Processing**: O(q log k) for k-step traversal queries
- **Space Complexity**: O(n log k)
- **Correctness**: Verified against official CSES test cases

## Critical Test Cases

Test cases that demonstrate computational complexity limits:
- **Cases 6-10, 12, 14**: Maximum constraint utilization (n = 200,000, q = 200,000, k = 10⁹)
- **Platform Dependency**: Local environment shows different performance characteristics than CSES

## Experimental Methodology

Binary verdict analysis using controlled Docker environments with standardized resource allocation. This unique case demonstrates that some algorithmic complexities create performance barriers that affect both languages, while external platform validation reveals environment-dependent behavior.

## Scientific Relevance

This experiment provides evidence that algorithmic complexity can create universal performance barriers independent of language implementation, while simultaneously demonstrating platform-dependent performance variations. The case challenges assumptions about systematic language bias by showing scenarios where both implementations fail under identical constraints, yet succeed differentially on external platforms.
