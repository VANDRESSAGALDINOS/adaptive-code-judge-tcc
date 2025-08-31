# 🎯 PROMPT DE LEMBRETE - EXECUTAR A CADA EXPERIMENTO

## 📋 ANTES DE COMEÇAR UM NOVO EXPERIMENTO

### 1. Configuração Inicial
```bash
# Copiar template
cp experiments_realworld/TEMPLATE_EXPERIMENTO.md experiments_realworld/[categoria]/[problema]/

# Preencher metadados obrigatórios no template
# - categoria, problema_id, complexidade_algoritmica
# - data_experimento, plataforma_origem
```

### 2. Durante a Execução
**SEMPRE coletar:**
- ✅ Pelo menos 3 tamanhos de input diferentes
- ✅ Mínimo 10 repetições por caso para estabilidade
- ✅ Dados de validação vs plataforma real (CSES/AtCoder)
- ✅ Teste de slow solutions em ambos sistemas

## 📊 APÓS COMPLETAR O EXPERIMENTO

### 3. Executar Checklist Automático
```bash
cd experiments_realworld
python CHECKLIST_EXPERIMENTO.py [categoria]/[problema]/

# Responder todas as perguntas do checklist
# Confirmar que todas as métricas foram coletadas
```

### 4. Dados Obrigatórios para Gráficos Finais

**Para Gráfico Executivo (Fatores por Categoria):**
- [ ] Fator de ajuste mediano calculado
- [ ] IQR do fator documentado
- [ ] Confiabilidade classificada (Alta/Média/Baixa)

**Para Heatmap de Injustiça:**
- [ ] Pelo menos 3 tamanhos: pequeno (~10²), médio (~10³), grande (~10⁴)
- [ ] Taxa de TLE Python para cada tamanho
- [ ] Confirmação de padrão crescente com tamanho

**Para Validação Externa:**
- [ ] Taxa TLE real da plataforma (CSES/AtCoder) documentada
- [ ] Comparação com nossa taxa TLE calculada
- [ ] Diferença absoluta < 15% (critério de validade)

**Para Before/After:**
- [ ] Success rate Python no sistema tradicional
- [ ] Success rate Python no sistema adaptativo
- [ ] Casos onde Python ainda falha (para mostrar rigor)

**Para Seletividade:**
- [ ] Slow solutions testadas nos 2 sistemas
- [ ] Confirmação de TLE em ambos (preservação de rigor)

## 🎯 CLASSIFICAÇÃO DO EXPERIMENTO

### 5. Critérios de Qualidade
**Experimento válido se:**
- ✅ Fator < 50x (realista)
- ✅ Correlação com plataforma real > 0.7
- ✅ Seletividade preservada
- ✅ IQR < 30% (estável)

### 6. Prioridade para Gráficos Finais
**Alta prioridade se:**
- ✅ Emblemático da categoria
- ✅ Representa comportamento típico
- ✅ Dados limpos e confiáveis

**Média prioridade se:**
- ✅ Representa categoria
- ✅ Dados confiáveis
- ❌ Não emblemático

**Baixa prioridade:**
- ⚠️ Caso atípico ou problemático
- ✅ Mas com insights valiosos

## 📝 DOCUMENTAÇÃO OBRIGATÓRIA

### 7. Arquivos que DEVEM existir:
- [ ] `experiment_plan.md` - metodologia
- [ ] `final_report.json` - dados completos
- [ ] `results/calibration_*.json` - dados de calibração
- [ ] `results/validation_results.json` - dados de validação
- [ ] `results/slow_solution_validation.json` - seletividade
- [ ] `resultados_finais/README.md` - resumo executivo
- [ ] `metadata_graficos.json` - dados estruturados para Python

### 8. Insights Específicos Documentar:
- [ ] **Anomalias**: Comportamentos inesperados
- [ ] **Bottlenecks**: CPU, memória, I/O dominante?
- [ ] **Padrões únicos**: Características da categoria
- [ ] **Limitações**: Casos onde método falha

## 🔗 PREPARAÇÃO PARA ANÁLISE FINAL

### 9. Quando Tiver 15 Experimentos Completos:
```bash
# Executar consolidação automática
python generate_final_analysis.py

# Gerar todos os gráficos
jupyter notebook final_analysis.ipynb

# Verificar se todos os insights estão capturados
```

### 10. Estrutura Final para TCC:
- **3-4 casos narrativos** individuais (Alta prioridade)
- **Gráfico executivo** com todos os fatores
- **Heatmap** com todas as categorias
- **Validação** com correlação externa
- **Before/After** mostrando correção responsável

---

## 🚨 LEMBRETE CRÍTICO

**NUNCA pular o checklist!** Cada experimento que não seguir este processo vai dificultar a análise final e comprometer a qualidade dos gráficos do TCC.

**A cada experimento concluído, executar:**
1. `python CHECKLIST_EXPERIMENTO.py`
2. Verificar se `metadata_graficos.json` foi gerado
3. Confirmar prioridade para gráficos finais
4. Documentar insights específicos no template

---
**Data de criação**: {datetime.now().strftime('%Y-%m-%d')}
**Versão**: 1.0

