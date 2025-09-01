# Experimentos de Programação Dinâmica

## Estrutura dos Experimentos

### Problem01: CSES 1635 - Coin Combinations I
- **Problema**: Contar maneiras distintas de formar soma x (ordem importa, repetição permitida)
- **Link**: https://cses.fi/problemset/task/1635
- **Algoritmo**: Programação Dinâmica para contagem de combinações
- **Categoria**: DP Iterativo vs DP Recursivo
- **Mudança**: Migrou de 1636→1635 (recursão mais viável, benchmark mais preciso)
- **Hipótese**: DP Recursivo sofre maior injustiça devido ao overhead de stack

### Metodologia

**Comparação Binária**:
- **Iterativo**: Solução bottom-up com tabela DP
- **Recursivo**: Solução top-down com memoização

**Descoberta Esperada**:
- Algoritmos recursivos tendem a mostrar maior disparidade Python vs C++
- DP iterativo: injustiça moderada
- DP recursivo: injustiça severa

### Estrutura de Diretórios

```
dp/
├── README.md
├── problem01_iterativo/
│   ├── solutions/
│   │   ├── solution.cpp
│   │   └── solution.py
│   ├── slow_validation/
│   │   └── solutions_slow/
│   ├── tests/
│   ├── run_benchmark.py
│   ├── analyze_results.py
│   ├── validate_slow_solutions.py
│   ├── PROVA_FORMAL.md
│   └── resultados_finais/
└── problem01_recursivo/
    ├── solutions/
    │   ├── solution.cpp
    │   └── solution.py
    ├── slow_validation/
    │   └── solutions_slow/
    ├── tests/
    ├── run_benchmark.py
    ├── analyze_results.py
    ├── validate_slow_solutions.py
    ├── PROVA_FORMAL.md
    └── resultados_finais/
```

### Status

- [ ] Problem01 Iterativo: Estrutura criada
- [ ] Problem01 Recursivo: Estrutura criada
- [ ] Implementação das soluções
- [ ] Execução dos benchmarks
- [ ] Análise comparativa iterativo vs recursivo
