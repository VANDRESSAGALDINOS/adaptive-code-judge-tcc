# CSES Validation Results - Problem03 Two Sets II Recursivo

## Submissões Realizadas

### 1. C++ Recursivo Otimizado
- **Status**: ACCEPTED
- **Data**: 2025-09-01 00:28:57 +0300
- **Linguagem**: C++ (C++11)
- **Resultado**: 24/24 testes aprovados
- **Performance**: 0.00s - 0.52s
- **TLE Rate**: 0%

### 2. Python Recursivo Otimizado - **INJUSTIÇA CONFIRMADA**
- **Status**: TIME LIMIT EXCEEDED
- **Data**: 2025-09-01 00:27:43 +0300
- **Linguagem**: Python3 (CPython3)
- **Resultado**: 18/24 testes aprovados
- **Falhas**: Testes #17, #19, #20, #21, #23, #24 (TLE)
- **TLE Rate**: 25%
- **Performance**: 0.02s - 0.59s (testes aprovados)

### 3. C++ Slow Recursivo
- **Status**: TIME LIMIT EXCEEDED
- **Data**: 2025-09-01 00:33:49 +0300
- **Linguagem**: C++ (C++11)
- **Resultado**: 15/24 testes aprovados
- **Falhas**: Testes #11, #12, #15, #17, #19, #20, #21, #23, #24 (TLE)
- **TLE Rate**: 37.5%
- **Overhead**: EXTRA_WORK = 2000

### 4. Python Slow Recursivo
- **Status**: TIME LIMIT EXCEEDED
- **Data**: 2025-09-01 00:34:39 +0300
- **Linguagem**: Python3 (CPython3)
- **Resultado**: 15/24 testes aprovados
- **Falhas**: Testes #11, #12, #15, #17, #19, #20, #21, #23, #24 (TLE)
- **TLE Rate**: 37.5%
- **Overhead**: EXTRA_WORK = 2000

## Análise da Injustiça Algorítmica

### Disparidade Confirmada
**Python Recursivo vs C++ Recursivo**: 25% vs 0% TLE rate demonstra injustiça significativa em algoritmos recursivos de DP.

### Casos Críticos Identificados
**Testes Problemáticos**: #17, #19, #20, #21, #23, #24
- Representam cenários computacionalmente intensivos para recursão
- Python falha consistentemente onde C++ executa normalmente
- Padrão sugere overhead específico de recursão profunda

### Seletividade do Sistema Preservada
**Slow Solutions**: 37.5% TLE rate em ambas linguagens
- Sistema detecta adequadamente overhead intencional
- Casos críticos expandem de 6 para 9 (incluem #11, #12, #15)
- Metodologia de detecção de soluções ineficientes validada

## Descobertas Científicas

### 1. Injustiça Severa em DP Recursivo
Two Sets II apresenta injustiça mais severa que Grid Paths (25% vs 13.3% TLE rate), indicando que complexidade algorítmica amplifica disparidades.

### 2. Padrão de Casos Críticos
Identificação precisa de casos específicos que causam overhead, permitindo análise targeted de características problemáticas.

### 3. Validação Metodológica
Slow solutions confirmam que sistema mantém capacidade de detectar soluções ineficientes, preservando integridade acadêmica.

## Comparação com Experimentos Anteriores

| Problema | Python TLE Rate | Casos Críticos | Complexidade |
|----------|----------------|-----------------|--------------|
| **Grid Paths Recursivo** | 13.3% | 2/15 | O(n²) |
| **Two Sets II Recursivo** | **25%** | **6/24** | **O(n×sum)** |

**Descoberta**: Maior complexidade algorítmica resulta em injustiça mais severa.

## Status da Fase 1

✅ **FASE 1 CONCLUÍDA**: Validação Externa CSES completa (4/4 submissões)

**Próxima Fase**: Benchmark Local Controlado para quantificar precisamente a disparidade e desenvolver fator de ajuste.
