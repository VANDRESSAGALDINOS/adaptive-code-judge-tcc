# CSES Validation Results - Problem02 Iterativo

## Submissões Realizadas

### 1. C++ Iterativo Otimizado
- **Status**: ACCEPTED
- **Data**: 2025-09-01 00:06:40 +0300
- **Linguagem**: C++ (C++11)
- **Resultado**: 15/15 testes aprovados
- **Performance**: 0.00s - 0.02s
- **Observação**: Performance superior ao recursivo

### 2. Python Iterativo Otimizado - **DESCOBERTA CRÍTICA**
- **Status**: ACCEPTED ✨
- **Data**: 2025-09-01 00:07:20 +0300
- **Linguagem**: Python3 (CPython3)
- **Resultado**: 15/15 testes aprovados
- **Performance**: 0.02s - 0.49s
- **Observação**: **NENHUM TLE - Eliminação completa da injustiça**

### 3. C++ Slow Iterativo
- **Status**: TIME LIMIT EXCEEDED
- **Data**: 2025-09-01 00:08:05 +0300
- **Linguagem**: C++ (C++11)
- **Resultado**: 10/15 testes aprovados
- **Falhas**: Testes #6-#10 (TLE)
- **TLE Rate**: 33.3%
- **Overhead**: EXTRA_WORK = 2000

### 4. Python Slow Iterativo
- **Status**: TIME LIMIT EXCEEDED
- **Data**: 2025-09-01 00:08:52 +0300
- **Linguagem**: Python3 (CPython3)
- **Resultado**: 10/15 testes aprovados
- **Falhas**: Testes #6-#10 (TLE)
- **TLE Rate**: 33.3%
- **Overhead**: EXTRA_WORK = 2000

## Análise Comparativa: Recursivo vs Iterativo

### Injustiça Algorítmica - Eliminação Completa

| Abordagem | Python TLE Rate | Casos Críticos | Status |
|-----------|----------------|-----------------|---------|
| **DP Recursivo** | 13.3% | #6, #7 falham | Injustiça confirmada |
| **DP Iterativo** | **0%** | **Todos passam** | **Injustiça eliminada** |

### Descoberta Metodológica

**Causa Raiz Identificada**: O overhead de recursão em Python é o fator determinante da injustiça algorítmica em DP.

**Evidência**: Eliminação total de TLE ao migrar de recursão para iteração mantendo lógica algorítmica idêntica.

### Implicações Científicas

1. **Especificidade do Overhead**: Injustiça não é inerente ao algoritmo DP, mas à implementação recursiva
2. **Solução Algorítmica**: Migração para DP iterativo resolve completamente a disparidade
3. **Validação Metodológica**: Comparação direta confirma causa raiz

## Seletividade Preservada

**Slow Solutions**: Ambas linguagens apresentam 33.3% TLE rate, confirmando que sistema detecta adequadamente soluções ineficientes.

## Status da Fase 1

✅ **FASE 1 CONCLUÍDA**: Validação Externa CSES completa (4/4 submissões)

**Descoberta Principal**: **DP Iterativo elimina completamente a injustiça observada no DP Recursivo**
