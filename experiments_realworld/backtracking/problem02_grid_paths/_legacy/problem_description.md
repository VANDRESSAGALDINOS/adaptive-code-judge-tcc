# Problem02: Grid Paths (CSES 1625)

## Problem Definition

**CSES Problem ID**: 1625  
**Name**: Grid Paths  
**Category**: Backtracking  
**Difficulty**: Extremely Hard  

### Problem Statement

There are 88418 paths in a 7×7 grid from the upper-left square to the lower-left square. Each path corresponds to a 48-character description consisting of characters D (down), U (up), L (left) and R (right).

For example, the path corresponds to the description:
`DRURRRRRDDDLUULDDDLDRRURDDLLLLLURULURRUULDLLDDDD`

You are given a description of a path which may also contain characters ? (any direction). Your task is to calculate the number of paths that match the description.

### Input
The only input line has a 48-character string of characters ?, D, U, L and R.

### Output
Print one integer: the total number of paths.

### Example
**Input:**
```
??????R??????U??????????????????????????LD????D?
```

**Output:**
```
201
```

## Algorithmic Analysis

### Complexity Analysis
- **Theoretical**: O(4^48) without pruning
- **Practical**: Significantly reduced with advanced pruning strategies
- **Space**: O(1) - only 7x7 grid and recursion stack

### Required Optimization Techniques

1. **Dead-end Diagonal Pruning**: Detect cells with <2 free neighbors
2. **Corridor/Trap Pruning**: Detect divisions that isolate grid regions
3. **Distance Pruning**: Verify if remaining steps are sufficient
4. **Early Termination**: Stop when destination is reached

### Problem Characteristics

- **Fixed Grid**: 7x7 (49 cells)
- **Fixed Path Length**: Exactly 48 steps
- **Start**: (0,0) - upper-left corner  
- **Destination**: (6,0) - lower-left corner
- **Wildcards**: '?' can be any direction

## Implementação

### Abordagem
- **Backtracking recursivo** com podas agressivas
- **Visited array** para rastrear células ocupadas
- **Poda combinada** para máxima eficiência

### Desafios
- **Extremamente pesado computacionalmente**
- **Requer podas muito específicas** para passar no CSES
- **Python sofre severamente** com overhead de recursão
- **C++ requer otimizações avançadas** para evitar TLE

## Expectativas Experimentais

### Hipóteses
1. **Algorithmic Injustice Severa**: Python falhará em muitos casos
2. **Recursion Overhead Crítico**: Diferença de performance extrema
3. **Seletividade Alta**: Slow solutions causarão TLE massivo

### Métricas Esperadas
- **C++ Otimizado**: ACCEPTED (100%)
- **Python Otimizado**: TLE significativo (>50%)
- **C++ Slow**: TLE parcial
- **Python Slow**: TLE massivo (>90%)

## Status do Experimento

- [ ] Códigos otimizados implementados
- [ ] Códigos slow implementados  
- [ ] Submissões CSES realizadas (4/4)
- [ ] Benchmarks locais executados
- [ ] Análise final concluída
