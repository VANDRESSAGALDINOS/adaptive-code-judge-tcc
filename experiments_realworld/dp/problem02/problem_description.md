# CSES 1638 - Grid Paths I

## Problem Details
- **Platform**: CSES Problem Set
- **Problem ID**: 1638
- **Problem Name**: Grid Paths I
- **Link**: https://cses.fi/problemset/task/1638
- **Time Limit**: 1.00 s
- **Memory Limit**: 512 MB
- **Category**: Dynamic Programming (2D DP)

## Description
Consider an n × n grid whose squares may have traps. It is not allowed to move to a square with a trap.
Your task is to calculate the number of paths from the upper-left square to the lower-right square. You can only move right or down.

## Input Format
- The first input line has an integer n: the size of the grid.
- After this, there are n lines that describe the grid. Each line has n characters: '.' denotes an empty cell, and '*' denotes a trap.

## Output Format
Print the number of paths modulo 10^9+7.

## Constraints
- 1 ≤ n ≤ 1000

## Sample Input/Output
```
Input:
4
....
.*..
...*
*...

Output:
3
```

## Algorithm Approach
- **Type**: 2D Dynamic Programming
- **Complexity**: O(n²) time, O(n²) space
- **Core Logic**: dp[i][j] = dp[i-1][j] + dp[i][j-1] if grid[i][j] != '*'
- **Base Cases**: dp[0][0] = 1 if grid[0][0] != '*'
