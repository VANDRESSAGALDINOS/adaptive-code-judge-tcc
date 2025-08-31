# CSES 1197 - Cycle Finding

## Problem Statement

You are given a directed graph, and your task is to find out if it contains a negative cycle, and also give an example of such a cycle.

## Input Format
- First line: two integers n and m (number of nodes and edges)
- Next m lines: three integers a, b, c (edge from node a to node b with weight c)

## Output Format
- If negative cycle exists: print "YES" followed by the cycle nodes in correct order
- If no negative cycle: print "NO"

## Constraints
- 1 ≤ n ≤ 2500
- 1 ≤ m ≤ 5000
- 1 ≤ a,b ≤ n
- -10^9 ≤ c ≤ 10^9

## Example
```
Input:
4 5
1 2 1
2 4 1
3 1 1
4 1 -3
4 3 -2

Output:
YES
1 2 4 1
```

## Algorithm Analysis

### Optimal Solution: Bellman-Ford Algorithm
- **Time Complexity**: O(nm) where n = nodes, m = edges
- **Space Complexity**: O(n + m)
- **Core Operations**: Edge relaxation, distance updates, cycle detection

### Key Algorithmic Steps
1. Initialize distances from implicit super-source
2. Perform n iterations of edge relaxation
3. Check for negative cycle in nth iteration
4. If cycle found, reconstruct and output cycle path

### Performance Characteristics
- **Loop Structure**: Nested loops over iterations and edges
- **Memory Access**: Sequential edge traversal, random distance updates
- **Computational Load**: Integer arithmetic, comparisons, array indexing

## Expected Language Performance Gap
Based on algorithmic characteristics, Python is expected to suffer from:
- Interpreter overhead in nested loops
- Dynamic typing costs in arithmetic operations
- Memory access patterns less optimized than compiled code

## Reference Links
- Problem URL: https://cses.fi/problemset/task/1197/
- Algorithm Reference: Bellman-Ford negative cycle detection