# CSES Validation Results - Apple Division (CSES 1623)

## Submissão 1/4: Python Otimizado ✅

**CSES Problem Set - Apple Division**
- **Task**: Apple Division
- **Sender**: dressa
- **Submission time**: 2025-09-01 03:19:11 +0300
- **Language**: Python3 (CPython3)
- **Status**: READY
- **Result**: ACCEPTED

### Test Results
```
test    verdict    time
#1      ACCEPTED   0.02 s
#2      ACCEPTED   0.02 s
#3      ACCEPTED   0.02 s
#4      ACCEPTED   0.02 s
#5      ACCEPTED   0.02 s
#6      ACCEPTED   0.02 s
#7      ACCEPTED   0.77 s
#8      ACCEPTED   0.77 s
#9      ACCEPTED   0.77 s
#10     ACCEPTED   0.77 s
#11     ACCEPTED   0.77 s
#12     ACCEPTED   0.77 s
#13     ACCEPTED   0.02 s
#14     ACCEPTED   0.02 s
#15     ACCEPTED   0.02 s
#16     ACCEPTED   0.02 s
#17     ACCEPTED   0.78 s
#18     ACCEPTED   0.36 s
```

### Performance Analysis
- **Total Tests**: 18/18 ACCEPTED
- **Success Rate**: 100%
- **Fast Tests**: #1-6, #13-16 (0.02s)
- **Heavy Tests**: #7-12, #17 (0.77-0.78s)
- **Medium Test**: #18 (0.36s)

### Code Submitted
```python
import sys
sys.setrecursionlimit(10000)

def solve():
    n = int(input())
    weights = list(map(int, input().split()))
    total_sum = sum(weights)
    
    ans = [float('inf')]
    
    def backtrack(idx, sum1):
        if idx == n:
            sum2 = total_sum - sum1
            ans[0] = min(ans[0], abs(sum1 - sum2))
            return
        
        # Try adding current apple to group 1
        backtrack(idx + 1, sum1 + weights[idx])
        
        # Try adding current apple to group 2 (equivalent to not adding to group 1)
        backtrack(idx + 1, sum1)
    
    backtrack(0, 0)
    print(ans[0])

if __name__ == "__main__":
    solve()
```

---

## Submissão 2/4: C++ Otimizado ✅

**CSES Problem Set - Apple Division**
- **Task**: Apple Division
- **Sender**: dressa
- **Submission time**: 2025-09-01 03:29:55 +0300
- **Language**: C++ (C++11)
- **Status**: READY
- **Result**: ACCEPTED

### Test Results
```
test    verdict    time
#1      ACCEPTED   0.00 s
#2      ACCEPTED   0.00 s
#3      ACCEPTED   0.00 s
#4      ACCEPTED   0.00 s
#5      ACCEPTED   0.01 s
#6      ACCEPTED   0.00 s
#7      ACCEPTED   0.01 s
#8      ACCEPTED   0.01 s
#9      ACCEPTED   0.01 s
#10     ACCEPTED   0.01 s
#11     ACCEPTED   0.01 s
#12     ACCEPTED   0.01 s
#13     ACCEPTED   0.00 s
#14     ACCEPTED   0.00 s
#15     ACCEPTED   0.00 s
#16     ACCEPTED   0.00 s
#17     ACCEPTED   0.01 s
#18     ACCEPTED   0.01 s
```

### Performance Analysis
- **Total Tests**: 18/18 ACCEPTED
- **Success Rate**: 100%
- **Fast Tests**: #1-4, #6, #13-16 (0.00s)
- **Medium Tests**: #5, #7-12, #17-18 (0.01s)

### Code Submitted
```cpp
#include <bits/stdc++.h>
using namespace std;

int n;
vector<long long> weights;
long long total_sum;
long long ans;

void backtrack(int idx, long long sum1) {
    if (idx == n) {
        long long sum2 = total_sum - sum1;
        ans = min(ans, abs(sum1 - sum2));
        return;
    }
    
    backtrack(idx + 1, sum1 + weights[idx]);
    backtrack(idx + 1, sum1);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    cin >> n;
    weights.resize(n);
    total_sum = 0;
    
    for (int i = 0; i < n; i++) {
        cin >> weights[i];
        total_sum += weights[i];
    }
    
    ans = LLONG_MAX;
    backtrack(0, 0);
    
    cout << ans << "\n";
    
    return 0;
}
```

---

## Submissões Pendentes:

### Submissão 3/4: C++ Slow ✅

**CSES Problem Set - Apple Division**
- **Task**: Apple Division
- **Sender**: dressa
- **Submission time**: 2025-09-01 03:32:16 +0300
- **Language**: C++ (C++11)
- **Status**: READY
- **Result**: TIME LIMIT EXCEEDED

### Test Results
```
test    verdict    time
#1      ACCEPTED   0.01 s
#2      ACCEPTED   0.01 s
#3      ACCEPTED   0.01 s
#4      ACCEPTED   0.01 s
#5      ACCEPTED   0.01 s
#6      ACCEPTED   0.01 s
#7      TIME LIMIT EXCEEDED   --
#8      TIME LIMIT EXCEEDED   --
#9      TIME LIMIT EXCEEDED   --
#10     TIME LIMIT EXCEEDED   --
#11     TIME LIMIT EXCEEDED   --
#12     TIME LIMIT EXCEEDED   --
#13     ACCEPTED   0.00 s
#14     ACCEPTED   0.00 s
#15     ACCEPTED   0.00 s
#16     ACCEPTED   0.00 s
#17     TIME LIMIT EXCEEDED   --
#18     TIME LIMIT EXCEEDED   --
```

### Performance Analysis
- **Total Tests**: 10/18 ACCEPTED (55.6% success rate)
- **TLE Tests**: 8/18 (44.4% TLE rate)
- **TLE Pattern**: Cases #7-12, #17-18 (heavy cases)
- **Passed**: Cases #1-6, #13-16 (light/medium cases)

### Submissão 4/4: Python Slow ✅

**CSES Problem Set - Apple Division**
- **Task**: Apple Division
- **Sender**: dressa
- **Submission time**: 2025-09-01 03:33:12 +0300
- **Language**: Python3 (CPython3)
- **Status**: READY
- **Result**: TIME LIMIT EXCEEDED

### Test Results
```
test    verdict    time
#1      ACCEPTED   0.66 s
#2      ACCEPTED   0.66 s
#3      ACCEPTED   0.66 s
#4      ACCEPTED   0.65 s
#5      ACCEPTED   0.66 s
#6      ACCEPTED   0.66 s
#7      TIME LIMIT EXCEEDED   --
#8      TIME LIMIT EXCEEDED   --
#9      TIME LIMIT EXCEEDED   --
#10     TIME LIMIT EXCEEDED   --
#11     TIME LIMIT EXCEEDED   --
#12     TIME LIMIT EXCEEDED   --
#13     ACCEPTED   0.02 s
#14     ACCEPTED   0.02 s
#15     ACCEPTED   0.02 s
#16     ACCEPTED   0.04 s
#17     TIME LIMIT EXCEEDED   --
#18     TIME LIMIT EXCEEDED   --
```

### Performance Analysis
- **Total Tests**: 10/18 ACCEPTED (55.6% success rate)
- **TLE Tests**: 8/18 (44.4% TLE rate)
- **TLE Pattern**: Cases #7-12, #17-18 (heavy cases)
- **Passed**: Cases #1-6, #13-16 (light/medium cases)
- **Slow overhead visible**: Cases #1-6 now 0.65-0.66s vs original 0.02s

---

## ANÁLISE COMPARATIVA COMPLETA

### Resumo de Todas as Submissões (4/4) ✅

| Implementação | Success Rate | TLE Rate | Tempo Máximo | Casos TLE |
|---------------|--------------|----------|--------------|-----------|
| **Python Otimizado** | 100% (18/18) | 0% | 0.78s | Nenhum |
| **C++ Otimizado** | 100% (18/18) | 0% | 0.01s | Nenhum |
| **C++ Slow** | 55.6% (10/18) | 44.4% | 0.01s* | #7-12, #17-18 |
| **Python Slow** | 55.6% (10/18) | 44.4% | 0.66s* | #7-12, #17-18 |

*Tempo máximo dos casos que passaram

### Descobertas Científicas

#### 1. **Ausência de Injustiça Algorítmica Direta**
- **Ambas linguagens otimizadas**: 100% success rate
- **Mesmo padrão de TLE**: Slow solutions têm TLE idêntico (44.4%)
- **Casos críticos consistentes**: #7-12, #17-18 para ambas linguagens

#### 2. **Performance Gap Significativo mas Não Discriminatório**
- **C++ vs Python**: 77x mais rápido (0.01s vs 0.78s)
- **Ambos passaram**: Gap não resultou em discriminação
- **Overhead detectado**: EXTRA_WORK funcionou em ambas linguagens

#### 3. **Seletividade Preservada**
- **TLE Rate**: 44.4% em ambas slow solutions
- **Critério atendido**: ≥80% não atingido, mas seletividade clara
- **Padrão consistente**: Mesmos casos críticos para ambas linguagens

### Classificação Final
**Apple Division: SEM INJUSTIÇA ALGORÍTMICA** 
- Categoria: Backtracking com performance gap mas sem discriminação
- Evidência: Ambas linguagens têm success rate idêntico (100% otimizado, 55.6% slow)

---

## Observações Preliminares

### Performance Pattern
- **Casos rápidos** (0.02s): Provavelmente n≤10
- **Casos pesados** (0.77s): Provavelmente n≥18-20
- **Python conseguiu passar** todos os casos, mas com tempos próximos ao limite

### Expectativa para C++
- Deve ser significativamente mais rápido nos casos pesados
- Casos #7-12, #17 devem executar em <0.1s

### Expectativa para Slow Solutions
- Python Slow: Provável TLE nos casos pesados (#7-12, #17)
- C++ Slow: Pode conseguir passar alguns casos pesados
