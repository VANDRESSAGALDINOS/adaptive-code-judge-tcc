# Problem Specification: Cycle Finding

## Formal Definition

### Problem Statement
Given a directed graph G = (V, E) where |V| = n and |E| = m, determine if the graph contains a negative-weight cycle. If such a cycle exists, output any one cycle in the correct order.

### Input Format
```
Line 1: n m (number of nodes and edges)
Next m lines: a b c (directed edge from node a to node b with weight c)
```

### Output Format
```
If negative cycle exists:
  Line 1: YES
  Line 2: sequence of nodes forming the cycle (first and last node identical)
If no negative cycle exists:
  Line 1: NO
```

### Constraints
- 1 ≤ n ≤ 2,500 (nodes)
- 1 ≤ m ≤ 5,000 (edges)
- 1 ≤ a, b ≤ n (node indices)
- -10⁹ ≤ c ≤ 10⁹ (edge weights)

## Algorithmic Requirements

### Optimal Approach
Bellman-Ford algorithm with negative cycle detection is optimal for this constraint set:
- **Detection Phase**: O(nm) time complexity for n iterations of edge relaxation
- **Reconstruction Phase**: O(n) time complexity for cycle path reconstruction
- **Space Complexity**: O(n + m) for distance arrays and edge storage

### Algorithm Justification
For the given constraints (n ≤ 2,500, m ≤ 5,000):
- **Maximum Operations**: 2,500 × 5,000 = 12.5 × 10⁶ operations
- **Practical Complexity**: Well within computational limits for both languages
- **Alternative Approaches**: Floyd-Warshall O(n³) would be less efficient for sparse graphs

## Mathematical Formulation

### Distance Array Initialization
```
dist[i] = 0 for all i ∈ [1, n]  (implicit super-source approach)
parent[i] = -1 for all i ∈ [1, n]
```

### Bellman-Ford Relaxation
```
For iteration k = 1 to n:
    For each edge (a, b, w) ∈ E:
        if dist[a] + w < dist[b]:
            dist[b] = dist[a] + w
            parent[b] = a
            x = b  (track last updated node)
```

### Negative Cycle Detection
```
If x ≠ -1 after n iterations:
    Negative cycle exists
    Find cycle node: y = parent^n[x]  (apply parent n times)
    Reconstruct cycle using parent pointers
```

## Implementation Requirements

### Correctness Criteria
1. **Cycle Detection**: Correctly identify presence of negative cycles
2. **Cycle Reconstruction**: Output valid cycle with negative total weight
3. **Connectivity Handling**: Handle disconnected components appropriately
4. **Precision**: Avoid integer overflow with edge weights up to 10⁹

### Edge Cases
- **Self-loops**: Negative self-loops form trivial cycles
- **Multiple Cycles**: Any valid negative cycle is acceptable output
- **Disconnected Graphs**: Cycles may exist in separate components
- **Zero-weight Cycles**: Only negative cycles should be reported

## Test Case Analysis

### CSES Official Test Cases
- **Total Cases**: 27 official test cases
- **Small Cases**: n ≤ 100, simple graph structures
- **Medium Cases**: n ≤ 1,000, moderate complexity
- **Large Cases**: n = 2,500, maximum constraint utilization

### Critical Test Cases
Test cases that typically cause Time Limit Exceeded (TLE) in Python implementations:
- **Cases 6-10**: Dense graphs with high edge-to-node ratios
- **Cases 13, 19, 21, 27**: Maximum constraint cases with complex cycle structures

### Performance Characteristics
- **Dense Graphs**: Higher m/n ratio increases computational load
- **Deep Cycles**: Longer paths to cycle detection increase iteration count
- **Multiple Components**: Disconnected graphs require full algorithm execution

## Platform Specifications

### CSES Platform Constraints
- **Time Limit**: 1.00 second
- **Memory Limit**: 512 MB
- **Evaluation**: Fixed time limit across all programming languages
- **Judge System**: Single-threaded execution environment

### Expected Performance Characteristics
- **C++ (g++ -O2)**: ~0.2-0.4 seconds for maximum constraint cases
- **Python (CPython 3.x)**: ~0.8-1.7 seconds for maximum constraint cases
- **Performance Gap**: Approximately 4.33x slower execution in Python

### Binary Verdict Implications
The significant performance differential creates systematic evaluation bias where algorithmically identical solutions receive different verdicts based solely on implementation language. This necessitates adaptive time limit methodology to ensure fair evaluation while preserving algorithmic selectivity.
