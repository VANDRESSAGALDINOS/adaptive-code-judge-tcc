# Problem02: Grid Paths (CSES 1625)

## Descrição do Problema

**CSES Problem ID**: 1625  
**Nome**: Grid Path Description  
**Categoria**: Backtracking  
**Dificuldade**: Extremely Hard  

### Enunciado

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

## Análise Algorítmica

### Complexidade
- **Teórica**: O(4^48) sem podas
- **Prática**: Drasticamente reduzida com podas avançadas
- **Espaço**: O(1) - apenas grid 7x7 e recursão

### Técnicas de Otimização Necessárias

1. **Poda de Dead End Diagonal**: Detectar células com <2 vizinhos livres
2. **Poda de Trap/Corredor**: Detectar divisões que isolam regiões
3. **Poda de Distância**: Verificar se passos restantes são suficientes
4. **Early Termination**: Parar ao atingir destino

### Características do Problema

- **Grid fixo**: 7x7 (49 células)
- **Caminho fixo**: Exatamente 48 passos
- **Início**: (0,0) - canto superior esquerdo  
- **Destino**: (6,0) - canto inferior esquerdo
- **Wildcards**: '?' pode ser qualquer direção

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
