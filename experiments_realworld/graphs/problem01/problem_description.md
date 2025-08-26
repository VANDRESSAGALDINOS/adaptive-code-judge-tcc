# Shortest Routes II — All-Pairs Shortest Paths (CSES)

## Problem Metadata

| Attribute | Value |
|-----------|-------|
| **Platform** | CSES (Competitive Programming School) |
| **Problem ID** | 1672 |
| **Problem Name** | Shortest Routes II |
| **URL** | https://cses.fi/problemset/task/1672/ |
| **Time Limit** | 1.00s |
| **Memory Limit** | 512 MB |
| **Category** | Graph Algorithms |
| **Subcategory** | All-Pairs Shortest Paths (APSP) |
| **Tags** | Floyd–Warshall, Distance Matrix, Multiple Queries |

## Thesis Relevance

### Injustice Hypothesis
This problem represents a **classic case** where:
- **C++ passes comfortably** with Floyd–Warshall O(n³)
- **Python (CPython) frequently receives TLE** on fixed 1.00s limit
- **Same algorithmic complexity** in both languages

### Empirical Evidence of Injustice
**Data collected from real Python submission on CSES:**

| Test Case | C++ Status | Python Status | Observation |
|-----------|------------|---------------|-------------|
| #1-5 | ACCEPTED | ACCEPTED | Small cases (~0.02s) |
| #6-12 | ACCEPTED | TLE | **Large cases penalize Python** |
| #13 | ACCEPTED | ACCEPTED | Specific small case |
| #14-15 | ACCEPTED | TLE | **Injustice confirmation** |
| #16 | ACCEPTED | ACCEPTED | Specific small case |

**Injustice Rate**: Python fails in 9/16 cases (56.25%) with correct algorithm.

**Validation**: The equivalent C++ implementation successfully passes all test cases ([CSES Result #14297533](https://cses.fi/problemset/result/14297533/)), confirming that the algorithm is correct and the Python failures are due to time limit constraints, not algorithmic errors.

## Problem Statement

### Description
Given an **undirected** graph with `n` cities and `m` bidirectional roads (each with positive weight), answer `q` minimum distance queries between pairs of cities. If there is no path between two cities, print `-1`.

### Input Format
```
Line 1: n m q
Next m lines: a b c (road between city a and b with weight c)
Next q lines: a b (query: minimum distance from a to b)
```

### Output Format
```
For each query: minimum distance or -1 if no path exists
```

### Constraints
- `1 ≤ n ≤ 500` (number of cities)
- `1 ≤ m ≤ n²` (number of roads)
- `1 ≤ q ≤ 10⁵` (number of queries)
- `1 ≤ c ≤ 10⁹` (road weights)
- Vertices numbered from `1` to `n`

## Algorithmic Analysis

### Optimal Approach: Floyd-Warshall
- **Time Complexity**: O(n³) for preprocessing + O(1) per query
- **Space Complexity**: O(n²) for distance matrix
- **Justification**: With q = 10⁵ queries, O(n³) preprocessing + O(1) queries outperforms multiple Dijkstra O(q × n log n)

### Pseudocode
```
Initialization:
  dist[i][j] = INF for all i,j
  dist[i][i] = 0 for all i
  For each edge (a,b,c): dist[a][b] = min(dist[a][b], c)

Floyd-Warshall:
  For k = 1 to n:
    For i = 1 to n:
      For j = 1 to n:
        dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

Queries:
  For each (a,b): return dist[a][b] or -1 if INF
```

## Performance Analysis by Language

### C++ - Advantages
- **Dense loops**: Compiler aggressively optimizes O(n³) operations
- **Cache locality**: Sequential matrix access benefits L1/L2 cache
- **Minimal overhead**: Native arithmetic and comparison operations
- **Expected result**: ~0.3-0.5s for n=500

### Python - Challenges
- **Interpreter overhead**: Each operation goes through CPython interpreter
- **List access**: `dist[i][j]` has overhead compared to array[i][j] in C++
- **Numeric operations**: `min()` and `+` have per-operation overhead
- **Typical result**: ~1.2-1.8s for n=500 (exceeds 1.00s limit)

## Experimental Protocol

### Controlled Environment
```bash
# C++ Environment
FROM debian:stable-slim
RUN apt-get update && apt-get install -y g++
COMPILE: g++ -O3 -march=native -pipe -o fw solution.cpp
EXECUTE: timeout 2s ./fw < input.txt

# Python Environment  
FROM python:3.11-slim
EXECUTE: timeout 2s python3 solution.py < input.txt
```

### Benchmark Methodology
1. **Case Selection**: Largest official case + 2 medium cases
2. **Repetitions**: 30 executions per language per case
3. **Metrics**: p50, p90, IQR for statistical robustness
4. **Reliability Criteria**: C++ IQR < 15%, Python IQR < 20%
5. **Timeout**: 2.0s (2x original limit for analysis)

### Proposed Adaptive Time Limit Calculation
```
adjustment_factor_python = median(python_times) / median(cpp_times)
adaptive_limit_python = original_limit * adjustment_factor_python
```
**Note**: This adjustment factor is part of the proposed adaptive judge system, not implemented by CSES. The factor will be derived empirically from benchmark data to establish fair time limits per language.

## Hypotheses to Validate

### H1: Documented Injustice
- Python will receive TLE on large cases with fixed 1.00s limit
- C++ will pass comfortably on the same cases

### H2: Effective Adaptive Solution
- With proposed adaptive limits, Python will achieve success rate ≥95%
- Proposed adjustment factor (part of adaptive system) expected between 1.5x-2.5x

### H3: Algorithmic Equivalence
- Both implementations will produce identical outputs
- Same number of fundamental operations (comparisons, updates)

## Extended Validation Protocol

### Cross-Platform TLE Verification
As additional validation of our adaptive methodology, we include **deliberately inefficient solutions** that should receive TLE in both traditional and adaptive systems.

**Purpose**: Demonstrate that adaptive time limits preserve algorithmic selectivity while removing language bias.

**Implementation**: See `slow_validation/` directory for complete TLE cross-validation protocol.

**External Validation**: CSES submissions confirm TLE behavior for both languages:
- C++ Slow Solution: [CSES Result #14298232](https://cses.fi/problemset/result/14298232/) - TLE (no WA)
- Python Slow Solution: [CSES Result #14298238](https://cses.fi/problemset/result/14298238/) - TLE (no WA)

**Scientific Value**: Refutes potential criticism that adaptive systems inflate time limits artificially by showing that inefficient algorithms remain correctly rejected even with adaptive limits.

## Scientific Value for Thesis

### Expected Contributions
1. **Injustice Quantification**: Empirical data on Python/C++ disparity in traditional fixed-limit judges
2. **Adaptive Solution Proposal**: Demonstrate how proposed adaptive time limits remove injustice while maintaining rigor
3. **Algorithmic Selectivity Preservation**: Validate that adaptive limits distinguish efficient from inefficient algorithms
4. **Cross-Platform Behavioral Consistency**: Prove that local system accurately replicates external platform behavior
5. **Generalizable Methodology**: Framework applicable to other dense problems and programming platforms
6. **Pedagogical Evidence**: Positive impact on fair algorithm evaluation through adaptive judging

### Anticipated Technical Insights
- **Loop Density Impact**: O(n³) amplifies language differences
- **Memory Access Patterns**: Sequential matrix access favors C++
- **Interpreter Overhead**: CPython penalty is linear to number of operations
- **Compiler Optimizations**: GCC significantly benefits nested loops
- **Calibration Robustness**: Adjustment factors preserve algorithmic distinction across efficiency levels

## Reference Implementation Status

### Algorithmic Equivalence Verification
The C++ and Python reference implementations for this experiment have been **formally proven algorithmically equivalent** through rigorous mathematical analysis. See `formal_proof.md` for complete proof details.

**Key Verification Results:**
- **Identical Algorithm**: Both implement Floyd-Warshall with same O(n³) complexity
- **Identical Logic**: Same initialization, edge processing, and query handling
- **Identical Correctness**: Both maintain Floyd-Warshall invariants identically
- **Identical Output**: Guaranteed same results for all valid inputs

**Scientific Validity**: Any performance differences observed in benchmarks represent **language implementation characteristics** rather than algorithmic differences, validating the experimental methodology for measuring platform injustice.

**Implementation Quality**: Both solutions are production-ready and suitable as reference implementations, having been tested and verified on the actual CSES platform.

**Platform Validation**: The C++ implementation has been successfully submitted and **ACCEPTED** on CSES ([Result #14297533](https://cses.fi/problemset/result/14297533/)), confirming correctness and establishing baseline performance for experimental comparison.

---

**Last Update**: January 2025  
**C++ Submission Link**: [CSES Result #14297533](https://cses.fi/problemset/result/14297533/) - **ACCEPTED**  
**Reference Implementation Status**: Formally verified equivalent  
**Status**: Ready for implementation and benchmark
