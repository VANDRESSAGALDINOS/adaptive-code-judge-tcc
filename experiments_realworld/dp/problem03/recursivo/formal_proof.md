# Prova Formal de Equivalência Algorítmica - LCS Recursivo

## Problema
**CSES - Longest Common Subsequence**: Encontrar a maior subsequência comum entre duas sequências de inteiros.

## Definição Formal

**Input**: 
- Sequência A = [a₁, a₂, ..., aₙ] de tamanho n
- Sequência B = [b₁, b₂, ..., bₘ] de tamanho m

**Output**: 
- Comprimento da LCS
- Uma LCS válida (qualquer uma se múltiplas existem)

**LCS Definition**: Uma subsequência S é comum a A e B se S pode ser obtida removendo elementos de ambas A e B mantendo a ordem relativa.

## Algoritmo Implementado
**Programação Dinâmica Recursiva (Top-down) com Memoização e Reconstrução**

## Prova de Equivalência

### Relação de Recorrência

**Estado**: `lcs(i,j)` = comprimento da LCS entre A[1..i] e B[1..j]

**Recorrência**:
```
lcs(i,j) = 0                           se i = 0 ou j = 0
         = 1 + lcs(i-1,j-1)            se A[i] = B[j]
         = max(lcs(i-1,j), lcs(i,j-1)) se A[i] ≠ B[j]
```

### Implementações

#### C++ (solution.cpp)
```cpp
int lcs(int i, int j) {
    if (i == 0 || j == 0) return 0;
    if (memo[i][j] != -1) return memo[i][j];
    
    int result;
    if (a[i-1] == b[j-1]) {
        result = 1 + lcs(i-1, j-1);
        parent[i][j] = 1; // Diagonal
    } else {
        int up = lcs(i-1, j);
        int left = lcs(i, j-1);
        if (up >= left) {
            result = up;
            parent[i][j] = 2; // Cima
        } else {
            result = left;
            parent[i][j] = 3; // Esquerda
        }
    }
    return memo[i][j] = result;
}
```

#### Python (solution.py)
```python
def lcs_recursive(i, j, a, b, memo, parent):
    if i == 0 or j == 0:
        return 0
    if memo[i][j] != -1:
        return memo[i][j]
    
    if a[i-1] == b[j-1]:
        result = 1 + lcs_recursive(i-1, j-1, a, b, memo, parent)
        parent[i][j] = 1  # Diagonal
    else:
        up = lcs_recursive(i-1, j, a, b, memo, parent)
        left = lcs_recursive(i, j-1, a, b, memo, parent)
        if up >= left:
            result = up
            parent[i][j] = 2  # Cima
        else:
            result = left
            parent[i][j] = 3  # Esquerda
    
    memo[i][j] = result
    return result
```

### Demonstração de Equivalência

**1. Mesma Relação de Recorrência:**
Ambas implementações seguem exatamente a mesma lógica:
- Casos base idênticos: i=0 ou j=0 → 0
- Caso match: A[i]=B[j] → 1 + lcs(i-1,j-1)
- Caso mismatch: max(lcs(i-1,j), lcs(i,j-1))

**2. Memoização Equivalente:**
- **C++**: `memo[i][j]` array 2D
- **Python**: `memo[i][j]` lista 2D
- Ambos verificam se valor já foi calculado antes de recursão

**3. Reconstrução da Solução:**
- **C++**: `parent[i][j]` armazena direção (1=diagonal, 2=cima, 3=esquerda)
- **Python**: `parent[i][j]` com mesma codificação
- Backtracking idêntico para construir LCS

**4. Complexidade Temporal:**
- **Ambos**: O(n×m) - cada estado calculado uma vez
- **Memoização**: Garante que lcs(i,j) é computado no máximo uma vez

**5. Complexidade Espacial:**
- **Ambos**: O(n×m) para memo + O(n×m) para parent = O(n×m)

## Diferenças de Implementação (Não Algorítmicas)

### Linguagem-Específicas
1. **Gerenciamento de Memória:**
   - C++: Arrays estáticos, memset para inicialização
   - Python: Listas dinâmicas, list comprehension

2. **Recursion Limit:**
   - C++: Limite de stack nativo (~10⁶ chamadas)
   - Python: sys.setrecursionlimit(2000000) necessário

3. **I/O Optimization:**
   - C++: ios::sync_with_stdio(false), cin.tie(nullptr)
   - Python: sys.stdin.buffer.read() para performance

### Overhead Esperado
Baseado na descoberta do Problem02:
- **Recursão em Python**: Overhead significativo esperado
- **Complexidade 2D**: Pode amplificar diferenças (n×m subproblemas)
- **Reconstrução**: Adiciona overhead de backtracking

## Prova de Corretude

### Teorema
As implementações C++ e Python produzem resultado idêntico para qualquer entrada válida.

### Demonstração por Indução

**Caso Base**: i=0 ou j=0
- Ambas retornam 0 ✓

**Passo Indutivo**: Assumindo corretude para estados menores
- **Caso A[i]=B[j]**: Ambas retornam 1 + lcs(i-1,j-1) ✓
- **Caso A[i]≠B[j]**: Ambas retornam max(lcs(i-1,j), lcs(i,j-1)) ✓

**Reconstrução**: 
- Parent tracking idêntico garante mesma LCS construída ✓

### Invariante
Para todo estado (i,j), memo[i][j] contém o comprimento correto da LCS entre A[1..i] e B[1..j].

## Expectativas para Experimento

### Hipótese Principal
Recursão em Python apresentará overhead em casos grandes (n,m próximos de 1000), similar ao observado no Problem02.

### Diferencial do LCS
- **Complexidade 2D**: n×m subproblemas vs n² no Grid Paths
- **Reconstrução**: Overhead adicional de backtracking
- **Arrays vs Grids**: Acesso a arrays pode ter padrão diferente

**Predição**: Injustiça moderada a severa no recursivo, eliminável no iterativo.
