# Validação CSES - Dynamic Programming Iterativo (CSES 1635)

## Dados das Submissões

### Submissão C++ - Implementação Iterativa
**Data**: 2025-08-31 21:59:50 +0300  
**Status**: ACCEPTED  
**Linguagem**: C++ (C++11)  
**Link**: [Código compartilhado no CSES]

#### Resultados por Test Case
| Test | Verdict | Time | Análise |
|------|---------|------|---------|
| #1 | ACCEPTED | 0.00s | Baseline |
| #2 | ACCEPTED | 0.01s | Input grande simples |
| #3 | ACCEPTED | 0.00s | Input médio |
| #4 | ACCEPTED | 0.57s | Caso crítico A |
| #5 | ACCEPTED | 0.30s | Caso moderado |
| #6 | ACCEPTED | 0.00s | Edge case |
| #7 | ACCEPTED | 0.00s | Input pequeno |
| #8 | ACCEPTED | 0.57s | Caso crítico B |
| #9 | ACCEPTED | 0.00s | Input básico |
| #10 | ACCEPTED | 0.00s | Input básico |
| #11 | ACCEPTED | 0.57s | Caso crítico C |
| #12 | ACCEPTED | 0.10s | Input moderado |
| #13 | ACCEPTED | 0.01s | Input pequeno |

**Observação**: Três casos específicos (4, 8, 11) apresentam tempo de execução idêntico (0.57s), sugerindo padrão algorítmico consistente para inputs de escala x=1,000,000.

### Submissão Python - Implementação Iterativa
**Data**: 2025-08-31 22:00:46 +0300  
**Status**: TIME LIMIT EXCEEDED  
**Linguagem**: Python3 (CPython3)  
**Link**: [Código compartilhado no CSES]

#### Resultados por Test Case
| Test | Verdict | Time | Gap vs C++ |
|------|---------|------|------------|
| #1 | ACCEPTED | 0.02s | +∞% |
| #2 | ACCEPTED | 0.30s | +2900% |
| #3 | ACCEPTED | 0.02s | +∞% |
| #4 | TLE | >1.0s | >+75% |
| #5 | TLE | >1.0s | >+233% |
| #6 | ACCEPTED | 0.02s | +∞% |
| #7 | ACCEPTED | 0.03s | +∞% |
| #8 | TLE | >1.0s | >+75% |
| #9 | ACCEPTED | 0.02s | +∞% |
| #10 | ACCEPTED | 0.02s | +∞% |
| #11 | TLE | >1.0s | >+75% |
| #12 | TLE | >1.0s | >+900% |
| #13 | ACCEPTED | 0.10s | +900% |

**Taxa de Sucesso**: 8/13 (61.5%)  
**Cases TLE**: 5/13 (38.5%)

## Análise Comparativa com DP Recursivo

### Performance C++ por Abordagem
| Test Case | Recursivo | Iterativo | Diferença |
|-----------|-----------|-----------|-----------|
| #4 | 0.47s | 0.57s | +21% |
| #8 | 0.47s | 0.57s | +21% |
| #11 | 0.47s | 0.57s | +21% |

**Observação**: DP iterativo apresenta overhead de aproximadamente 21% comparado ao recursivo em C++, contrariando expectativa de que iterativo seria mais eficiente.

### Performance Python por Abordagem
| Abordagem | Taxa Sucesso | Cases TLE | Casos Críticos |
|-----------|--------------|-----------|-----------------|
| Recursivo | 8/13 (61.5%) | #2,4,5,8,11 | RecursionError + TLE |
| Iterativo | 8/13 (61.5%) | #4,5,8,11,12 | TLE puro |

**Resultado**: Taxa de sucesso idêntica entre abordagens, indicando que limitação recursiva não é fator determinante da injustiça observada.

## Descobertas Analíticas

### Refutação de Hipótese Inicial
**Hipótese**: DP iterativo eliminaria injustiça temporal por remover limitações de recursão.  
**Resultado**: Hipótese refutada. Injustiça temporal persiste com mesma magnitude.

### Identificação de Fatores Causais
A persistência da injustiça em DP iterativo indica que os fatores determinantes são:

1. **Overhead interpretativo**: Diferença fundamental entre linguagem compilada vs interpretada
2. **Intensidade de operações**: Algoritmo O(n×x) com acesso intensivo a arrays
3. **Complexidade de input**: Cases críticos (x=1,000,000, n=100) excedem capacidade temporal Python

### Caracterização de Cases Críticos
**Pattern identificado**: Cases com x=1,000,000 e n=100 sistematicamente causam TLE em Python, independente da abordagem (recursiva ou iterativa).

## Implicações Científicas

### Para a Hipótese de Pesquisa
A manutenção da injustiça em DP iterativo fortalece a evidência de que a causa primária não são limitações arquiteturais específicas (recursão), mas diferenças fundamentais de performance entre linguagens compiladas e interpretadas em algoritmos computacionalmente intensivos.

### Para Juízes Adaptativos
Sistemas adaptativos devem considerar não apenas a abordagem algorítmica (recursivo vs iterativo), mas a complexidade computacional absoluta do problema. DP com x>100,000 pode requerer ajustes específicos independente da implementação.

### Limitações do Estudo
1. **Amostra específica**: Resultados limitados ao CSES 1635
2. **Implementação única**: Uma implementação por linguagem/abordagem
3. **Plataforma específica**: CSES pode ter características particulares

## Metodologia de Validação

### Equivalência Algorítmica
Ambas implementações seguem especificação idêntica:
- Complexidade: O(n×x)
- Espaço: O(x)
- Base cases: dp[0] = 1
- Recorrência: dp[i] = Σ dp[i-coin] para coin ≤ i

### Controles Experimentais
- **Mesmos test cases**: 13 casos oficiais CSES
- **Mesma plataforma**: CSES Online Judge
- **Implementações equivalentes**: Validadas por correção de output
- **Tempo de submissão**: Intervalo < 1 minuto (condições similares)

## Validação de Soluções Lentas

### Submissão C++ Lenta - DP Iterativo com Overhead
**Data**: 2025-08-31 22:06:18 +0300  
**Status**: TIME LIMIT EXCEEDED  
**Linguagem**: C++ (C++11)  
**Overhead**: EXTRA_WORK = 200

#### Resultados Detalhados - C++ Slow
| Test | Verdict | Time | Comparação vs Normal |
|------|---------|------|---------------------|
| #1 | ACCEPTED | 0.00s | Igual (0.00s) |
| #2 | ACCEPTED | 0.42s | Degradação (+4100%) |
| #3 | ACCEPTED | 0.01s | Degradação (+∞%) |
| #4 | TLE | >1.0s | Novo TLE vs 0.57s |
| #5 | TLE | >1.0s | Novo TLE vs 0.30s |
| #6 | ACCEPTED | 0.00s | Igual (0.00s) |
| #7 | ACCEPTED | 0.03s | Degradação (+∞%) |
| #8 | TLE | >1.0s | Novo TLE vs 0.57s |
| #9 | ACCEPTED | 0.00s | Igual (0.00s) |
| #10 | ACCEPTED | 0.00s | Igual (0.00s) |
| #11 | TLE | >1.0s | Novo TLE vs 0.57s |
| #12 | ACCEPTED | 0.07s | Degradação (-30%) |
| #13 | ACCEPTED | 0.07s | Degradação (+600%) |

**Taxa de Sucesso**: 9/13 (69.2%) → 4/13 TLE novos

### Submissão Python Lenta - DP Iterativo com Overhead  
**Data**: 2025-08-31 22:07:12 +0300  
**Status**: TIME LIMIT EXCEEDED  
**Linguagem**: Python3 (CPython3)  
**Overhead**: EXTRA_WORK = 200

#### Resultados Detalhados - Python Slow
| Test | Verdict | Time | Comparação vs Normal |
|------|---------|------|---------------------|
| #1 | ACCEPTED | 0.02s | Igual (0.02s) |
| #2 | TLE | >1.0s | Novo TLE vs 0.30s |
| #3 | ACCEPTED | 0.08s | Degradação (+300%) |
| #4 | TLE | >1.0s | Mantém TLE |
| #5 | TLE | >1.0s | Mantém TLE |
| #6 | ACCEPTED | 0.02s | Igual (0.02s) |
| #7 | ACCEPTED | 0.99s | Degradação (+3200%) |
| #8 | TLE | >1.0s | Mantém TLE |
| #9 | ACCEPTED | 0.02s | Igual (0.02s) |
| #10 | ACCEPTED | 0.02s | Igual (0.02s) |
| #11 | TLE | >1.0s | Mantém TLE |
| #12 | TLE | >1.0s | Novo TLE vs normal |
| #13 | TLE | >1.0s | Novo TLE vs 0.10s |

**Taxa de Sucesso**: 8/13 (61.5%) → 5/13 (38.5%) - 3 TLE adicionais

### Análise de Efetividade do Overhead

#### Validação C++ Slow
- **Cases originalmente ACCEPTED**: 4 novos TLE (4,5,8,11)
- **Degradação detectável**: Cases 2,3,7,12,13 mostram overhead mensurável
- **Efetividade**: Overhead detectado em cases críticos

#### Validação Python Slow
- **Cases originalmente ACCEPTED**: 3 novos TLE (2,12,13)  
- **Cases já TLE**: Mantiveram TLE (4,5,8,11)
- **Case crítico #7**: 0.03s → 0.99s (margem crítica)
- **Efetividade**: Overhead amplificou degradação existente

## Conclusões Preliminares

1. **Persistência de injustiça**: DP iterativo não resolve injustiça temporal observada
2. **Fator causal refinado**: Overhead interpretativo, não limitações recursivas
3. **Consistência de padrão**: Cases críticos mantêm mesmo perfil de falha
4. **Validação metodológica**: Overhead intencional detectado adequadamente em ambas linguagens
5. **Amplificação diferencial**: Python mostra maior sensibilidade ao overhead adicional
