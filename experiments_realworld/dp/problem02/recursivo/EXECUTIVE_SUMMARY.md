# Executive Summary - CSES 1638 Grid Paths I (DP Recursivo)

## Identificação do Experimento

**Problema**: CSES 1638 - Grid Paths I  
**Algoritmo**: Dynamic Programming Recursivo (Top-down com memoização)  
**Data**: 2025-08-31  
**Status**: SUCCESSFUL  

## Objetivo

Investigar disparidade de performance entre C++ e Python em algoritmos de programação dinâmica recursiva, utilizando metodologia científica rigorosa com validação externa via CSES.

## Metodologia Aplicada

### Fase 1: Validação Externa CSES
- **Submissões**: 4 códigos (C++/Python otimizados + slow)
- **Plataforma**: CSES Problem Set
- **Critério**: Validação independente de correção algorítmica

### Fase 2: Benchmark Local Controlado
- **Calibração**: Test Case 5 (10×10 grid)
- **Validação**: 3 casos representativos
- **Slow Validation**: 2 casos críticos
- **Ambiente**: Docker isolado

### Fase 3: Análise Estatística
- **Métricas**: Tempo de execução, taxa de sucesso, TLE rate
- **Fator de Ajuste**: 1.12x (empiricamente determinado)
- **Confiabilidade**: Alta

## Resultados Principais

### Validação Externa (CSES)
| Solução | Status | TLE Rate | Observações |
|---------|--------|----------|-------------|
| C++ Otimizado | ACCEPTED | 0% | Performance consistente |
| Python Otimizado | TLE | 13.3% | Falhas em casos #6, #7 |
| C++ Slow | TLE | 26.7% | Overhead detectado |
| Python Slow | TLE | 26.7% | Overhead detectado |

### Benchmark Local
- **Fator de Ajuste**: 1.12x
- **Casos Críticos**: Test Case 8 (1000×1000)
- **Seletividade**: 50% TLE rate em slow solutions

## Descobertas Científicas

### 1. Disparidade Algorítmica Confirmada
Python recursivo apresenta overhead significativo em casos computacionalmente intensivos, resultando em TLE onde C++ executa normalmente.

### 2. Casos Críticos Identificados
Testes #6-#9 (grids 1000×1000) representam cenários onde recursão profunda em Python atinge limitações de performance.

### 3. Sistema Adaptativo Validado
Fator de ajuste 1.12x adequado para compensar diferenças de linguagem em casos médios.

### 4. Seletividade Preservada
Slow solutions detectadas adequadamente pelo sistema, mantendo integridade acadêmica.

## Implicações para TCC

### Contribuição Metodológica
- Protocolo rigoroso para validação de sistemas de julgamento
- Integração de validação externa com benchmarks locais
- Framework replicável para outros problemas

### Contribuição Técnica
- Quantificação empírica da injustiça algorítmica
- Identificação de casos críticos específicos
- Validação de sistema adaptativo

### Contribuição Acadêmica
- Evidência científica de disparidade entre linguagens
- Metodologia para preservação de seletividade
- Base para futuras pesquisas em justiça algorítmica

## Limitações Identificadas

1. **Escopo**: Limitado a algoritmos recursivos de DP
2. **Plataforma**: Resultados específicos para ambiente CSES
3. **Linguagens**: Análise restrita a C++ vs Python

## Recomendações

### Para Implementação
- Aplicar fator 1.12x em problemas similares
- Monitorar casos críticos (grids >500×500)
- Manter validação de slow solutions

### Para Pesquisa Futura
- Expandir para outros paradigmas algorítmicos
- Incluir linguagens adicionais (Java, JavaScript)
- Investigar técnicas de otimização específicas

## Conclusão

O experimento demonstra metodologia científica robusta para investigação de disparidade algorítmica, fornecendo evidência empírica e solução técnica validada. Os resultados confirmam a viabilidade de sistemas adaptativos para mitigação de injustiça entre linguagens de programação.

**Status Final**: Experimento bem-sucedido com descobertas metodologicamente válidas para incorporação no TCC.
