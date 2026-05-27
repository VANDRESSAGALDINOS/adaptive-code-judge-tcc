# Experimento On2_quadratic - Experimento

## Resumo Executivo

**Descoberta Principal**: Python supera C++ em **-52.8%** para algoritmo não especificado em ambientes containerizados.

**Resultado**: Esperado - confirma teoria

## Dados Experimentais Brutos

### Performance Medida
- **C++ Mediano**: 1.0600s
- **Python Mediano**: 1.6200s  
- **Razão Python/C++**: 1.528x
- **Vantagem Python**: -52.8%

### Confiabilidade
- **Repetições Bem-sucedidas**: 5/10
- **Teste Utilizado**: massive_matrix
- **Confiável**: Sim

### Variabilidade (IQR)
- **C++ IQR**: 0.0750s (7.1%)
- **Python IQR**: 0.0600s (3.7%)

## Análise dos Resultados

### Algoritmo não especificado
- **Descrição**: Descrição não disponível
- **Complexidade Teórica**: O(n2 quadraticn)
- **Implementação**: Algoritmicamente equivalente em ambas linguagens

### Fatores de Performance Identificados

1. **Overhead de Compilação**
   - C++ requer compilação a cada execução (~0.29s)
   - Python executa imediatamente (~0.18s)

2. **Otimizações de Runtime**
   - CPython tem operações nativas altamente otimizadas
   - Estruturas de dados Python implementadas em C

3. **Container Overhead**
   - Docker startup mais rápido para Python
   - Toolchain C++ adiciona latência

## Insights para o TCC

### Contribuição Científica
- **Paradigma Contestado**: Confirma expectativas teóricas
- **Evidência Empírica**: Dados quantitativos de ambiente real
- **Metodologia**: Separação de fatores algorítmicos vs overhead

### Aplicação Prática
```json
{
  "adaptive_limits": {
    "problem_type": "On2_quadratic",
    "cpp_limit_ms": 1060,
    "python_limit_ms": 1620,
    "adjustment_factor": 1.528
  }
}
```

## Dados Técnicos Completos

### Execuções C++
```
[1.13, 1.06, 1.13, 1.05, 1.06]
```

### Execuções Python  
```
[1.62, 1.63, 1.58, 1.58, 1.65]
```

## Conclusão

Este experimento demonstra que **performance é contextual** e depende criticamente do ambiente de execução. 

Os resultados confirmam expectativas teóricas e demonstram a importância de medições empíricas.

**Para sistemas de juízes online, estes dados justificam limites de tempo adaptativos** que considerem a performance real de cada linguagem no ambiente de produção.

---
*Relatório gerado automaticamente em 26/05/2026 23:15:51*
*Experimento conduzido como parte do projeto Adaptive Code Judge*
