# Descrição do Experimento: DP Recursivo CSES 1635

## Objetivo do Experimento

Demonstrar empiricamente injustiças de linguagem em algoritmos de **Programação Dinâmica Recursiva** através da comparação de implementações algoritmicamente equivalentes em C++ e Python.

## Metodologia Experimental

### Problema Selecionado
**CSES 1635 - Coin Combinations I**
- **Tipo**: Programação Dinâmica Top-down com Memoização
- **Complexidade**: O(n × x) tempo, O(x) espaço + stack
- **Características**: Recursão profunda até O(x) onde x ≤ 10^6

### Implementações Testadas

#### C++ Recursivo
- **Algoritmo**: Top-down DP com memoização nativa
- **Stack**: Sistema operacional (profundidade alta)
- **Submissão**: 2025-08-31 20:55:58 +0300
- **Link**: https://cses.fi/paste/afbf3069975b5278db48fc/

#### Python Recursivo  
- **Algoritmo**: Equivalente matemático ao C++
- **Stack**: Virtual com `sys.setrecursionlimit(1100000)`
- **Submissão**: 2025-08-31 21:07:29 +0300
- **Limitação**: RecursionError em casos extremos

### Validação de Equivalência

#### Prova Matemática
- **Recorrência**: `f(remaining) = Σ f(remaining - coin_i)`
- **Casos base**: `f(0) = 1`, `f(<0) = 0`
- **Memoização**: Idêntica em ambas linguagens
- **Status**: ✅ Equivalência comprovada

#### Validação com Soluções Lentas
- **C++ Slow**: https://cses.fi/paste/d69a2b02f3b24a33db498b/
- **Python Slow**: https://cses.fi/paste/698dd97b5969f208db49b5/
- **Mecanismo**: EXTRA_WORK=150 para degradação controlada
- **Resultado**: ✅ Degradação confirmada (19x no Test #3)

## Resultados Experimentais

### Performance C++ vs Python

| Categoria | C++ | Python | Injustiça |
|-----------|-----|---------|-----------|
| **Casos pequenos** | 0.01s ACCEPTED | 0.02s ACCEPTED | **Fator 2x** |
| **Casos críticos** | 0.47s ACCEPTED | TLE >1.0s | **Tipo A: >2.13x** |
| **Caso extremo** | N/A | RecursionError | **Tipo B: Arquitetural** |

### Descobertas Críticas

#### Injustiça Tipo A (Temporal)
- **Tests afetados**: #4, #5, #8, #11
- **Padrão**: C++ marginal (0.47s), Python TLE
- **Fator**: >2.13x diferença mínima

#### Injustiça Tipo B (Arquitetural)
- **Test específico**: #2 (x=1,000,000, moeda=1)
- **Python**: RecursionError irrecuperável
- **Causa**: Stack overflow em recursão O(x)

## Protocolo de Validação

### Critérios de Equivalência
1. ✅ **Recorrência matemática idêntica**
2. ✅ **Casos base equivalentes**
3. ✅ **Estratégia de memoização igual**
4. ✅ **Processamento de entrada/saída correto**

### Critérios de Injustiça
1. ✅ **C++ executa, Python falha** (Tipo B)
2. ✅ **C++ marginal, Python TLE** (Tipo A)
3. ✅ **Diferença >2x em casos críticos**

### Validação de Seletividade
1. ✅ **Soluções lentas TLE** em ambas linguagens
2. ✅ **Degradação controlada** observada
3. ✅ **Preservação da ordenação** de dificuldade

## Limitações Metodológicas

### Escopo Experimental
- **Amostra**: 1 problema de DP recursivo
- **Plataforma**: CSES Online Judge apenas
- **Linguagens**: C++ e Python exclusivamente

### Controles Ausentes
- **Versão iterativa**: Não implementada para comparação
- **Outros problemas**: Não testados para generalização
- **Outras linguagens**: Não avaliadas

### Validade Externa
- **Generalização**: Limitada a DP recursivo
- **Reprodutibilidade**: Dependente da plataforma CSES
- **Estabilidade**: Sujeita a variações de sistema

## Contribuições Metodológicas

### Framework de Categorização
**Inovação**: Distinção entre injustiças temporais vs arquiteturais
- **Tipo A**: Diferenças de performance recuperáveis
- **Tipo B**: Limitações fundamentais irrecuperáveis

### Implicações para Sistemas Adaptativos
**Descoberta**: Ajuste de time limits é insuficiente para injustiças Tipo B
**Recomendação**: Sistemas devem oferecer alternativas algorítmicas

## Status e Próximos Passos

### Experimento Atual
- **Status**: ✅ **Metodologicamente completo**
- **Reprodutibilidade**: ✅ Códigos e submissões documentadas
- **Validade interna**: ✅ Equivalência comprovada

### Expansão Necessária
1. **Implementação iterativa** do mesmo problema
2. **Comparação recursivo vs iterativo**
3. **Múltiplos problemas** de DP
4. **Análise estatística** robusta

**Conclusão**: Experimento estabelece base sólida para investigação de injustiças arquiteturais em sistemas de julgamento online.
