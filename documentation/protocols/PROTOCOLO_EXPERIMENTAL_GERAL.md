# PROTOCOLO EXPERIMENTAL GERAL

## Visão Geral

Este protocolo padroniza a execução de experimentos para detecção de injustiças linguísticas em juízes online, baseado na metodologia de Análise Binária de Veredicto.

## Pré-requisitos

### Dados Necessários
1. **Problema específico** da plataforma (ex: CSES 1197)
2. **Soluções algoritmicamente equivalentes** em C++ e Python
3. **Test cases oficiais** da plataforma
4. **Dados de submissões reais** (para validação externa)

### Ambiente Técnico
1. **Docker** configurado com imagens apropriadas
2. **Python 3.11+** para scripts de análise
3. **Acesso à plataforma** para coleta de dados externos

## Fase 1: Preparação

### 1.1 Análise do Problema
- [ ] Identificar **complexidade algorítmica**
- [ ] Classificar **categoria** (grafos, DP, etc.)
- [ ] Determinar **tamanho típico** dos casos de teste
- [ ] Verificar **tipos de saída** (única vs múltiplas válidas)

### 1.2 Coleta de Dados Externos
- [ ] Submeter **solução C++** na plataforma real
- [ ] Submeter **solução Python** na plataforma real
- [ ] Documentar **casos que dão TLE** em Python
- [ ] Identificar **casos críticos** vs **casos controle**

### 1.3 Preparação de Soluções
- [ ] **Prova formal** de equivalência algorítmica
- [ ] **Soluções otimizadas** para ambas linguagens
- [ ] **Slow solutions** para validação de seletividade
- [ ] **Validação de correção** em casos pequenos

## Fase 2: Configuração

### 2.1 Parâmetros Experimentais
```json
{
  "time_limit": "igual_plataforma_real",
  "repetitions": "minimo_10_por_caso",
  "docker_images": {
    "cpp": "gcc:latest",
    "python": "python:3.11-slim"
  },
  "casos_criticos": "baseados_dados_externos",
  "casos_controle": "amostra_representativa"
}
```

### 2.2 Estrutura de Diretórios
```
problemXX/
├── solutions/
│   ├── solution.cpp
│   └── solution.py
├── slow_validation/
│   ├── slow_solution.cpp
│   └── slow_solution.py
├── tests_cses/
│   ├── 1.in, 1.out
│   └── ...
├── results/
└── scripts/
    ├── run_benchmark.py
    ├── analyze_binary_verdict.py
    └── validate_slow_solutions.py
```

## Fase 3: Execução

### 3.1 Calibração
```bash
python3 run_benchmark.py \
  --phase=calibration \
  --case=CASO_REPRESENTATIVO \
  --repetitions=30 \
  --time-limit=LIMITE_REAL
```

**Objetivo**: Determinar fator de ajuste baseado em caso representativo

### 3.2 Validação Binária
```bash
python3 run_benchmark.py \
  --phase=validation \
  --cases=CASOS_CRITICOS \
  --repetitions=10 \
  --time-limit=LIMITE_REAL \
  --adjustment-factor=FATOR_CALIBRADO
```

**Objetivo**: Testar sistema tradicional vs adaptativo

### 3.3 Análise Binária
```bash
python3 analyze_binary_verdict.py
```

**Objetivo**: Aplicar metodologia binária aos resultados

### 3.4 Validação de Seletividade
```bash
python3 validate_slow_solutions.py \
  --cases=AMOSTRA_CASOS \
  --adjustment-factor=FATOR_CALIBRADO
```

**Objetivo**: Confirmar que slow solutions são rejeitadas

## Fase 4: Análise

### 4.1 Critérios de Validação
- [ ] **Injustiça detectada**: `tradicional_cpp == ACCEPTED && tradicional_python == REJECTED`
- [ ] **Injustiça corrigida**: `adaptativo_cpp == ACCEPTED && adaptativo_python == ACCEPTED`
- [ ] **Seletividade preservada**: `slow_solutions == REJECTED` em ambos sistemas
- [ ] **Fator realista**: `1.5x <= fator_ajuste <= 50x`

### 4.2 Métricas de Qualidade
```python
metricas = {
    "confiabilidade_cpp": "IQR_relativo < 0.15",
    "confiabilidade_python": "IQR_relativo < 0.15", 
    "casos_resgatados": "count(python_rescued)",
    "correlacao_externa": "comparacao_com_dados_reais"
}
```

### 4.3 Documentação Obrigatória
- [ ] **Relatório binário**: `BINARY_VERDICT_REPORT.md`
- [ ] **Metadados**: `metadata_graficos.json`
- [ ] **Descobertas específicas**: `DESCOBERTA_ESPECIFICA_PROBLEMXX.md`
- [ ] **Dados brutos**: `results/*.json`

## Fase 5: Validação Externa

### 5.1 Comparação com Dados Reais
- [ ] **Correlação** entre resultados locais e CSES
- [ ] **Explicação** de discrepâncias identificadas
- [ ] **Validação** de casos críticos vs controle

### 5.2 Checklist de Qualidade
```python
# Executar automaticamente
python3 /path/to/AUTO_CHECKLIST.py
```

## Critérios de Sucesso

### Experimento Válido
- ✅ **Injustiça detectada** no sistema tradicional
- ✅ **Injustiça corrigida** no sistema adaptativo  
- ✅ **Seletividade preservada** em ambos sistemas
- ✅ **Correlação externa** com dados reais
- ✅ **Documentação completa** gerada

### Experimento Inconclusivo
- ❌ Sem injustiça detectada (investigar parâmetros)
- ❌ Seletividade comprometida (ajustar slow solutions)
- ❌ Fator irrealista (> 50x ou < 1.5x)
- ❌ Baixa confiabilidade (IQR > 0.15)

## Tratamento de Problemas Comuns

### Problema: Sem Injustiça Detectada
**Possíveis causas**:
- Limite de tempo muito permissivo
- Casos não críticos suficientes
- Ambiente muito diferente da plataforma real

**Soluções**:
- Reduzir limite de tempo
- Focar em casos que dão TLE na plataforma real
- Ajustar configuração Docker

### Problema: Fator de Ajuste Irrealista
**Possíveis causas**:
- Diferenças de ambiente muito grandes
- Algoritmo não equivalente
- Overhead Docker excessivo

**Soluções**:
- Verificar equivalência algorítmica
- Otimizar configuração Docker
- Considerar overhead como insight científico

### Problema: Seletividade Comprometida
**Possíveis causas**:
- Slow solutions insuficientemente lentas
- Fator de ajuste muito permissivo

**Soluções**:
- Aumentar EXTRA_PASSES nas slow solutions
- Validar que slow solutions dão TLE consistentemente

## Automação

### Scripts Reutilizáveis
1. **`run_benchmark.py`** - Execução de benchmarks
2. **`analyze_binary_verdict.py`** - Análise binária
3. **`validate_slow_solutions.py`** - Validação de seletividade
4. **`AUTO_CHECKLIST.py`** - Checklist automático

### Templates
1. **`TEMPLATE_EXPERIMENTO.md`** - Estrutura padrão
2. **`experiment_metadata.json`** - Metadados padrão
3. **`problem_description.md`** - Descrição acadêmica

## Evolução do Protocolo

### Versão Atual: 1.0
- ✅ Metodologia binária estabelecida
- ✅ Validação em Problem02
- ✅ Scripts automatizados

### Próximas Versões
- 🔄 **v1.1**: Suporte a múltiplas plataformas
- 🔄 **v1.2**: Análise multi-dimensional (além de TLE)
- 🔄 **v1.3**: Pipeline completamente automatizado

---
**Protocolo**: Experimental Geral v1.0  
**Baseado em**: Metodologia de Análise Binária de Veredicto  
**Validado em**: Problem02 - CSES 1197  
**Status**: Pronto para aplicação em novos experimentos
