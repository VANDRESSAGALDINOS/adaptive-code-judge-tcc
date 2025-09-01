# CSES - Two Sets II

## Problem Details
- **Platform**: CSES Problem Set
- **Problem Name**: Two Sets II
- **Link**: https://cses.fi/problemset/task/1093
- **Time Limit**: 1.00 s
- **Memory Limit**: 512 MB
- **Category**: Dynamic Programming (Subset Sum DP)

## Description
Your task is to count the number of ways numbers 1,2,...,n can be divided into two sets of equal sum.

For example, if n=7, there are four solutions:
- {1,3,4,6} and {2,5,7}
- {1,2,5,6} and {3,4,7}
- {1,2,4,7} and {3,5,6}
- {1,6,7} and {2,3,4,5}

## Input Format
The only input line contains an integer n.

## Output Format
Print the answer modulo 10^9+7.

## Constraints
- 1 ≤ n ≤ 500

## Sample Input/Output
```
Input:
7

Output:
4
```

## Algorithm Approach

### Recursivo (Top-down com memoização)
- **Type**: 2D Dynamic Programming - Recursivo
- **Complexity**: O(n × sum) tempo, O(n × sum) espaço
- **Core Logic**: 
  ```
  count_ways(i, target) = count_ways(i-1, target) + count_ways(i-1, target-i)
  ```
- **Base Cases**: target=0 → 1, i≤0 ou target<0 → 0

### Iterativo (Bottom-up com tabulation)
- **Type**: 2D Dynamic Programming - Iterativo  
- **Complexity**: O(n × sum) tempo, O(n × sum) espaço
- **Core Logic**: Preencher tabela dp[i][j] bottom-up
- **Otimização**: Divisão por 2 usando inversão modular

## Injustiça Confirmada - Resultados CSES

### Validação Externa Inicial
| Solução | Status | TLE Rate | Casos Críticos |
|---------|--------|----------|-----------------|
| **C++ Recursivo** | ACCEPTED | 0% | Todos passam (0.52s máximo) |
| **Python Recursivo** | TLE | **25%** | **6/24 casos falharam** |

### Descoberta Científica
**Injustiça Algorítmica Confirmada**: Python recursivo falha em 25% dos casos onde C++ executa normalmente, demonstrando overhead significativo de recursão.

## Hipótese Experimental

**Baseado na descoberta do Problem02**: 
- **DP Recursivo**: Injustiça severa confirmada (25% TLE rate)
- **DP Iterativo**: Esperamos eliminação da injustiça (fator próximo a 1.0x)

**Diferencial do Two Sets II**: 
- **Complexidade alta**: n×sum subproblemas (até 500×62500)
- **Recursão profunda**: Overhead significativo em Python
- **Casos críticos bem definidos**: 6 casos específicos causam TLE