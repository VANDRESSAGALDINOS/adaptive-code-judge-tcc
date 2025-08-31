# AUTOMAÇÃO DE CHECKLISTS E VALIDAÇÃO

## Visão Geral

Este documento centraliza todos os scripts e processos automatizados para validação de experimentos, garantindo consistência e qualidade em todos os experimentos.

## Scripts Disponíveis

### 1. AUTO_CHECKLIST.py
**Função**: Checklist automático pós-experimento

**Uso**:
```bash
cd documentation/workflows
python AUTO_CHECKLIST.py /path/to/experiment/
```

**Validações Automáticas**:
- ✅ Presença de arquivos obrigatórios
- ✅ Estrutura de dados válida
- ✅ Critérios de qualidade atendidos
- ✅ Geração de metadata_graficos.json
- ✅ Classificação de prioridade

### 2. CHECKLIST_EXPERIMENTO.py
**Função**: Checklist interativo (backup)

**Uso**:
```bash
cd documentation/workflows
python CHECKLIST_EXPERIMENTO.py /path/to/experiment/
```

**Validações Interativas**:
- 🔄 Perguntas de validação manual
- 🔄 Confirmação de critérios
- 🔄 Classificação assistida

### 3. TEMPLATE_EXPERIMENTO.md
**Função**: Template padronizado para novos experimentos

**Uso**:
```bash
cp documentation/workflows/TEMPLATE_EXPERIMENTO.md experiments_realworld/categoria/problemXX/
```

**Inclui**:
- 📋 Estrutura padrão de documentação
- 📋 Seções obrigatórias
- 📋 Formato de metadados
- 📋 Checklist integrado

## Critérios de Validação Automática

### Arquivos Obrigatórios
```python
REQUIRED_FILES = [
    "experiment_metadata.json",
    "results/calibration_*.json",
    "results/validation_results.json", 
    "results/slow_solution_validation.json",
    "BINARY_VERDICT_REPORT.md",
    "binary_verdict_analysis.json"
]
```

### Critérios de Qualidade
```python
QUALITY_CRITERIA = {
    "fator_realista": "< 50x",
    "confiabilidade_alta": "IQR < 0.15",
    "correlacao_externa": "> 0.7",
    "seletividade_preservada": "slow_solutions TLE",
    "injustica_detectada": "binary_verdict == True",
    "dados_suficientes": "repetitions >= 10"
}
```

### Classificação de Prioridade
```python
def classify_priority(experiment_data):
    if (experiment_data["emblematico"] and 
        experiment_data["representa_categoria"] and
        experiment_data["confiabilidade"] == "Alta"):
        return "Alta"
    elif (experiment_data["representa_categoria"] and
          experiment_data["confiabilidade"] in ["Alta", "Média"]):
        return "Média"
    else:
        return "Baixa"
```

## Estrutura de Metadados Gerada

### metadata_graficos.json
```json
{
  "experiment": {
    "categoria": "graphs|dp_iterativa|dp_recursiva|recursao_profunda|backtracking",
    "problema": "problemXX",
    "data": "2025-08-30",
    "status": "completo"
  },
  "fatores": {
    "ajuste_mediano": 0.0,
    "confiabilidade": "Alta|Média|Baixa",
    "iqr_cpp": 0.0,
    "iqr_python": 0.0
  },
  "correcao": {
    "tradicional_python": 0.0,
    "adaptativo_python": 100.0,
    "melhoria": 0.0,
    "metodologia_binaria": {
      "tradicional_cpp": "ACCEPTED|REJECTED",
      "tradicional_python": "ACCEPTED|REJECTED",
      "adaptativo_cpp": "ACCEPTED|REJECTED",
      "adaptativo_python": "ACCEPTED|REJECTED",
      "injustica_detectada": true,
      "injustica_corrigida": true,
      "python_resgatado": true
    }
  },
  "seletividade": {
    "preservada": true
  },
  "validacao": {
    "score": 100.0,
    "all_valid": true,
    "criteria": {
      "fator_realista": true,
      "tres_tamanhos": true,
      "slow_solutions_tle": true,
      "correlacao_verificada": true,
      "insights_documentados": true,
      "confiabilidade_alta": true
    }
  },
  "classificacao": {
    "emblematico": true,
    "representa_categoria": true,
    "dados_suficientes": true,
    "prioridade": "Alta|Média|Baixa",
    "score": 100.0
  },
  "para_graficos": {
    "incluir_executivo": true,
    "incluir_heatmap": true,
    "caso_narrativo": true,
    "prioridade": "Alta|Média|Baixa"
  }
}
```

## Workflow de Automação

### Processo Padrão
```bash
# 1. Após completar experimento
cd /path/to/experiment/

# 2. Executar análise binária
python analyze_binary_verdict.py

# 3. Executar checklist automático
python /path/to/documentation/workflows/AUTO_CHECKLIST.py .

# 4. Verificar outputs
ls -la metadata_graficos.json
cat RESUMO_AUTO_ANALISE.md
```

### Validação em Lote
```bash
# Para validar múltiplos experimentos
for exp in experiments_realworld/*/problem*/; do
    echo "Validando: $exp"
    python documentation/workflows/AUTO_CHECKLIST.py "$exp"
done
```

## Integração com Notebook Final

### Coleta Automática de Dados
```python
def load_all_experiments():
    """Carrega automaticamente todos os experimentos validados"""
    experiments = []
    
    for metadata_file in Path('experiments_realworld').rglob('metadata_graficos.json'):
        with open(metadata_file) as f:
            data = json.load(f)
            experiments.append(data)
    
    return pd.DataFrame(experiments)
```

### Filtros de Qualidade
```python
def filter_valid_experiments(df):
    """Filtra apenas experimentos que atendem critérios de qualidade"""
    return df[
        (df['validacao.all_valid'] == True) &
        (df['classificacao.score'] >= 80) &
        (df['seletividade.preservada'] == True)
    ]
```

## Troubleshooting

### Problemas Comuns

#### Arquivo metadata_graficos.json não gerado
**Causa**: Dados insuficientes ou critérios não atendidos
**Solução**: 
```bash
python AUTO_CHECKLIST.py --debug /path/to/experiment/
```

#### Score baixo no checklist
**Causa**: Critérios de qualidade não atendidos
**Solução**: Verificar logs detalhados e corrigir dados

#### Classificação "Baixa" inesperada
**Causa**: Experimento não representa categoria ou tem baixa confiabilidade
**Solução**: Revisar dados e metodologia

### Logs e Debug
```python
# Habilitar logs detalhados
python AUTO_CHECKLIST.py --verbose --debug /path/to/experiment/

# Verificar critérios específicos
python AUTO_CHECKLIST.py --check-criteria /path/to/experiment/
```

## Manutenção

### Atualizações de Critérios
1. **Modificar** critérios em `AUTO_CHECKLIST.py`
2. **Testar** em experimento piloto
3. **Aplicar** a todos os experimentos
4. **Documentar** mudanças

### Versionamento
- **v1.0**: Automação básica
- **v1.1**: Validação binária integrada
- **v1.2**: Classificação automática de prioridade

---
**Automação**: Checklists e Validação v1.2  
**Scripts**: Python 3.11+ compatível  
**Status**: Testado e validado em Problem01 e Problem02  
**Localização**: `documentation/workflows/`
