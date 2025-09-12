# Limitações Arquiteturais da Recursão em Programação Dinâmica

## Descoberta Científica

Durante a implementação de algoritmos de programação dinâmica recursiva (top-down) com memoização, foi identificada uma limitação arquitetural fundamental que distingue linguagens compiladas de interpretadas em contextos de recursão profunda.

## Contexto Experimental

**Problema analisado**: CSES 1635 - Coin Combinations I  
**Algoritmo**: Programação Dinâmica Recursiva com Memoização  
**Complexidade**: O(n × x) tempo, O(x) espaço + O(x) stack  
**Constraints**: x ≤ 10^6

## Observação Empírica

### Implementação C++ Recursiva
**Status**: ACCEPTED  
**Performance**: Margem estreita (0.47s de 1.0s nos casos críticos)  
**Stack profundidade**: Suporta até x = 10^6 sem modificações

### Implementação Python Recursiva
**Status**: RUNTIME ERROR (RecursionError)  
**Falha**: Stack overflow em casos com x ≥ 10^6  
**Limitação**: `sys.setrecursionlimit()` mesmo ajustado para 1.100.000 não resolve casos patológicos

## Análise da Causa Raiz

### Diferenças Arquiteturais

**C++ (Linguagem Compilada)**:
- Stack nativo do sistema operacional
- Gerenciamento direto de memória
- Overhead mínimo por chamada de função
- Capacidade de stack limitada apenas por memória física

**Python (Linguagem Interpretada)**:
- Stack virtualizado no interpretador
- Verificações de segurança em cada chamada
- Overhead significativo por frame de função
- Limite artificial de recursão para prevenção de crash

### Caso Patológico Identificado

**Input crítico**: n=1, x=1.000.000, coins=[1]  
**Profundidade de stack requerida**: Exatamente 1.000.000 níveis  
**Resultado**:
- C++: Execução bem-sucedida
- Python: RecursionError mesmo com limite elevado

## Implicações Metodológicas

### Para Comparação de Linguagens

Esta descoberta revela que certas categorias algorítmicas apresentam incompatibilidade arquitetural fundamental, não apenas diferenças de performance. Em algoritmos recursivos profundos:

1. **C++** pode executar algoritmos que **Python não consegue completar**
2. A comparação deixa de ser temporal (injustiça) e torna-se **viabilidade técnica**
3. Algoritmos recursivos demonstram **limitação categórica** de linguagens interpretadas

### Para Sistemas de Julgamento Online

**Problemas com recursão profunda** criam barreira intransponível para submissões Python, independentemente de otimizações de código. Isto constitui injustiça qualitativa, não apenas quantitativa.

## Estratégia de Mitigação Proposta

### Metodologia Adaptativa

Para problemas onde recursão apresenta limitações arquiteturais:

1. **Manter implementação recursiva** como prova de conceito das limitações
2. **Implementar versão iterativa equivalente** para comparação justa de performance
3. **Documentar ambos os resultados** como evidências complementares

### Categorização de Injustiças

**Tipo A - Injustiça Temporal**: Ambas linguagens executam, Python mais lento  
**Tipo B - Injustiça Arquitetural**: Python incapaz de executar algoritmo viável em C++

## Contribuição Científica

Esta descoberta fortalece a tese principal ao demonstrar que injustiças em sistemas de julgamento online operam em múltiplas dimensões:

1. **Performance relativa** (fator de tempo)
2. **Viabilidade algorítmica** (capacidade de execução)
3. **Limitações arquiteturais** (diferenças fundamentais entre paradigmas de linguagem)

O sistema adaptativo proposto deve considerar não apenas fatores de tempo, mas também viabilidade técnica por categoria algorítmica.

## Validação Experimental

**Data**: 2025-08-31  
**Plataforma**: CSES Online Judge  
**Reprodutibilidade**: Casos documentados em `/experiments_realworld/dp/problem01_recursivo/`  
**Status**: Descoberta validada e incorporada à metodologia












