# Protocolo Metodológico Rigoroso - Experimentos TCC

## 🎯 OBJETIVO
Seguir rigorosamente a metodologia estabelecida nos experimentos de grafos para QUALQUER novo problema, garantindo consistência científica e dados válidos para o notebook Python final.

---

## 📋 CHECKLIST OBRIGATÓRIO POR PROBLEMA

### **ESTRUTURA INICIAL** ✅
1. Criar estrutura completa:
   ```
   experiments_realworld/[categoria]/problem[N]/
   ├── tests_cses/                    # Test cases compartilhados
   ├── recursivo/                     # Se aplicável
   │   ├── solutions/
   │   ├── slow_validation/solutions_slow/
   │   ├── results/
   │   └── resultados_finais/
   ├── iterativo/                     # Se aplicável
   │   ├── solutions/
   │   ├── slow_validation/solutions_slow/
   │   ├── results/
   │   └── resultados_finais/
   └── [outros_tipos]/
   ```

### **IMPLEMENTAÇÃO** ✅
2. **Códigos Otimizados**: C++ e Python algoritmicamente equivalentes
3. **Códigos Lentos**: C++ e Python com overhead intencional (EXTRA_WORK)
4. **Prova Formal**: Demonstrar equivalência algorítmica matemática
5. **Scripts**: Adaptar run_benchmark.py, validate_slow_solutions.py, analyze_results.py

---

## 🚀 EXECUÇÃO METODOLÓGICA - ORDEM OBRIGATÓRIA

### **FASE 1: VALIDAÇÃO EXTERNA CSES** 🌐
**AÇÃO REQUIRED**: Usuário deve submeter no CSES e fornecer resultados

#### Submissões Obrigatórias:
1. **C++ Otimizado** → Copiar resultado CSES completo
2. **Python Otimizado** → Copiar resultado CSES completo  
3. **C++ Slow** → Copiar resultado CSES completo
4. **Python Slow** → Copiar resultado CSES completo

#### Template de Resultado CSES:
```
CSES Problem Set
[NOME DO PROBLEMA]
Submission details
Task: [NOME]
Sender: dressa  
Submission time: [DATA]
Language: [C++/Python3]
Status: READY
Result: [ACCEPTED/TLE/RUNTIME ERROR]
Test results
test    verdict    time
#1      [ACCEPTED/TLE]    [TIME]s
#2      [ACCEPTED/TLE]    [TIME]s
...
Code
[CÓDIGO FONTE]
```

**⚠️ CRITICAL**: Todos os 4 resultados CSES são obrigatórios antes de prosseguir!

### **FASE 2: BENCHMARK LOCAL CONTROLADO** 🔬

#### Ordem de Execução:
1. **Calibração**: Test case representativo (não trivial!)
   ```bash
   python3 run_benchmark.py --calibration-case [MEDIUM_CASE] --calibration-reps 5 --time-limit 3.0
   ```
   - **Critério**: Caso que executa em ~0.1-0.5s em ambas linguagens
   - **Evitar**: Casos triviais (x=1, resultado imediato)
   - **Escolher**: Caso que demonstra diferença mensurável de performance

2. **Validação**: Múltiplos test cases incluindo críticos
   ```bash
   python3 run_benchmark.py --validation-cases [SMALL MEDIUM LARGE CRITICAL] --validation-reps 5 --time-limit 3.0
   ```
   - **Mínimo 5 casos**: Progressão de complexidade
   - **Include**: Funcionais (rápidos) + Críticos (quase TLE)
   - **Total execuções**: 5 casos × 5 reps = 25+ execuções

3. **Slow Validation**: Test cases críticos
   ```bash
   python3 validate_slow_solutions.py --test-cases [LARGE CRITICAL] --time-limit 2.0
   ```
   - **Critério**: Casos que levam slow solutions a TLE
   - **Meta**: ≥80% TLE rate para validar seletividade

4. **Análise Final**: Gerar relatório
   ```bash
   python3 analyze_results.py --input=results --output=final_report.json
   ```

### **FASE 3: DOCUMENTAÇÃO CIENTÍFICA** 📝

#### Arquivos Obrigatórios:
1. **formal_proof.md** - Equivalência algorítmica + descobertas
2. **CSES_VALIDATION_RESULTS.md** - Resultados externos documentados
3. **EXECUTIVE_SUMMARY.md** - Sumário executivo completo
4. **NOTEBOOK_INSIGHTS.md** - Insights para notebook Python
5. **STATISTICAL_ANALYSIS.md** - Análise estatística detalhada
6. **metadata_[tipo].json** - Metadados estruturados

---

## 📊 CRITÉRIOS DE QUALIDADE CIENTÍFICA

### **Calibração Confiável** ✅
- C++ IQR < 15%
- Python IQR < 20%
- Fator de ajuste 0.5x - 5.0x (range razoável)

### **Validação Robusta** ✅
- Mínimo 5 test cases
- Mínimo 5 repetições por case
- Include casos funcionais + críticos

### **Seletividade Preservada** ✅
- Slow solutions ≥ 80% TLE rate
- Sistema detecta overhead adequadamente

### **Análise Estatística** ✅
- Experiment Status: SUCCESSFUL
- Dados robustos (≥ 25 execuções total)
- Descobertas cientificamente válidas

---

## 🔄 ADAPTAÇÕES POR CATEGORIA

### **Dynamic Programming**
- **Recursivo**: Top-down com memoização
- **Iterativo**: Bottom-up com tabulation
- **Comparação**: Análise de ambas abordagens obrigatória
- **Insight**: Verificar se injustiça é específica de abordagem

### **Backtracking** (Próximo)
- **Poda Simples**: Backtracking básico
- **Poda Avançada**: Com otimizações de poda
- **Comparação**: Verificar impacto das otimizações
- **Insight**: Analisar recursão profunda vs iteração

### **Greedy** (Futuro)
- **Implementações diretas**: C++ vs Python equivalentes
- **Focus**: Algoritmos com muitas operações de sorting/heap
- **Insight**: Verificar overhead em operações builtin

---

## ⚠️ PONTOS CRÍTICOS DE ATENÇÃO

### **Escolha de Test Cases - Critérios Específicos**

#### **Para Calibração** (1 caso):
- ❌ **NUNCA usar caso trivial** (x=1, n=1, resultado imediato)
- ✅ **Usar caso MÉDIO** que executa em ~0.1-0.5s em ambas linguagens
- ✅ **Verificar diferença mensurável** de performance (>10% gap)
- ✅ **Ambas linguagens devem ACEITAR** (não TLE)

#### **Para Validação** (5+ casos):
- ✅ **SMALL**: Casos funcionais rápidos (<0.1s)
- ✅ **MEDIUM**: Casos representativos (0.1-0.5s) 
- ✅ **LARGE**: Casos pesados (0.5-1.5s)
- ✅ **CRITICAL**: Casos quase-TLE (próximos do limite)
- ✅ **Progressão**: Complexidade crescente para mapear injustiça

#### **Para Slow Validation** (2-3 casos):
- ✅ **Apenas casos LARGE/CRITICAL** que forçam TLE em slow solutions
- ✅ **Meta**: ≥80% TLE rate para confirmar seletividade

### **Validação CSES Obrigatória**
- ❌ **NUNCA prosseguir sem resultados CSES**
- ✅ **Sempre documentar links/códigos compartilhados**
- ✅ **Verificar consistência** entre local e CSES

### **Critérios de Sucesso Experimental**
- ✅ **Para experimentos adaptativos** (como grafos): Melhoria significativa
- ✅ **Para experimentos de refutação** (como DP): Injustiça confirmada + metodologia válida
- ✅ **Sempre**: Calibração confiável + seletividade preservada

---

## 📋 TEMPLATE DE EXECUÇÃO

### **Início de Novo Problema**
```markdown
## Problema: [NOME] - [CATEGORIA]

### Status Checklist:
- [ ] Estrutura criada
- [ ] Códigos otimizados implementados
- [ ] Códigos slow implementados  
- [ ] Prova formal documentada
- [ ] Scripts adaptados

### Submissões CSES Pendentes:
- [ ] C++ Otimizado: [AGUARDANDO USUÁRIO]
- [ ] Python Otimizado: [AGUARDANDO USUÁRIO]
- [ ] C++ Slow: [AGUARDANDO USUÁRIO]  
- [ ] Python Slow: [AGUARDANDO USUÁRIO]

### Benchmarks Pendentes:
- [ ] Calibração executada
- [ ] Validação executada
- [ ] Slow validation executada
- [ ] Análise final executada

### Documentação Pendente:
- [ ] Formal proof
- [ ] CSES validation results
- [ ] Executive summary
- [ ] Notebook insights
- [ ] Statistical analysis
- [ ] Metadata estruturado
```

---

## 🎯 OBJETIVO FINAL

**Cada experimento deve produzir:**
1. **Dados científicos robustos** para notebook Python
2. **Descobertas metodologicamente válidas** para TCC
3. **Documentação completa** para reprodutibilidade
4. **Validação externa** via CSES platform
5. **Análise estatística rigorosa** com critérios científicos

---

## 📞 PROTOCOLO DE COMUNICAÇÃO

### **Quando Precisar de Input do Usuário:**
```
⚠️ AÇÃO NECESSÁRIA: 
Favor submeter [CÓDIGO] no CSES e fornecer resultado completo 
(incluindo test details e link de compartilhamento)
```

### **Quando Reportar Progresso:**
```
✅ FASE CONCLUÍDA: [NOME]
Próximo passo: [AÇÃO]
Status geral: [X/Y] fases completas
```

### **Quando Identificar Problemas:**
```
🚨 PROBLEMA IDENTIFICADO: [DESCRIÇÃO]
Correção necessária: [AÇÃO]
Impacto: [BAIXO/MÉDIO/ALTO]
```

---

**ESTE PROTOCOLO É OBRIGATÓRIO PARA TODOS OS PRÓXIMOS EXPERIMENTOS**
**SEGUIR RIGOROSAMENTE PARA GARANTIR QUALIDADE CIENTÍFICA MÁXIMA**
