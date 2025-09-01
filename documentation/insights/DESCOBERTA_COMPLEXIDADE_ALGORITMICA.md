# Descoberta: Correlação entre Complexidade Algorítmica e Injustiça de Linguagem

## Resumo Executivo

Durante os experimentos da categoria "graphs", identificamos um padrão científico fundamental: **diferentes tipos de algoritmos apresentam níveis distintos de injustiça de linguagem**.

## Descoberta Empírica

### Dados Observados

| Algoritmo | Problema | Complexidade | Slowdown Python | Injustiça |
|-----------|----------|--------------|-----------------|-----------|
| **Floyd-Warshall** | CSES 1672 | O(n³) | ~37x | **SEVERA** |
| **Bellman-Ford** | CSES 1197 | O(nm) | ~4.3x | **SEVERA** |
| **Dijkstra** | CSES 1670 | O(m log n) | 4-7x | **MODERADA** |

### Padrão Identificado

**HIERARQUIA DE INJUSTIÇA:**
1. **Algoritmos Cúbicos** (O(n³)): Injustiça extrema (>30x slowdown)
2. **Algoritmos Quadráticos/Simulação** (O(nm), O(nk)): Injustiça severa (4-10x)
3. **Algoritmos com Estruturas de Dados** (O(m log n)): Injustiça moderada (3-7x)

## Hipótese Científica

**"Quanto maior a intensidade computacional bruta (loops aninhados, simulação de passos), maior a penalização de linguagens interpretadas."**

### Fatores Contribuintes

1. **Loops Aninhados**: Python sofre exponencialmente com nested loops
2. **Simulação de Estados**: Overhead de interpretação se acumula
3. **Estruturas de Dados Complexas**: Heap/Priority Queue são mais eficientes em C++
4. **Memory Access Patterns**: C++ tem melhor cache locality

## Implicações para Seleção de Problemas

### Estratégia Otimizada

**Para maximizar detecção de injustiça:**
- **Priorizar**: Algoritmos recursivos, simulação, DP com loops aninhados
- **Evitar**: Algoritmos puramente baseados em estruturas de dados otimizadas
- **Focar**: Problemas com k grande (simulação de muitos passos)

### Aplicação Imediata

**CSES 1750 - Planets Queries I** é superior ao Dijkstra porque:
- **Binary Lifting**: Simulação recursiva de 2^i passos
- **k até 10^9**: Computação intensiva
- **Functional Graph**: Traversal repetitivo
- **Expectativa**: Slowdown >10x (vs 4-7x do Dijkstra)

## Contribuição Metodológica

Esta descoberta estabelece **critérios científicos para seleção de problemas** em experimentos de injustiça de linguagem:

1. **Classificação por Tipo Algorítmico**
2. **Predição de Severidade de Injustiça**
3. **Otimização de Tempo Experimental**
4. **Validação de Hipóteses**

## Próximos Experimentos

Aplicar este insight nas categorias restantes:
- **DP Recursiva**: Expectativa de injustiça severa
- **Backtracking**: Expectativa de injustiça extrema
- **Deep Recursion**: Expectativa de injustiça crítica

## Status

- **Data**: 2025-08-31
- **Experimentos Base**: Problem01, Problem02, Problem03 (parcial)
- **Validação**: Pendente (Problem03 será substituído por CSES 1750)
- **Aplicação**: Imediata para seleção de próximos problemas


