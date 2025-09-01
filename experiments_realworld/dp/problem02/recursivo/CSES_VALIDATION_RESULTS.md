# CSES Validation Results - Problem02 Recursivo

## Submissões Realizadas

### 1. C++ Recursivo Otimizado
- **Status**: ACCEPTED
- **Data**: 2025-08-31 23:07:49 +0300
- **Linguagem**: C++ (C++11)
- **Resultado**: 15/15 testes aprovados
- **Performance**: 0.01s - 0.03s

### 2. Python Recursivo Otimizado  
- **Status**: TIME LIMIT EXCEEDED
- **Data**: 2025-08-31 23:08:41 +0300
- **Linguagem**: Python3 (CPython3)
- **Resultado**: 13/15 testes aprovados
- **Falhas**: Testes #6, #7 (TLE)
- **Performance**: 0.02s - 0.99s (testes aprovados)

## Análise Preliminar

**Disparidade Observada**: C++ recursivo executa completamente, Python recursivo falha em casos críticos.

**Casos Críticos Identificados**: Testes #6 e #7 representam cenários computacionalmente intensivos para recursão em Python.

### 3. C++ Slow Recursivo (Corrigido)
- **Status**: TIME LIMIT EXCEEDED
- **Data**: 2025-08-31 23:41:23 +0300
- **Linguagem**: C++ (C++11)
- **Resultado**: 11/15 testes aprovados
- **Falhas**: Testes #6, #7, #8, #9 (TLE)
- **TLE Rate**: 26.7%
- **Overhead**: EXTRA_WORK = 2000

### 4. Python Slow Recursivo
- **Status**: TIME LIMIT EXCEEDED  
- **Data**: 2025-08-31 23:42:29 +0300
- **Linguagem**: Python3 (CPython3)
- **Resultado**: 11/15 testes aprovados
- **Falhas**: Testes #6, #7, #8, #9 (TLE)
- **TLE Rate**: 26.7%
- **Overhead**: EXTRA_WORK = 2000

## Análise da Seletividade

**Casos Críticos Identificados**: Testes #6-#9 consistentemente causam TLE em soluções com overhead.

**Seletividade Validada**: Slow solutions apresentam falhas sistemáticas nos mesmos casos críticos.

**Metodologia Confirmada**: Sistema distingue adequadamente entre soluções otimizadas e ineficientes.

## Status da Fase 1

✅ **FASE 1 CONCLUÍDA**: Validação Externa CSES completa (4/4 submissões)
