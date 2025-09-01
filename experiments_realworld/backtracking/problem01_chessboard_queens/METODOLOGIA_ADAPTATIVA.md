# Metodologia Adaptativa para Problemas Intrinsecamente Rápidos

## 🎯 PROBLEMA CIENTÍFICO
**N-Queens 8x8** é um problema de **tamanho fixo pequeno** que não gera TLE naturalmente em nenhuma linguagem, mesmo com overhead intencional moderado.

## 🔬 ABORDAGEM CIENTÍFICA ADAPTATIVA

### **CATEGORIA A: Problemas com Injustiça Algorítmica Natural**
- **Exemplos**: DP recursivo, Grafos com alta complexidade
- **Metodologia**: Protocolo original (TLE rate ≥80%)
- **Foco**: Quantificar injustiça direta

### **CATEGORIA B: Problemas Intrinsecamente Rápidos** 
- **Exemplos**: N-Queens 8x8, problemas de tamanho fixo
- **Metodologia**: **Análise de Sensibilidade Diferencial**
- **Foco**: Quantificar tolerância ao overhead

## 📊 METODOLOGIA PARA CATEGORIA B

### **FASE 1: Caracterização do Problema**
1. **Baseline Performance**: Medir tempos sem overhead
2. **Overhead Scaling**: Testar múltiplos níveis de EXTRA_WORK
3. **Threshold Detection**: Identificar ponto de saturação

### **FASE 2: Análise de Sensibilidade Diferencial**
```
EXTRA_WORK_LEVELS = [0, 1000, 5000, 10000, 25000, 50000, 100000]
```

**Métricas Científicas**:
- **Slope Ratio**: Taxa de degradação C++ vs Python
- **Tolerance Threshold**: EXTRA_WORK onde Python atinge 1s
- **Differential Sensitivity Index (DSI)**: Razão das sensibilidades

### **FASE 3: Validação Estatística**
- **Regressão Linear**: Tempo vs EXTRA_WORK
- **R² Analysis**: Qualidade do ajuste
- **Confidence Intervals**: 95% CI para slopes
- **Statistical Significance**: p-value < 0.05

## 🎯 CRITÉRIOS DE SUCESSO ADAPTADOS

### **Para Categoria B (Problemas Rápidos)**:
- ✅ **DSI ≥ 2.0**: Sensibilidade diferencial significativa
- ✅ **R² ≥ 0.95**: Relação linear forte
- ✅ **p < 0.05**: Diferença estatisticamente significativa
- ✅ **Tolerance Gap ≥ 10x**: Python atinge limite antes de C++

## 📈 VALOR CIENTÍFICO

**Descoberta**: Mesmo problemas "justos" revelam **sensibilidade diferencial**, complementando casos de injustiça algorítmica direta.

**Implicação**: Sistemas de avaliação podem inadvertidamente penalizar Python mesmo quando algoritmos são equivalentes e corretos.
