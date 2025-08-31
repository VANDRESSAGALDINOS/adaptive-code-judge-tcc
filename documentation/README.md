# DOCUMENTAÇÃO DO PROJETO - ADAPTIVE CODE JUDGE

## Visão Geral

Esta pasta contém toda a documentação técnica e metodológica do projeto Adaptive Code Judge, organizada de forma hierárquica para facilitar navegação e manutenção.

## Estrutura da Documentação

```
documentation/
├── README.md                    # Este arquivo - índice geral
├── methodology/                 # Metodologias desenvolvidas
│   └── ANALISE_BINARIA_VEREDICTO.md  # Metodologia principal
├── protocols/                   # Protocolos experimentais
│   └── PROTOCOLO_EXPERIMENTAL_GERAL.md  # Protocolo padronizado
├── frameworks/                  # Frameworks reutilizáveis
│   └── BINARY_VERDICT_FRAMEWORK.md  # Framework de implementação
├── workflows/                   # Workflows e processos organizacionais
│   ├── README.md                # Índice de workflows
│   ├── EXPERIMENTAL_WORKFLOW.md # Processo por experimento
│   ├── FINAL_ANALYSIS_WORKFLOW.md # Processo análise final
│   ├── NOTEBOOK_TEMPLATE.md     # Template notebook Python
│   ├── CHECKLIST_AUTOMATION.md  # Automação de validação
│   ├── AUTO_CHECKLIST.py        # Script checklist automático
│   ├── CHECKLIST_EXPERIMENTO.py # Script checklist interativo
│   └── TEMPLATE_EXPERIMENTO.md  # Template experimento
└── insights/                    # Descobertas científicas gerais
```

## Metodologias Desenvolvidas

### 🔬 Análise Binária de Veredicto
**Arquivo**: `methodology/ANALISE_BINARIA_VEREDICTO.md`

**Descrição**: Metodologia fundamental para detecção objetiva de injustiças linguísticas em juízes online.

**Principais Contribuições**:
- Simulação exata da lógica de plataformas reais
- Critérios binários objetivos (ACCEPTED/REJECTED)
- Framework replicável para qualquer plataforma
- Primeira formalização científica na área

**Aplicabilidade**: CSES, AtCoder, LeetCode, HackerRank, qualquer juiz online

**Status**: ✅ Validada e pronta para replicação

## Workflows e Processos

### 🔄 Workflow Experimental
**Arquivo**: `workflows/EXPERIMENTAL_WORKFLOW.md`

**Descrição**: Processo completo para execução de experimentos individuais com checklist automático e critérios de validação.

**Aplicabilidade**: Todos os experimentos do projeto

**Status**: ✅ Testado e validado

### 📊 Workflow de Análise Final
**Arquivo**: `workflows/FINAL_ANALYSIS_WORKFLOW.md`

**Descrição**: Processo para geração automática de notebook Python com todos os gráficos e análises finais para TCC.

**Aplicabilidade**: Após completar todos os 15 experimentos

**Status**: ✅ Framework completo e pronto

### 🤖 Automação de Checklists
**Arquivo**: `workflows/CHECKLIST_AUTOMATION.md`

**Descrição**: Scripts automatizados para validação de qualidade e geração de metadados estruturados.

**Aplicabilidade**: Todos os experimentos

**Status**: ✅ Implementado e funcional

## Descobertas Científicas

### Problem02 - Evolução Metodológica
- **Descoberta**: Análise estatística mascarava injustiças reais
- **Solução**: Desenvolvimento da análise binária
- **Impacto**: Transformação de experimento inconclusivo em evidência científica sólida

## Protocolos Experimentais

### Protocolo Geral para Experimentos
1. **Identificação de casos críticos** via dados externos
2. **Configuração de parâmetros realistas**
3. **Execução com análise binária**
4. **Validação externa** quando possível

## Como Usar Esta Documentação

### Para Pesquisadores
1. **Leia** `methodology/ANALISE_BINARIA_VEREDICTO.md` para entender a base metodológica
2. **Aplique** o protocolo aos seus experimentos
3. **Contribua** com novas descobertas e extensões

### Para Desenvolvedores
1. **Implemente** os scripts de análise binária
2. **Adapte** para sua plataforma específica
3. **Valide** com dados reais da plataforma

### Para Auditores
1. **Use** como framework de avaliação de fairness
2. **Aplique** critérios objetivos de detecção
3. **Documente** resultados para transparência

## Contribuições Futuras

### Metodologias Planejadas
- **Análise Multi-dimensional**: Além de TLE, incluir outros tipos de erro
- **Métricas de Fairness**: Índices quantitativos de equidade
- **Automação Completa**: Pipeline end-to-end para auditoria

### Protocolos em Desenvolvimento
- **Certificação de Plataformas**: Processo para selo de fairness
- **Benchmark Padronizado**: Conjunto de testes de referência
- **Validação Cruzada**: Protocolo para comparação entre plataformas

## Histórico de Versões

### v1.0 (2025-08-30)
- ✅ Análise Binária de Veredicto implementada
- ✅ Validação em Problem02 (CSES 1197)
- ✅ Framework básico estabelecido

### Planejado v1.1
- 🔄 Extensão para múltiplas plataformas
- 🔄 Automação de coleta de dados externos
- 🔄 Interface web para auditoria

## Licença e Uso

Esta documentação é parte do projeto acadêmico Adaptive Code Judge e está disponível para:
- **Uso acadêmico**: Pesquisas e estudos científicos
- **Uso educacional**: Ensino de metodologias de pesquisa
- **Uso prático**: Auditoria de fairness em plataformas

## Contato e Contribuições

Para contribuições, sugestões ou questões sobre as metodologias:
- **Projeto**: Adaptive Code Judge TCC
- **Instituição**: UFCG - Universidade Federal de Campina Grande
- **Área**: Ciência da Computação - Sistemas Computacionais

---
**Última atualização**: 2025-08-30  
**Versão da documentação**: 1.0  
**Status**: Em desenvolvimento ativo
