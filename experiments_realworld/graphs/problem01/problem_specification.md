# Problem Specification: Shortest Routes II

## Formal Definition

### Problem Statement
Given an undirected weighted graph G = (V, E) where |V| = n and |E| = m, process q queries requesting the shortest path distance between specified vertex pairs. If no path exists between two vertices, return -1.

### Input Format
```
Line 1: n m q
Next m lines: a b c (undirected edge between vertices a and b with weight c)
Next q lines: a b (query: shortest distance from vertex a to vertex b)
```

### Output Format
```
For each query: minimum distance or -1 if vertices are disconnected
```

### Constraints
- 1 ≤ n ≤ 500 (vertices)
- 1 ≤ m ≤ n² (edges)  
- 1 ≤ q ≤ 10⁵ (queries)
- 1 ≤ c ≤ 10⁹ (edge weights)
- Vertices indexed from 1 to n
- All edge weights are positive integers

## Algorithmic Requirements

### Optimal Approach
Floyd-Warshall algorithm is optimal for this constraint set:
- **Preprocessing**: O(n³) time complexity
- **Query Processing**: O(1) time complexity per query
- **Space Complexity**: O(n²) for distance matrix

### Algorithm Justification
With q ≤ 10⁵ queries and n ≤ 500:
- Floyd-Warshall total: O(n³ + q) = O(125×10⁶ + 10⁵) ≈ O(125×10⁶)
- Alternative Dijkstra: O(q × n log n) = O(10⁵ × 500 × 9) ≈ O(450×10⁶)

Floyd-Warshall provides superior asymptotic performance for the given constraints.

## Mathematical Formulation

### Distance Matrix Initialization
```
dist[i][j] = {
    0           if i = j
    min(w(i,j)) if (i,j) ∈ E (minimum among multiple edges)
    ∞           otherwise
}
```

### Floyd-Warshall Recurrence
```
For k = 1 to n:
    For i = 1 to n:
        For j = 1 to n:
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

### Query Processing
```
query(a, b) = {
    dist[a][b] if dist[a][b] < ∞
    -1          otherwise
}
```

## Implementation Requirements

### Correctness Criteria
1. **Shortest Path Property**: For all vertex pairs (i,j), dist[i][j] represents the minimum path weight
2. **Connectivity Detection**: Infinite distances correctly identify disconnected components
3. **Self-Distance**: dist[i][i] = 0 for all vertices i
4. **Symmetry**: For undirected graphs, dist[i][j] = dist[j][i]

### Precision Considerations
- Edge weights up to 10⁹ require careful overflow prevention
- Path weights may reach n × max_weight ≤ 500 × 10⁹ = 5 × 10¹¹
- Implementation must use 64-bit integers (long long in C++, int in Python)

## Test Case Analysis

### CSES Official Test Cases
- **Total Cases**: 16 official test cases
- **Small Cases**: n ≤ 100, simple connectivity patterns
- **Large Cases**: n = 500, dense graphs with maximum query load
- **Edge Cases**: Disconnected graphs, single vertices, maximum weights

### Critical Test Cases
Test cases that typically cause Time Limit Exceeded (TLE) in Python implementations:
- Cases 6-12: Large dense graphs (n = 500, high edge density)
- Cases 14-15: Maximum constraint cases (n = 500, q = 10⁵)

### Control Test Cases
Test cases that pass in both C++ and Python:
- Cases 1-5: Small to medium graphs (n ≤ 200)
- Case 13: Specific medium case with favorable characteristics
- Case 16: Large but sparse graph structure

## Platform Specifications

### CSES Platform Constraints
- **Time Limit**: 1.00 second
- **Memory Limit**: 512 MB
- **Evaluation**: Fixed time limit across all programming languages
- **Judge System**: Single-threaded execution environment

### Expected Performance Characteristics
- **C++ (g++ -O2)**: ~0.3-0.5 seconds for n=500 dense cases
- **Python (CPython 3.x)**: ~1.2-1.8 seconds for n=500 dense cases
- **Performance Gap**: Approximately 2.5-3.0x slower execution in Python

This performance differential creates systematic evaluation bias where algorithmically identical solutions receive different verdicts based solely on implementation language.
