# WORKFLOWS E PROCESSOS ORGANIZACIONAIS

## Visão Geral

Esta pasta contém todos os workflows, processos e templates organizacionais do projeto, centralizados para fácil acesso e manutenção.

## Estrutura de Workflows

```
workflows/
├── README.md                           # Este arquivo - índice geral
├── EXPERIMENTAL_WORKFLOW.md            # Processo completo por experimento
├── FINAL_ANALYSIS_WORKFLOW.md          # Processo para análise final
├── NOTEBOOK_TEMPLATE.md                # Template do notebook Python
└── CHECKLIST_AUTOMATION.md             # Automação de checklists
```

## Workflows Disponíveis

### 🔬 Workflow Experimental
**Arquivo**: `EXPERIMENTAL_WORKFLOW.md`

**Descrição**: Processo completo para execução de um experimento individual.

**Quando usar**: A cada novo experimento (Problem01, Problem02, etc.)

**Inclui**:
- Checklist pré-experimento
- Configuração obrigatória
- Critérios de validação
- Documentação necessária
- Classificação de prioridade

### 📊 Workflow de Análise Final
**Arquivo**: `FINAL_ANALYSIS_WORKFLOW.md`

**Descrição**: Processo para gerar análise final quando todos os experimentos estiverem completos.

**Quando usar**: Após completar todos os 15 experimentos planejados

**Inclui**:
- Prompt completo para assistente
- Verificação de pré-requisitos
- Instruções de execução
- Outputs esperados

### 💻 Template do Notebook
**Arquivo**: `NOTEBOOK_TEMPLATE.md`

**Descrição**: Código Python completo para o notebook de análise final.

**Quando usar**: Como base para implementação do notebook final

**Inclui**:
- Código Python completo
- 5 gráficos pré-definidos
- Estatísticas executivas
- Export para LaTeX

### 🤖 Automação de Checklists
**Arquivo**: `CHECKLIST_AUTOMATION.md`

**Descrição**: Scripts e processos automatizados para validação.

**Quando usar**: Para automatizar verificações repetitivas

**Inclui**:
- Scripts de validação automática
- Critérios de qualidade
- Geração de metadados

## Como Usar os Workflows

### Para Novos Experimentos
1. **Consulte** `EXPERIMENTAL_WORKFLOW.md`
2. **Siga** o checklist passo a passo
3. **Execute** scripts de automação
4. **Valide** critérios de qualidade

### Para Análise Final
1. **Verifique** que todos os experimentos estão completos
2. **Use** o prompt de `FINAL_ANALYSIS_WORKFLOW.md`
3. **Execute** o código de `NOTEBOOK_TEMPLATE.md`
4. **Valide** outputs gerados

### Para Manutenção
1. **Atualize** workflows conforme necessário
2. **Documente** mudanças de processo
3. **Mantenha** consistência entre experimentos

## Vantagens da Centralização

### 1. Facilidade de Acesso
- **Localização única** para todos os processos
- **Navegação clara** através do README
- **Referência rápida** durante experimentos

### 2. Manutenibilidade
- **Atualizações centralizadas** afetam todos os experimentos
- **Versionamento** de processos
- **Consistência** garantida

### 3. Escalabilidade
- **Novos workflows** facilmente adicionados
- **Processos reutilizáveis** para diferentes categorias
- **Automação** progressiva

### 4. Organização Técnica
- **Separação clara** entre metodologia e processo
- **Workflows específicos** para diferentes fases
- **Documentação estruturada**

## Integração com Projeto

### Referências nos Experimentos
Cada experimento deve referenciar os workflows apropriados:

```markdown
# Problem XX
## Processo Seguido
- Workflow: documentation/workflows/EXPERIMENTAL_WORKFLOW.md
- Checklist: Executado via CHECKLIST_AUTOMATION.md
- Validação: Critérios de EXPERIMENTAL_WORKFLOW.md atendidos
```

### Automação
Scripts automatizados devem referenciar workflows:

```python
# AUTO_CHECKLIST.py
WORKFLOW_REFERENCE = "documentation/workflows/EXPERIMENTAL_WORKFLOW.md"
```

## Histórico de Versões

### v1.0 (2025-08-30)
- ✅ Workflows centralizados
- ✅ Processo experimental padronizado
- ✅ Template de notebook completo
- ✅ Automação de checklists

### Planejado v1.1
- 🔄 Workflow para múltiplas plataformas
- 🔄 Automação completa de experimentos
- 🔄 Integração com CI/CD

## Contribuições

### Como Melhorar os Workflows
1. **Identifique** pontos de melhoria durante uso
2. **Documente** sugestões de otimização
3. **Teste** mudanças em experimentos piloto
4. **Atualize** workflows centralmente

### Critérios de Qualidade
- **Clareza**: Instruções inequívocas
- **Completude**: Todos os passos cobertos
- **Automação**: Máximo de automação possível
- **Flexibilidade**: Adaptável a diferentes cenários

---
**Workflows**: Organizacionais e Técnicos v1.0  
**Escopo**: Experimentos de Injustiça Linguística  
**Status**: Centralizados e prontos para uso  
**Manutenção**: Centralizada nesta pasta
