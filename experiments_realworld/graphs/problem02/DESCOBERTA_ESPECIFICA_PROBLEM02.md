# DESCOBERTA ESPECÍFICA - PROBLEM02

## Experimento: CSES 1197 - Cycle Finding

### Contexto Específico
Este experimento foi o **primeiro caso de aplicação** da metodologia de Análise Binária de Veredicto, servindo como prova de conceito e validação inicial.

### Descoberta Durante o Experimento
Durante a execução do Problem02, identificamos que nossa metodologia inicial estava **mascarando injustiças reais**:

**❌ Resultado Inicial (Metodologia Incorreta):**
```
Sistema Tradicional: C++ ✅ ACCEPTED, Python ✅ ACCEPTED
Sistema Adaptativo:  C++ ✅ ACCEPTED, Python ✅ ACCEPTED
Conclusão: Sem injustiça detectada
```

**✅ Resultado Corrigido (Metodologia Binária):**
```
Sistema Tradicional: C++ ✅ ACCEPTED, Python ❌ REJECTED
Sistema Adaptativo:  C++ ✅ ACCEPTED, Python ✅ ACCEPTED
Conclusão: Injustiça detectada e corrigida
```

### Parâmetros Específicos do Problem02
- **Algoritmo**: Bellman-Ford para detecção de ciclos negativos
- **Complexidade**: O(nm) onde n=nós, m=arestas
- **Casos críticos**: 6, 7, 8, 9, 10, 13, 19, 21, 27
- **Fator de ajuste**: 4.33x
- **Limite rigoroso**: 1.0s (igual ao CSES)

### Validação Específica
- **Validação externa**: Dados reais do CSES (submissões 14361359, 14361394)
- **Slow solutions**: TLE garantido com EXTRA_PASSES=150
- **Validação inteligente**: Múltiplas saídas válidas para ciclos negativos

### Resultados Específicos
- **Injustiça detectada**: ✅ Python rejeitado no sistema tradicional
- **Injustiça corrigida**: ✅ Python aprovado no sistema adaptativo
- **Seletividade preservada**: ✅ Slow solutions continuam rejeitadas
- **Casos resgatados**: 6 de 9 casos críticos

### Contribuição para Metodologia Geral
Este experimento:
1. **Revelou** a necessidade da análise binária
2. **Validou** a eficácia da metodologia
3. **Estabeleceu** o protocolo para experimentos futuros
4. **Demonstrou** aplicabilidade prática

### Lições Específicas Aprendidas
1. **Limites permissivos** (2.0s) mascaram injustiças
2. **Casos críticos** são mais informativos que amostras aleatórias
3. **Validação externa** é essencial para credibilidade
4. **Status de erro** pode variar ("TLE" vs "TIME_LIMIT_EXCEEDED")

### Arquivos Específicos Gerados
- `BINARY_VERDICT_REPORT.md` - Relatório científico dos resultados
- `binary_verdict_analysis.json` - Dados da análise binária
- `analyze_binary_verdict.py` - Script de análise (reutilizável)
- `results/validation_results.json` - Dados experimentais

### Status do Experimento
- ✅ **Metodologia validada**
- ✅ **Injustiça detectada e corrigida**
- ✅ **Documentação completa**
- ✅ **Pronto para inclusão no TCC**

### Próximos Passos
1. **Aplicar metodologia** aos próximos experimentos
2. **Usar como referência** para validação
3. **Incluir como caso emblemático** na dissertação

---
**Experimento**: Problem02 - CSES 1197 Cycle Finding  
**Data**: 2025-08-30  
**Status**: ✅ Concluído com sucesso científico  
**Contribuição**: Primeira validação da metodologia binária
