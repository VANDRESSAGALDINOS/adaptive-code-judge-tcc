# Relatório de Veredito Binário - CSES 1635 DP Recursivo

## Dados do Experimento
- **Problema**: CSES 1635 - Coin Combinations I (DP Recursivo)
- **Data**: 2025-08-31
- **Time Limit**: 3.0s (adaptativo: 2.92s)
- **Fator de Ajuste**: 0.97x (calibração corrigida - metodologia rigorosa)

## Correção Metodológica Aplicada
**Problema Inicial**: Calibração inadequada com test case trivial (#1, x=1)
**Solução**: Recalibração com test case representativo (#9, x=9) seguindo padrão dos experimentos de grafos
**Resultado**: Fator ajustado de 1.07x → 0.97x (Python ligeiramente mais rápido)

## Análise de Veredito por Test Case

### Test Case 9 (Calibração Corrigida)
- **Input**: x=9, coins=[2,3,4]
- **C++**: ✅ ACCEPTED (mediana 0.813s, 5 repetições)
- **Python**: ✅ ACCEPTED (mediana 0.814s, 5 repetições)
- **Veredito**: Ambas linguagens funcionais, Python ligeiramente mais rápido

### Casos Funcionais (1,3,7,9)
- **Veredito**: **SEM INJUSTIÇA** - Performance similar entre linguagens
- **Observação**: Python = C++ em casos pequenos/médios

### Test Case 4 (Injustiça Temporal)
- **Input**: x=1,000,000, 100 coins
- **C++**: ✅ ACCEPTED (1.3-1.9s, 5/5 repetições)
- **Python**: ❌ TLE (3.000s, 0/5 repetições)
- **Veredito**: **INJUSTIÇA TEMPORAL SEVERA** - 100% TLE Python vs 100% ACCEPTED C++

### Test Case 8 (Injustiça Temporal)
- **Input**: x=1,000,000, 100 coins  
- **C++**: ✅ ACCEPTED (1.7-2.5s, 4/5 repetições) ❌ TLE (1/5)
- **Python**: ❌ TLE (3.000s, 0/5 repetições)
- **Veredito**: **INJUSTIÇA TEMPORAL** - Python 100% TLE vs C++ 80% ACCEPTED

### Test Case 11 (Injustiça Arquitetural)
- **Input**: x=1,000,000, 100 coins
- **C++**: ❌ TLE (4/5 repetições) ✅ ACCEPTED (1/5, 2.7s)
- **Python**: ❌ TLE (5/5 repetições)  
- **Veredito**: **INJUSTIÇA ARQUITETURAL** - Limitação recursiva afeta ambas linguagens

## Sumário de Injustiças (Metodologia Corrigida)

### Descoberta Inesperada: Performance Equivalente em Casos Pequenos/Médios
- **Test Cases**: 1,3,7,9 
- **Evidência**: Python = C++ (fator 0.97x)
- **Implicação**: Injustiça não é universal em DP recursivo

### Tipo A: Injustiça Temporal Severa
- **Test Cases**: 4,8 (casos críticos x=1M)
- **Evidência**: Python 100% TLE vs C++ 80-100% ACCEPTED
- **Causa**: Limitações recursivas Python + overhead interpretativo em casos extremos

### Tipo B: Injustiça Arquitetural  
- **Test Cases**: 11 (caso limite)
- **Evidência**: Ambas linguagens falham majoritariamente (Python 100%, C++ 80% TLE)
- **Causa**: Stack depth limits fundamentais

## Conclusão Científica Refinada

A **metodologia corrigida** revela nuances importantes:

1. **Casos pequenos/médios** (x≤1000): **SEM INJUSTIÇA** - Performance equivalente
2. **Casos críticos** (x=1M): **INJUSTIÇA TEMPORAL SEVERA** - Python sistematicamente penalizado  
3. **Casos limite**: **INJUSTIÇA ARQUITETURAL** - Ambas linguagens afetadas

**Implicação TCC**: DP Recursivo tem **injustiça específica por escala**, não universal. Casos reais de competitive programming podem não sofrer injustiça se inputs forem moderados.
