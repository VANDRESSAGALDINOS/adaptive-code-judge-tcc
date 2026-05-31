# CSES 1635 - Coin Combinations I

## Problem Specification

**Source**: CSES Problem Set  
**Problem ID**: 1635  
**Category**: Dynamic Programming  
**Difficulty**: Easy  
**Time Limit**: 1.00s  
**Memory Limit**: 512 MB  

## Problem Statement

Consider a money system consisting of n coins. Each coin has a positive integer value. Your task is to calculate the number of distinct ways you can produce a money sum x using the available coins.

For example, if the coins are {2,3,5} and the desired sum is 9, there are 8 ways:
- 2+2+5
- 2+5+2  
- 5+2+2
- 3+3+3
- 2+2+2+3
- 2+2+3+2
- 2+3+2+2
- 3+2+2+2

## Input Format

The first line has two integers n and x: the number of coins and the desired sum of money.

The second line has n integers c₁,c₂,...,cₙ: the value of each coin.

## Output Format

Print one integer: the number of ways modulo 10⁹+7.

## Constraints

- 1 ≤ n ≤ 100
- 1 ≤ x ≤ 10⁶
- 1 ≤ cᵢ ≤ 10⁶

## Example

**Input:**
```
3 9
2 3 5
```

**Output:**
```
8
```

## Algorithmic Analysis

### Mathematical Formulation

Let f(x) = number of ways to form sum x using available coins.

**Recurrence Relation**:
f(x) = Σ f(x - cᵢ) for all i where x ≥ cᵢ

**Base Case**: f(0) = 1 (one way to form sum 0: use no coins)

**Boundary Condition**: f(x) = 0 for x < 0

### Implementation Approaches

#### 1. Iterative Dynamic Programming (Bottom-Up)
- Compute f(0), f(1), ..., f(x) in ascending order
- Time Complexity: O(n × x)
- Space Complexity: O(x)

#### 2. Recursive Dynamic Programming (Top-Down)  
- Compute f(x) recursively with memoization
- Time Complexity: O(n × x)
- Space Complexity: O(x) + O(x) stack space

### Complexity Analysis

**Time Complexity**: O(n × x)
- Each state from 0 to x is computed exactly once
- Each computation requires checking n coins

**Space Complexity**: O(x)
- DP table or memoization array of size x+1
- Additional O(x) recursion stack for recursive approach

### Problem Characteristics

- **Combinatorial Counting**: Classic DP counting problem
- **Overlapping Subproblems**: Many ways to reach the same sum
- **Optimal Substructure**: Solution depends on optimal solutions to subproblems
- **Order Significance**: Different orderings count as distinct ways

## Research Relevance

This problem serves as an ideal testbed for comparing iterative versus recursive dynamic programming implementations because:

1. **Clear Equivalence**: Both approaches implement identical recurrence relation
2. **Measurable Differences**: Implementation overhead can be quantified
3. **External Validation**: CSES platform provides objective verification
4. **Moderate Complexity**: Suitable for controlled performance analysis

The problem allows investigation of how implementation approach affects language-specific performance characteristics while maintaining mathematical equivalence.

---

**Platform Reference**: [CSES 1635](https://cses.fi/problemset/task/1635)  
**Algorithm Category**: Dynamic Programming  
**Research Focus**: Implementation approach comparison  
**Validation Method**: External platform submission
