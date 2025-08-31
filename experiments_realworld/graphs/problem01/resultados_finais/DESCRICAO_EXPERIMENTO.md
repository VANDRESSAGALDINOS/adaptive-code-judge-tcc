# Experimento Problem01: CSES 1672 - Shortest Routes II

## Resumo Executivo

Este experimento validou empiricamente a existência de injustiça sistemática entre linguagens de programação em juízes online competitivos, implementando e testando uma solução adaptativa baseada em fatores de ajuste empiricamente derivados.

## Objetivos

### Objetivo Principal
Demonstrar que sistemas de time limits adaptativos podem corrigir injustiças linguísticas em juízes online sem comprometer a seletividade algorítmica.

### Objetivos Específicos
1. **Quantificar injustiça sistemática** entre C++ e Python no problema CSES 1672
2. **Calibrar fator de ajuste empiricamente** através de benchmarking controlado
3. **Validar correção de injustiça** mantendo rigor algorítmico
4. **Preservar performance de C++** (evitar regressão)
5. **Manter seletividade** (slow solutions ainda resultam em TLE)

## Metodologia

### Ambiente Experimental
- **Problema**: CSES 1672 - Shortest Routes II (Floyd-Warshall)
- **Linguagens**: C++ (gcc:latest -O3) vs Python (python:3.11-slim)
- **Plataforma**: Docker containerizado para isolamento
- **Dados**: 16 test cases oficiais do CSES
- **Algoritmo**: Floyd-Warshall O(n³) equivalente matemático

### Fases do Experimento

#### Fase 1: Calibração Controlada
- **Test Case**: #8 (caso crítico conhecido)
- **Repetições**: 15 execuções por linguagem
- **Método**: Benchmark direto com medição de tempo de execução
- **Objetivo**: Derivar fator de ajuste empiricamente

#### Fase 2: Validação Estratégica
- **Test Cases**: 1, 8, 12, 13, 15, 16 (controle + críticos)
- **Repetições**: 3 execuções por caso por linguagem
- **Sistemas**: Tradicional (1.0s) vs Adaptativo (C++: 1.0s, Python: 36.8s)
- **Objetivo**: Demonstrar correção de injustiça

#### Fase 3: Validação de Seletividade
- **Slow Solutions**: O(n⁴) artificialmente lentas
- **Objetivo**: Garantir que soluções inadequadas ainda resultem em TLE

## Protocolo Científico

### Controles Experimentais
- **Equivalência Algorítmica**: Prova formal de equivalência matemática
- **Ambiente Controlado**: Docker com configurações padronizadas
- **Dados Reais**: Test cases oficiais do CSES (não sintéticos)
- **Repetições**: Múltiplas execuções para validação estatística

### Critérios de Sucesso
1. **Calibração Confiável**: IQR < 15% (C++), < 20% (Python)
2. **Fator Razoável**: 1.5x ≤ ajuste ≤ 50x
3. **Injustiça Demonstrada**: Gap significativo entre linguagens
4. **Injustiça Corrigida**: Python recovery > 30%
5. **C++ Preservado**: Manutenção de 100% success rate
6. **Seletividade Mantida**: Slow solutions → TLE em ambos sistemas

## Implementação Técnica

### Arquitetura do Sistema
```
run_complete_experiment.py
├── run_benchmark.py       # Execução automatizada
├── analyze_results.py     # Análise estatística
├── validate_slow_solutions.py  # Validação de seletividade
└── Docker Environment     # Isolamento controlado
```

### Comandos Docker Utilizados
```bash
# C++ Environment
docker run --rm gcc:latest g++ -O3 -o solution solution.cpp

# Python Environment  
docker run --rm python:3.11-slim python3 solution.py
```

### Ferramentas de Medição
- **Timing**: Wall clock time via Python `time.time()`
- **Timeout**: Linux `timeout` command
- **Status**: Process exit codes + output analysis

## Arquivos de Configuração

### Estrutura de Dados
```
experiments_realworld/graphs/problem01/
├── solutions/              # Soluções otimizadas
├── slow_validation/        # Soluções deliberadamente lentas
├── tests_cses/            # 16 test cases oficiais
├── results/               # Dados coletados
└── scripts/               # Automação experimental
```

### Metadados do Experimento
- **Timestamp**: 2025-08-30T15:01:42
- **Protocol**: experiment_plan.md
- **Analyzer Version**: 1.0
- **Total Duration**: ~30 minutos
