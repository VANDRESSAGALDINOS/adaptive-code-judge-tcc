# CSES 1624 - Chessboard and Queens

## Descrição do Problema

**Fonte**: CSES Problem Set  
**ID**: 1624  
**Categoria**: Backtracking  
**Dificuldade**: Médio  
**Limite de Tempo**: 1.00s  
**Limite de Memória**: 512 MB  

## Enunciado

Sua tarefa é colocar oito rainhas em um tabuleiro de xadrez de forma que nenhuma das duas rainhas esteja atacando uma à outra. Como desafio adicional, cada quadrado é livre (.) ou reservado (*), e você só pode colocar rainhas nos quadrados livres. No entanto, os quadrados reservados não impedem que as rainhas se ataquem.

Quantas maneiras possíveis existem para colocar as rainhas?

## Entrada

A entrada tem oito linhas, e cada uma delas tem oito caracteres. Cada quadrado é livre (.) ou reservado (*).

## Saída

Imprima um inteiro: o número de maneiras que você pode colocar as rainhas.

## Exemplo

**Entrada:**
```
........
........
..*.....
........
........
.....**.
...*....
........
```

**Saída:**
```
65
```

## Análise Algorítmica

### Abordagem: Backtracking Clássico

**Algoritmo**:
1. Colocar rainhas linha por linha (uma por linha)
2. Para cada posição, verificar se é válida:
   - Quadrado não é reservado (*)
   - Não há conflito com rainhas já colocadas
3. Usar arrays booleanos para otimizar verificação:
   - `col_used[col]`: coluna ocupada
   - `diag1_used[row - col + 7]`: diagonal principal
   - `diag2_used[row + col]`: diagonal secundária
4. Backtrack quando não há posições válidas

### Complexidade

**Temporal**: O(8!) no pior caso, mas com poda eficiente  
**Espacial**: O(8) para arrays de controle + O(8) para stack de recursão  

### Características do Problema

- **Tamanho fixo**: 8x8 (não escala)
- **Poda intensa**: Verificações de conflito eliminam muitas possibilidades
- **Recursão limitada**: Máximo 8 níveis de profundidade
- **Determinístico**: Mesmo input sempre produz mesmo output

## Relevância para Estudo de Injustiça Algorítmica

### Hipóteses Iniciais

1. **Recursão intensiva** pode causar overhead em Python
2. **Backtracking** com múltiplas chamadas pode amplificar disparidades
3. **Verificações frequentes** podem favorecer C++ compilado

### Resultados Observados

**Injustiça Algorítmica**: ❌ Não observada  
**Seletividade Diferencial**: ✅ Confirmada  

- Ambas linguagens executam algoritmo otimizado com sucesso
- Python demonstra sensibilidade extrema ao overhead intencional (70% TLE)
- C++ tolera mesmo overhead com degradação controlada (~7x)

### Significância Científica

Este problema revela um novo tipo de disparidade: **seletividade diferencial ao overhead**, complementando os casos de injustiça algorítmica observados em problemas de DP. A descoberta sugere que sistemas de avaliação podem inadvertidamente penalizar Python mesmo quando algoritmos são algoritmicamente equivalentes e corretos.
