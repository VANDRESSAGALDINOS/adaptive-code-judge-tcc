# Template de Experimento - [CATEGORIA]_[PROBLEMA]

## 📋 METADADOS OBRIGATÓRIOS
```json
{
  "categoria": "[graphs|dp_iterativa|dp_recursiva|recursao_profunda|backtracking]",
  "problema_id": "[cses_1234|atcoder_abc123]",
  "problema_nome": "[Nome oficial]",
  "complexidade_algoritmica": "[O(n³)|O(2ⁿ)|etc]",
  "data_experimento": "YYYY-MM-DD",
  "duracao_total": "XX minutos",
  "plataforma_origem": "[CSES|AtCoder|etc]"
}
```

## 🎯 DADOS OBRIGATÓRIOS PARA GRÁFICOS FINAIS

### 1. FATOR DE AJUSTE (Para Gráfico Executivo)
- **Fator calibrado**: X.XX
- **IQR do fator**: ±X.XX
- **Confiabilidade**: [Alta|Média|Baixa]
- **Sample size**: N repetições

### 2. MAPA DE INJUSTIÇA (Para Heatmap)
```json
{
  "input_sizes": {
    "pequeno": {"N": 100, "python_tle_rate": 0.0},
    "medio": {"N": 1000, "python_tle_rate": 0.3},
    "grande": {"N": 10000, "python_tle_rate": 0.8}
  }
}
```

### 3. VALIDAÇÃO EXTERNA (Para Scatter CSES)
- **Taxa TLE Python (CSES real)**: XX%
- **Taxa TLE Python (Nosso benchmark)**: YY%
- **Diferença absoluta**: |XX-YY|%
- **Status validação**: [✅ Válido|⚠️ Discrepante|❌ Inválido]

### 4. CORREÇÃO RESPONSÁVEL (Para Before/After)
```json
{
  "tradicional": {"cpp": XX%, "python": YY%},
  "adaptativo": {"cpp": XX%, "python": ZZ%},
  "casos_python_ainda_falha": ["caso_X: razão", "caso_Y: razão"]
}
```

### 5. SELETIVIDADE PRESERVADA
- **Slow solutions C++ (tradicional)**: [TLE|PASS]
- **Slow solutions Python (tradicional)**: [TLE|PASS]  
- **Slow solutions C++ (adaptativo)**: [TLE|PASS]
- **Slow solutions Python (adaptativo)**: [TLE|PASS]
- **Status rigor**: [✅ Preservado|❌ Comprometido]

## 🔍 INSIGHTS ESPECÍFICOS

### Descobertas Inesperadas
- [ ] **Anomalia positiva**: [Descrever]
- [ ] **Anomalia negativa**: [Descrever]
- [ ] **Padrão divergente**: [Descrever]

### Características da Categoria
- [ ] **Overhead dominante**: [CPU|Memória|I/O]
- [ ] **Bottleneck identificado**: [Loops|Recursão|Estruturas]
- [ ] **Comportamento único**: [Descrever]

## 📊 DADOS ESTRUTURADOS (Para Scripts Python)

### export_data.json
```json
{
  "experiment": {
    "categoria": "",
    "problema": "",
    "data": ""
  },
  "fatores": {
    "ajuste_mediano": 0.0,
    "ajuste_iqr": 0.0,
    "confiabilidade": ""
  },
  "injustica": {
    "input_pequeno": {"size": 0, "tle_rate": 0.0},
    "input_medio": {"size": 0, "tle_rate": 0.0},
    "input_grande": {"size": 0, "tle_rate": 0.0}
  },
  "validacao": {
    "cses_real": 0.0,
    "nosso_benchmark": 0.0,
    "correlacao": 0.0
  },
  "correcao": {
    "tradicional_python": 0.0,
    "adaptativo_python": 0.0,
    "melhoria": 0.0
  },
  "seletividade": {
    "slow_cpp_tradicional": "TLE",
    "slow_python_tradicional": "TLE",
    "slow_cpp_adaptativo": "TLE", 
    "slow_python_adaptativo": "TLE",
    "preservada": true
  }
}
```

## 🚨 CHECKLIST OBRIGATÓRIO

### Antes de Finalizar o Experimento:
- [ ] Fator de ajuste calculado e confiável
- [ ] Pelo menos 3 tamanhos de input testados
- [ ] Validação vs plataforma real executada
- [ ] Slow solutions testadas em ambos sistemas
- [ ] Dados exportados para JSON estruturado
- [ ] Insights específicos documentados
- [ ] Anomalias/limitações identificadas

### Para Inclusão nos Gráficos Finais:
- [ ] **Caso emblemático?** [Sim/Não + Justificativa]
- [ ] **Representa bem a categoria?** [Sim/Não]
- [ ] **Dados suficientes para generalização?** [Sim/Não]

## 🎯 CRITÉRIOS DE QUALIDADE

### Experimento Válido Se:
- ✅ Fator de ajuste < 50x (realista)
- ✅ Correlação com CSES real > 0.7
- ✅ Seletividade preservada (slow solutions TLE)
- ✅ Sample size ≥ 10 repetições por caso
- ✅ IQR < 30% (estabilidade)

### Prioridade para Gráficos Finais:
- 🥇 **Alta**: Caso representa bem a categoria + resultado limpo
- 🥈 **Média**: Caso típico da categoria
- 🥉 **Baixa**: Caso atípico, mas com insights valiosos

---
**Data de criação**: [Data]
**Status**: [Planejado|Em execução|Concluído|Analisado]
**Prioridade gráficos**: [Alta|Média|Baixa]

