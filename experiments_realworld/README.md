# Real-World Experiments - Language Bias Detection and Correction

## **Contexto e Propósito**

### **Objetivo Principal**
Esta pasta contém experimentos reais para demonstrar, quantificar e corrigir injustiças sistemáticas entre linguagens de programação (C++ vs Python) em plataformas de juízes online, usando problemas reais e metodologia científica rigorosa.

### **Diferencial vs Experimentos Teóricos**
- **`experiments/`**: Experimentos teóricos com 6 classes de complexidade (O(1) até O(2ⁿ))
- **`experiments_realworld/`**: Experimentos com problemas reais de plataformas (CSES, AtCoder) 

## **Estrutura Organizacional**

```
experiments_realworld/
├── README.md                    # Este arquivo - contexto geral
├── graphs/                      # Problemas de grafos (alta penalização Python)
│   └── problem01/              # CSES 1672 - Shortest Routes II (PRINCIPAL)
├── dp/                         # Dynamic Programming (média penalização)
├── backtracking/               # Backtracking (alta penalização)
└── recursion/                  # Recursão profunda (alta penalização)
```

## **Problem01 - Experimento Principal (COMPLETO)**

### **Status: Pronto para Implementação de Benchmark**

O `graphs/problem01/` contém o experimento principal completamente preparado:

#### **Conteúdo Disponível:**
```
graphs/problem01/
├── problem_description.md       # Descrição acadêmica completa
├── experiment_plan.md          # PLANO DE AÇÃO DETALHADO
├── formal_proof.md             # Prova matemática de equivalência
├── experiment_metadata.json    # Metadados estruturados
├── solutions/                  # Implementações eficientes
│   ├── solution.cpp            # C++ otimizado (CSES ACCEPTED)
│   └── solution.py             # Python equivalente
├── tests_cses/                 # 16 casos de teste oficiais
│   ├── 1.in + 1.out           # Casos pequenos (controle)
│   ├── 8.in + 8.out           # Caso principal (calibração) 
│   ├── 12.in + 12.out         # Alta densidade
│   ├── 15.in + 15.out         # Máxima densidade
│   └── ...                    # Todos os 16 casos
└── slow_validation/            # Validação de seletividade
    ├── slow_solutions_description.md  # Metodologia soluções lentas
    ├── tle_validation_report.md       # Template de resultados
    └── solutions_slow/                # Soluções O(n⁴) 
        ├── slow_solution.cpp          # C++ deliberadamente lento
        └── slow_solution.py           # Python deliberadamente lento
```

#### **Validação Externa Já Realizada:**
```
CSES Submissions Documentadas:
✅ C++ Eficiente: https://cses.fi/problemset/result/14297533/ (ACCEPTED)
✅ C++ Lento: https://cses.fi/problemset/result/14298232/ (TLE - seletividade)
✅ Python Lento: https://cses.fi/problemset/result/14298238/ (TLE - seletividade)

Evidência de Injustiça: Python eficiente falha em 9/16 casos (56%) no CSES
```

## **Plano de Ação - Localização**

### **Documento Principal: `graphs/problem01/experiment_plan.md`**

O plano de ação completo está em **`experiments_realworld/graphs/problem01/experiment_plan.md`** contendo:

1. **Metodologia detalhada** (5 fases experimentais)
2. **Protocolo de execução** (Docker, repetições, métricas)
3. **Estratégia otimizada** (6 casos estratégicos vs 16 totais)
4. **Critérios de sucesso** (quantitativos e explícitos)
5. **Timeline realista** (5 dias → implementação imediata)

### **Resumo Executivo do Plano:**

#### **Fase 1: Calibração (Test Case #8)**
```bash
Objetivo: Calcular fator de ajuste Python/C++
Método: 15 repetições no caso crítico maior
Tempo: ~1 minuto de execução
Output: adjustment_factor (esperado: ~2.8x)
```

#### **Fase 2: Validação (6 casos estratégicos)**
```bash
Casos Críticos: #8, #12, #15 (TLE em Python tradicional)
Casos Controle: #1, #13, #16 (ACCEPTED em Python tradicional)
Método: 5 repetições × 4 condições (tradicional vs adaptativo)
Tempo: ~2 minutos de execução
```

#### **Fase 3: Análise Estatística**
```bash
Métricas Principais:
- tle_reduction_absolute (esperado: 50+ pontos percentuais)
- cases_rescued (esperado: 3 casos críticos)
- adjustment_factor (esperado: 2.5-3.0x)
```

## **O Que Implementar No Mac**

### **Próximos Passos Específicos:**

#### **1. Script de Benchmark Principal:**
```bash
# Criar: experiments_realworld/graphs/problem01/run_benchmark.py
# Função: Executar protocolo experimental automatizado
# Base: experiment_plan.md seções 4.2-4.4
```

#### **2. Ambiente Docker Setup:**
```bash
# Setup de containers isolados para C++ e Python
# Compilação padronizada e execução controlada
# Base: experiment_plan.md seção 4.1
```

#### **3. Script de Análise Estatística:**
```bash
# Criar: experiments_realworld/graphs/problem01/analyze_results.py
# Função: Processar tempos, calcular métricas, gerar relatórios
# Base: experiment_plan.md seção 5
```

#### **4. Validação de Seletividade:**
```bash
# Executar soluções lentas localmente
# Confirmar TLE em ambas linguagens (mesmo com ajuste)
# Base: slow_validation/slow_solutions_description.md
```

### **Arquivos de Saída Esperados:**
```
results/
├── calibration_results.json       # Dados de calibração
├── validation_results.json        # Dados de validação sistêmica  
├── statistical_analysis.json      # Métricas calculadas
├── benchmark_summary.md           # Relatório executivo
└── execution_logs/                # Logs detalhados
```

## **Metodologia Científica Aplicada**

### **Framework Estabelecido:**
1. **Equivalência Formal** ✅ (prova matemática completa)
2. **Validação Externa** ✅ (submissões CSES documentadas)
3. **Benchmark Controlado** ⏳ (implementação pendente)
4. **Análise Estatística** ⏳ (implementação pendente)
5. **Seletividade Validation** ⏳ (implementação pendente)

### **Rigor Experimental:**
- Ambiente Docker isolado
- Test cases oficiais (16 casos CSES)
- Repetições estatisticamente adequadas (15+5)
- Métricas zero-division-safe
- Validação cross-platform

## **Valor Para TCC**

### **Contribuições Esperadas:**
1. **Injustiça Quantificada**: Primeira medição sistemática (56% casos Python TLE)
2. **Solução Validada**: Sistema adaptativo com fator empírico (2.8x)
3. **Seletividade Preservada**: Anti-gaming via soluções ineficientes
4. **Framework Replicável**: Metodologia para outras linguagens/plataformas

### **Timeline de Execução:**
```
Implementação: 4-6 horas (scripts + Docker setup)
Execução: 5 minutos (benchmark automatizado)
Análise: 1-2 horas (estatísticas + relatórios)
Total: 1 dia de trabalho concentrado
```

## **Status dos Outros Problemas**

### **Graphs/DP/Backtracking/Recursion Problem02/03:**
```
Status: Estrutura criada, mas placeholders vazios
Prioridade: Baixa (problem01 é suficiente para TCC)
Uso Futuro: Expansão opcional para validação adicional
```

### **Recomendação:**
**Focar 100% no graphs/problem01 - é completo e suficiente para demonstrar toda a metodologia e obter resultados de alto impacto para o TCC.**

---

## **Resumo para Continuação**

### **Você tem:**
✅ Problema real validado externamente  
✅ Metodologia científica rigorosa  
✅ Documentação acadêmica completa  
✅ Plano de execução otimizado  
✅ Estrutura experimental organizada  

### **Você precisa implementar:**
⏳ Scripts de benchmark automatizado  
⏳ Análise estatística dos resultados  
⏳ Relatórios finais para TCC  

### **Localização do Plano:**
📍 **`experiments_realworld/graphs/problem01/experiment_plan.md`**

**Este é o documento principal para implementação - contém todos os detalhes técnicos, comandos, protocolos e especificações necessárias.**
