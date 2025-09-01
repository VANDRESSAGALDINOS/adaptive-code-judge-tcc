# Apple Division - CSES 1623

## Problema: Apple Division - Backtracking

### Status Checklist:
- [x] Estrutura criada
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

---

## Descrição do Problema

**CSES 1623 - Apple Division**

### Enunciado
You have n apples with known weights. Your task is to divide the apples into two groups so that the difference between the weights of the groups is minimal.

### Input
- First line: integer n (number of apples)
- Second line: n integers p1, p2, ..., pn (weights of apples)

### Output
- One integer: the minimum possible difference between the groups

### Constraints
- 1 ≤ n ≤ 20
- 1 ≤ pi ≤ 10^9

### Exemplo
```
Input:
5
3 2 7 4 1

Output:
1
```

**Explicação**: Podemos dividir as maçãs em grupos {3,2,7} (peso=12) e {4,1} (peso=5). A diferença é |12-5| = 7. Mas a divisão ótima é {3,2,4} (peso=9) e {7,1} (peso=8), com diferença |9-8| = 1.

---

## Análise Algorítmica

### Abordagem: Backtracking com Subset Sum
1. **Objetivo**: Encontrar subset que minimize |sum(subset) - sum(complement)|
2. **Estratégia**: Explorar todas as 2^n possibilidades de divisão
3. **Otimização**: Podar quando subset_sum > total_sum/2
4. **Complexidade**: O(2^n) no pior caso

### Características para Injustiça Algorítmica
- **Recursão profunda**: Até 20 níveis
- **Exploração exponencial**: 2^20 = ~1M estados
- **Backtracking intensivo**: Muitas chamadas recursivas
- **Alto potencial TLE**: Python vs C++ em casos grandes

### Casos de Teste Estratégicos
- **SMALL**: n=5, pesos pequenos
- **MEDIUM**: n=10, pesos médios  
- **LARGE**: n=15, pesos grandes
- **CRITICAL**: n=18-20, casos próximos ao limite

---

## Implementação Planejada

### Solução Otimizada
```cpp
// C++ - Backtracking com poda
void backtrack(int idx, long long sum1, long long sum2) {
    if (idx == n) {
        ans = min(ans, abs(sum1 - sum2));
        return;
    }
    
    // Poda: se sum1 já é maior que metade, não vale a pena continuar neste ramo
    if (sum1 <= total_sum / 2) {
        backtrack(idx + 1, sum1 + weights[idx], sum2);
    }
    backtrack(idx + 1, sum1, sum2 + weights[idx]);
}
```

### Solução Slow (EXTRA_WORK)
- Adicionar overhead intencional em cada chamada recursiva
- EXTRA_WORK = 2000 operações por chamada
- Testar sensibilidade C++ vs Python

---

## Expectativas Científicas

### Hipótese Principal
**Apple Division demonstrará injustiça algorítmica moderada a severa**, com Python falhando em casos n≥18 onde C++ ainda consegue passar.

### Métricas Esperadas
- **TLE Rate Python**: 40-70% em casos críticos
- **TLE Rate C++**: 0-20% nos mesmos casos
- **Performance Gap**: 5-15x diferença de tempo
- **Recursion Sensitivity**: Python mais sensível a profundidade

### Descoberta Esperada
**"Backtracking Recursion Injustice"** - Python falha sistematicamente em problemas de backtracking com recursão profunda (n≥18), mesmo com algoritmos matematicamente equivalentes.
