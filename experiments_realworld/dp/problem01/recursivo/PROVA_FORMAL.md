# Prova de Equivalência Matemática - DP Recursivo

## CSES 1635 - Coin Combinations I

### Enunciado do Problema

**Link**: https://cses.fi/problemset/task/1635

**Descrição**: Calcular o número de maneiras distintas de formar uma soma `x` usando moedas disponíveis (ordem importa, repetição permitida).

**Exemplo**: 
- Moedas: {2, 3, 5}, Soma: 9
- Maneiras: 2+2+5, 2+5+2, 5+2+2, 3+3+3, 2+2+2+3, 2+2+3+2, 2+3+2+2, 3+2+2+2 = **8 maneiras**

**Constraints**:
- 1 ≤ n ≤ 100
- 1 ≤ x ≤ 10^6  
- 1 ≤ c_i ≤ 10^6

### Algoritmo Implementado
**Programação Dinâmica Recursiva (Top-down) com Memoização**

### Prova de Equivalência

**Estado**: `solve(remaining)` = número de maneiras de formar valor `remaining`

**Recorrência**:
```
solve(remaining) = Σ solve(remaining - coins[i]) para todo i onde remaining >= coins[i]
```

**Casos Base**:
- `remaining == 0`: retorna 1 (uma maneira válida)
- `remaining < 0`: retorna 0 (impossível)

**Memoização**: `memo[remaining]` armazena resultados calculados

### Implementações

#### C++ (solution.cpp)
```cpp
int solve(int remaining) {
    if (remaining == 0) return 1;
    if (remaining < 0) return 0;
    if (memo[remaining] != -1) return memo[remaining];
    
    int result = 0;
    for (int i = 0; i < n; i++) {
        if (remaining >= coins[i]) {
            result = (result + solve(remaining - coins[i])) % MOD;
        }
    }
    
    return memo[remaining] = result;
}
```

#### Python (solution.py)  
```python
def solve(remaining, coins, memo):
    if remaining == 0: return 1
    if remaining < 0: return 0
    if memo[remaining] != -1: return memo[remaining]
    
    result = 0
    for coin in coins:
        if remaining >= coin:
            result = (result + solve(remaining - coin, coins, memo)) % MOD
    
    memo[remaining] = result
    return result
```

### Demonstração de Equivalência

**Ambas as implementações**:
1. **Mesma recorrência matemática**: `f(r) = Σ f(r-c[i])` para todo i
2. **Mesmos casos base**: `remaining==0` → 1, `remaining<0` → 0
3. **Mesma estratégia de memoização**: array 1D `memo[remaining]`
4. **Mesma ordem de processamento**: top-down com memoização
5. **Mesmo módulo**: MOD = 10^9 + 7

**Invariante Matemática**: Para qualquer valor `remaining`, ambas as funções retornam o mesmo valor.

**Complexidade**:
- **Tempo**: O(n × x) - cada estado `remaining` calculado uma vez
- **Espaço**: O(x) - array de memoização + O(x) stack
- **Stack Depth**: O(x) no pior caso

### Validação Externa

#### Resultados CSES - C++ Recursivo
**Status**: ✅ **ACCEPTED**  
**Submissão**: 2025-08-31 20:55:58 +0300  
**Link**: https://cses.fi/paste/afbf3069975b5278db48fc/

**Performance por Teste**:
| Test | Verdict | Time | Análise |
|------|---------|------|---------|
| #1 | ACCEPTED | 0.01s | Caso pequeno |
| #2 | ACCEPTED | 0.05s | Médio |
| #3 | ACCEPTED | 0.01s | Pequeno |
| #4 | **ACCEPTED** | **0.47s** | **Caso crítico** |
| #5 | ACCEPTED | 0.18s | Médio |
| #6-7 | ACCEPTED | 0.01s | Pequenos |
| #8 | **ACCEPTED** | **0.47s** | **Caso crítico** |
| #9-10 | ACCEPTED | 0.01s | Pequenos |
| #11 | **ACCEPTED** | **0.47s** | **Caso crítico** |
| #12-13 | ACCEPTED | 0.01s | Pequenos |

**Observações**:
- **Casos críticos**: Tests #4, #8, #11 com 0.47s (próximo ao limite 1.0s)
- **C++ viável**: Recursão funciona, mas margem estreita
- **Python risco**: Esperado TLE nos casos críticos

#### Python Recursivo

**Primeira submissão** (RecursionError): 
- **Problema**: `sys.setrecursionlimit(10000)` insuficiente para x=10^6
- **Erro**: Stack overflow em casos grandes
- **Tests falharam**: #2, #4, #5, #8, #11, #13

**Tentativa de correção**:
- **Ajuste**: `sys.setrecursionlimit(1100000)` para suportar profundidade máxima
- **Resultado**: RecursionError persiste em casos patológicos (x=10^6, n=1)
- **Conclusão**: Limitação arquitetural fundamental documentada

**Descoberta científica**: Ver `/documentation/insights/LIMITACOES_ARQUITETURAIS_RECURSAO.md`

**Status final**:
- **Injustiça temporal**: TLE em casos críticos (#4, #5, #8, #11)
- **Injustiça arquitetural**: RecursionError em casos extremos (#2)
- **Categoria descoberta**: Tipo B - Injustiça Arquitetural

### Hipótese de Injustiça
**Python vs C++**: Recursão + memoização tende a amplificar diferenças de performance:
- **Overhead de stack**: Python tem custo maior por chamada (comprovado em 1636)
- **Acesso à memoização**: Arrays têm performance diferente entre linguagens
- **Gerenciamento de memória**: GC vs controle manual
- **Casos críticos**: Tests #4, #8, #11 são candidatos a TLE em Python

### Status da Prova
- [x] **Equivalência matemática**: ✓ Demonstrada
- [x] **Implementação C++**: ✓ Completa e validada
- [x] **Implementação Python**: ✓ Completa  
- [x] **Validação CSES C++**: ✅ ACCEPTED (margem estreita)
- [ ] **Validação CSES Python**: Aguardando resultado
- [ ] **Benchmark experimental**: Pendente
