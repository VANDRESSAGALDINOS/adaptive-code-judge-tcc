# Resultados Problem01_Recursivo: CSES 1635 - Coin Combinations I (DP Recursivo)

## 📋 Índice de Documentação

### 📊 Documentos Principais
- **[DESCRICAO_EXPERIMENTO.md](./DESCRICAO_EXPERIMENTO.md)**: Descrição completa do experimento, metodologia e implementação recursiva
- **[INSIGHTS_CIENTIFICOS.md](./INSIGHTS_CIENTIFICOS.md)**: Descobertas sobre injustiças Tipo A/B e limitações arquiteturais
- **[ANALISE_COMPARATIVA.md](./ANALISE_COMPARATIVA.md)**: Comparação detalhada entre C++ e Python recursivo

### 📈 Dados Experimentais
- **[../formal_proof.md](../formal_proof.md)**: Prova de equivalência algorítmica matemática
- **[BINARY_VERDICT_REPORT.md](../BINARY_VERDICT_REPORT.md)**: Análise binária ACCEPTED vs REJECTED
- **Submissões CSES**: Links documentados para reprodutibilidade

## 🎯 Resultados Principais

### ⚠️ **LIMITAÇÕES ARQUITETURAIS DESCOBERTAS**
- **C++ Recursivo**: ✅ ACCEPTED (marginal: 0.47s de 1.0s)
- **Python Recursivo**: ❌ RUNTIME ERROR + TLE
- **Descoberta**: Recursão profunda O(x≥10^6) inviável em Python

### 📊 **Métricas de Injustiça**
```
Injustiça Tipo A (Temporal):
├── Tests críticos: #4, #5, #8, #11
├── Fator mínimo: >2.13x (0.47s → >1.0s)
└── Python TLE onde C++ passa

Injustiça Tipo B (Arquitetural):
├── Test patológico: #2 (x=1,000,000, moeda=1)
├── Python: RecursionError
└── C++ viável: Não testado neste caso específico
```

### 🔬 **Contribuições Científicas**

#### Framework de Categorização
**Injustiça Tipo A**: Diferenças temporais em algoritmos executáveis
**Injustiça Tipo B**: Impossibilidade arquitetural de execução

#### Descoberta Metodológica
Sistemas adaptativos devem considerar **viabilidade algorítmica**, não apenas fatores de tempo.

## 📌 **Status Experimental**
- **Equivalência Algorítmica**: ✅ Comprovada matematicamente
- **Validação CSES**: ✅ Submetido e documentado
- **Slow Solutions**: ✅ Validadas com degradação controlada
- **Reprodutibilidade**: ✅ Códigos e links documentados

## ⚖️ **Limitações Reconhecidas**
- **Escopo**: 1 problema DP recursivo
- **Controle**: Falta versão iterativa equivalente
- **Generalização**: Limitada a esta categoria algorítmica

## 🎯 **Próximos Passos**
1. Implementar versão iterativa do mesmo problema
2. Comparar recursivo vs iterativo
3. Validar em múltiplos problemas DP
4. Análise estatística com amostras maiores

**Status**: Experimento recursivo **metodologicamente completo** ✅
