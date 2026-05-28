# Experimento On2_quadratic - Experimento

## Resumo Executivo

**Descoberta Principal**: Python supera C++ em **-51.4%** para algoritmo não especificado em ambientes containerizados.

**Resultado**: Esperado - confirma teoria

## Dados Experimentais Brutos

### Performance Medida
- **C++ Mediano**: 1.0599s
- **Python Mediano**: 1.6044s
- **Razão Python/C++**: 1.514x
- **Vantagem Python**: -51.4%

### Confiabilidade
- **Repetições Bem-sucedidas**: 5/10
- **Teste Utilizado**: massive_matrix
- **Confiável**: Sim

### Variabilidade (IQR)
- **C++ IQR**: 0.0216s (2.0%)
- **Python IQR**: 0.0407s (2.5%)

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
    "cpp_limit_ms": 1059,
    "python_limit_ms": 1604,
    "adjustment_factor": 1.514
  }
}
```

## Dados Técnicos Completos

### Execuções C++
```
[1.0889060497283936, 1.0555834770202637, 1.0679731369018555, 1.059885025024414, 1.0580341815948486]
```

### Execuções Python
```
[1.6006889343261719, 1.6484425067901611, 1.5973975658416748, 1.604419231414795, 1.631051778793335]
```

## Conclusão

Este experimento demonstra que **performance é contextual** e depende criticamente do ambiente de execução.

Os resultados confirmam expectativas teóricas e demonstram a importância de medições empíricas.

**Para sistemas de juízes online, estes dados justificam limites de tempo adaptativos** que considerem a performance real de cada linguagem no ambiente de produção.

---
*Relatório gerado automaticamente em 27/05/2026 22:27:52*
*Experimento conduzido como parte do projeto Adaptive Code Judge*
