# 🎯 PROMPT PARA EXECUÇÃO DO NOTEBOOK FINAL

## 📋 QUANDO USAR ESTE PROMPT:
Após completar TODOS os 15 experimentos (3 de cada categoria), envie este prompt completo para o assistente:

---

## 🚀 **PROMPT DE EXECUÇÃO FINAL:**

```
🎓 TCC NOTEBOOK FINAL - Todos os experimentos completos!

Contexto: Completei todos os 15 experimentos do TCC Adaptive Code Judge seguindo o framework que criamos. Agora preciso gerar o notebook Python final com todos os gráficos e análises.

📊 ESTRUTURA ESPERADA:
- 5 categorias: graphs, dp_iterativa, dp_recursiva, recursao_profunda, backtracking  
- 3 experimentos por categoria = 15 total
- Cada experimento tem metadata_graficos.json padronizado
- Framework automático já desenvolvido

🎯 GRÁFICOS PRÉ-DEFINIDOS:
1. **Gráfico Executivo**: Fatores de ajuste por categoria (barras + IQR)
2. **Heatmap Injustiça**: % TLE Python por categoria vs tamanho input  
3. **Validação Externa**: Scatter CSES real vs nosso benchmark
4. **Before/After**: Correção Python tradicional→adaptativo
5. **Casos Emblemáticos**: 3-4 experimentos narrativos individuais

📈 ANÁLISES AUTOMÁTICAS:
- Estatísticas executivas para TCC
- Evidência contra fator fixo (2x-3x inadequado)
- Correlação com CSES real
- Preservação de seletividade
- Export para LaTeX

🛠️ ARQUIVOS DE REFERÊNCIA:
- documentation/workflows/NOTEBOOK_TEMPLATE.md (código base otimizado)
- documentation/workflows/AUTO_CHECKLIST.py (estrutura de dados)
- Todos os metadata_graficos.json (dados estruturados)

🎓 OBJETIVO TCC:
Gerar notebook publication-ready que prove empiricamente:
1. Injustiça é categórica (fatores variam 3x-40x)
2. Fator fixo é inadequado  
3. Calibração empírica é necessária
4. Correção preserva rigor algorítmico

Por favor, execute o notebook final completo baseado no framework que desenvolvemos!
```

---

## 📝 INFORMAÇÕES COMPLEMENTARES PARA O ASSISTENTE:

### 🔍 Detalhes do Framework Desenvolvido:

**Estrutura de Dados Padronizada:**
```json
{
  "experiment": {"categoria": "", "problema": "", "data": ""},
  "fatores": {"ajuste_mediano": 0.0, "confiabilidade": ""},
  "correcao": {"tradicional_python": 0.0, "adaptativo_python": 0.0},
  "seletividade": {"preservada": true},
  "classificacao": {"prioridade": "Alta|Média|Baixa", "emblematico": true}
}
```

**Gráficos Específicos Acordados:**
1. **Executivo**: Escala Y até 25x, IQR bars, linha 3x referência
2. **Heatmap**: Gradação verde→vermelho, tamanhos reais (N=10³, etc)
3. **Validação**: Scatter + linha y=x + banda confiança
4. **Before/After**: Barras duplas + anotações de melhoria
5. **Emblemáticos**: Problem01 garantido (fator 36.8x)

**Insights Científicos Chave:**
- Problem01: graphs, 36.8x, caso emblemático extremo
- Diversidade de fatores comprova inadequação de fator fixo
- Seletividade preservada em 100% dos casos
- Correlação alta com CSES real (validação externa)

**Output Esperado:**
- 5 gráficos PNG publication-ready
- Estatísticas executivas JSON
- Comandos LaTeX prontos
- Tabelas CSV para importação

### 🎯 Contexto Problem01 (Referência):
- **Categoria**: graphs (CSES 1672)
- **Fator**: 36.84x (extremo)
- **Melhoria**: +50 pontos percentuais
- **Status**: Emblemático, Alta prioridade
- **TLEs confirmados**: casos 8, 12, 15
- **Seletividade**: Preservada (slow solutions TLE)

---

## ⚠️ IMPORTANTE:
- Usar EXATAMENTE este prompt quando todos os experimentos estiverem prontos
- Verificar que todos os 15 experimentos têm metadata_graficos.json
- Confirmar que AUTO_CHECKLIST.py foi executado em todos
- Framework já está testado e validado no Problem01

**Data de criação**: 2025-08-30
**Versão**: 1.0 - Framework completo

