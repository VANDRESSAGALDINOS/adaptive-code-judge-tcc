# Problem Description - CSES 1750 Planets Queries I

## Problem Details
- **Platform**: CSES
- **Problem ID**: 1750
- **Problem Name**: Planets Queries I
- **Time Limit**: 1.00 s
- **Memory Limit**: 512 MB
- **Category**: Graph Algorithms (Binary Lifting / Functional Graph)

## Description
You are playing a game consisting of n planets. Each planet has a teleporter to another planet (or the planet itself).
Your task is to process q queries of the form: when you begin on planet x and travel through k teleporters, which planet will you reach?

## Algorithm
**Binary Lifting on Functional Graph** - Efficient k-step traversal
- **Time Complexity**: O(n log k + q log k) where k can be up to 10^9
- **Space Complexity**: O(n log k)
- **Key Insight**: Precompute 2^i steps for efficient jumping

## Input Format
- First line: n (planets) and q (queries)
- Second line: n integers t_i (teleporter destinations)
- Next q lines: x k (start planet x, travel k steps)

## Output Format
- For each query, print the destination planet after k teleporters

## Constraints
- 1 ≤ n, q ≤ 200,000
- 1 ≤ t_i ≤ n
- 1 ≤ x ≤ n
- 0 ≤ k ≤ 1,000,000,000

## Sample Input/Output
```
Input:
4 3
2 1 1 4
1 2
3 4
4 1

Output:
1
2
4
```

## Expected Injustice Level
Based on algorithmic complexity discovery: **SEVERA** (Binary lifting + simulation expected >10x slowdown)