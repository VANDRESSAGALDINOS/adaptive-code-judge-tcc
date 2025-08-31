# FRAMEWORK: BINARY VERDICT ANALYSIS

## Visão Geral

Framework reutilizável para implementação da metodologia de Análise Binária de Veredicto em qualquer experimento de detecção de injustiças linguísticas.

## Componentes do Framework

### 1. Classe Base: BinaryVerdictAnalyzer

```python
class BinaryVerdictAnalyzer:
    """Framework base para análise binária de veredictos"""
    
    def __init__(self, platform_name, time_limit, critical_cases):
        self.platform_name = platform_name
        self.time_limit = time_limit
        self.critical_cases = critical_cases
        self.control_cases = []
        
    def load_validation_results(self, results_file):
        """Carrega resultados de validação"""
        pass
        
    def analyze_binary_verdict(self, results):
        """Aplica metodologia binária"""
        pass
        
    def generate_report(self, analysis):
        """Gera relatório científico"""
        pass
```

### 2. Módulo de Execução: BenchmarkExecutor

```python
class BenchmarkExecutor:
    """Executor padronizado de benchmarks"""
    
    def __init__(self, docker_config, solutions_dir, tests_dir):
        self.docker_config = docker_config
        self.solutions_dir = solutions_dir
        self.tests_dir = tests_dir
        
    def run_calibration(self, case_id, repetitions, time_limit):
        """Fase de calibração"""
        pass
        
    def run_validation(self, cases, repetitions, adjustment_factor, time_limit):
        """Fase de validação binária"""
        pass
        
    def validate_selectivity(self, slow_solutions, cases, adjustment_factor):
        """Validação de seletividade"""
        pass
```

### 3. Utilitários: VerdictUtils

```python
class VerdictUtils:
    """Utilitários para análise de veredictos"""
    
    @staticmethod
    def is_tle_status(status):
        """Verifica se status indica TLE"""
        return status in ["TLE", "TIME_LIMIT_EXCEEDED"]
        
    @staticmethod
    def calculate_final_verdict(detailed_results):
        """Calcula veredicto final baseado em resultados detalhados"""
        for result in detailed_results:
            if VerdictUtils.is_tle_status(result["status"]):
                return "REJECTED"
        return "ACCEPTED"
        
    @staticmethod
    def detect_injustice(traditional_results, adaptive_results):
        """Detecta injustiça linguística"""
        trad_cpp = traditional_results["cpp"]["final_verdict"]
        trad_python = traditional_results["python"]["final_verdict"]
        adapt_cpp = adaptive_results["cpp"]["final_verdict"]
        adapt_python = adaptive_results["python"]["final_verdict"]
        
        injustice_detected = (trad_cpp == "ACCEPTED" and trad_python == "REJECTED")
        injustice_corrected = (adapt_cpp == "ACCEPTED" and adapt_python == "ACCEPTED")
        
        return {
            "injustice_detected": injustice_detected,
            "injustice_corrected": injustice_corrected,
            "python_rescued": trad_python == "REJECTED" and adapt_python == "ACCEPTED"
        }
```

## Templates de Implementação

### 1. Script de Análise Binária

```python
#!/usr/bin/env python3
"""
Template: Análise Binária de Veredicto
Adapte para seu experimento específico
"""

import json
from pathlib import Path
from binary_verdict_framework import BinaryVerdictAnalyzer

def main():
    # Configuração específica do experimento
    analyzer = BinaryVerdictAnalyzer(
        platform_name="CSES",  # Adapte para sua plataforma
        time_limit=1.0,        # Limite real da plataforma
        critical_cases=[6, 7, 8, 9, 10]  # Casos que dão TLE
    )
    
    # Carregar resultados
    results = analyzer.load_validation_results("results/validation_results.json")
    
    # Aplicar análise binária
    analysis = analyzer.analyze_binary_verdict(results)
    
    # Gerar relatório
    report = analyzer.generate_report(analysis)
    
    # Salvar resultados
    with open("binary_verdict_analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)
    
    with open("BINARY_VERDICT_REPORT.md", "w") as f:
        f.write(report)
    
    print("✅ Análise binária concluída!")

if __name__ == "__main__":
    main()
```

### 2. Configuração Docker Padrão

```python
DOCKER_CONFIG = {
    "cpp": {
        "image": "gcc:latest",
        "compile_cmd": "g++ -O2 -std=c++17 solution.cpp -o solution",
        "run_cmd": "timeout {time_limit}s ./solution"
    },
    "python": {
        "image": "python:3.11-slim", 
        "compile_cmd": None,
        "run_cmd": "timeout {time_limit}s python3 solution.py"
    }
}
```

### 3. Estrutura de Metadados

```json
{
  "experiment": {
    "problema": "problemXX",
    "plataforma": "CSES",
    "data": "2025-08-30",
    "status": "completo"
  },
  "metodologia_binaria": {
    "tradicional_cpp": "ACCEPTED|REJECTED",
    "tradicional_python": "ACCEPTED|REJECTED",
    "adaptativo_cpp": "ACCEPTED|REJECTED", 
    "adaptativo_python": "ACCEPTED|REJECTED",
    "injustica_detectada": true,
    "injustica_corrigida": true,
    "python_resgatado": true
  },
  "parametros": {
    "limite_tempo": 1.0,
    "casos_criticos": [6, 7, 8, 9, 10],
    "fator_ajuste": 4.33,
    "repeticoes": 10
  }
}
```

## Checklist de Implementação

### Preparação
- [ ] Identificar casos críticos via dados externos
- [ ] Configurar Docker com imagens apropriadas
- [ ] Preparar soluções algoritmicamente equivalentes
- [ ] Criar slow solutions para validação

### Execução
- [ ] Executar calibração para determinar fator
- [ ] Executar validação com análise binária
- [ ] Validar seletividade com slow solutions
- [ ] Comparar com dados externos da plataforma

### Análise
- [ ] Aplicar metodologia binária aos resultados
- [ ] Verificar critérios de injustiça
- [ ] Gerar relatório científico
- [ ] Documentar descobertas específicas

### Validação
- [ ] Confirmar correlação com dados externos
- [ ] Verificar confiabilidade estatística
- [ ] Validar preservação de seletividade
- [ ] Documentar limitações e insights

## Adaptações por Plataforma

### CSES
```python
CSES_CONFIG = {
    "time_limit": 1.0,  # Padrão CSES
    "memory_limit": "512MB",
    "languages": ["C++17", "Python3"],
    "verdict_format": ["ACCEPTED", "TLE", "WA", "RE"]
}
```

### AtCoder
```python
ATCODER_CONFIG = {
    "time_limit": 2.0,  # Padrão AtCoder
    "memory_limit": "1024MB", 
    "languages": ["C++17", "Python3"],
    "verdict_format": ["AC", "TLE", "WA", "RE"]
}
```

### LeetCode
```python
LEETCODE_CONFIG = {
    "time_limit": "variable",  # Depende do problema
    "memory_limit": "variable",
    "languages": ["C++", "Python3"],
    "verdict_format": ["Accepted", "Time Limit Exceeded", "Wrong Answer"]
}
```

## Extensões Futuras

### Análise Multi-dimensional
```python
class MultiDimensionalAnalyzer(BinaryVerdictAnalyzer):
    """Extensão para análise além de TLE"""
    
    def analyze_all_verdicts(self, results):
        """Analisa TLE, WA, RE, etc."""
        pass
        
    def calculate_fairness_index(self, results):
        """Calcula índice quantitativo de fairness"""
        pass
```

### Automação Completa
```python
class AutomatedPipeline:
    """Pipeline completamente automatizado"""
    
    def collect_external_data(self, platform, problem_id):
        """Coleta dados externos automaticamente"""
        pass
        
    def run_complete_experiment(self, config):
        """Executa experimento completo"""
        pass
        
    def generate_final_report(self, results):
        """Gera relatório final automaticamente"""
        pass
```

## Instalação e Uso

### Dependências
```bash
pip install docker pandas numpy matplotlib seaborn
```

### Uso Básico
```python
from binary_verdict_framework import BinaryVerdictAnalyzer

# Configurar experimento
analyzer = BinaryVerdictAnalyzer("CSES", 1.0, [6, 7, 8, 9, 10])

# Executar análise
results = analyzer.load_validation_results("results.json")
analysis = analyzer.analyze_binary_verdict(results)
report = analyzer.generate_report(analysis)

# Salvar resultados
analyzer.save_results(analysis, report)
```

## Contribuições

### Como Contribuir
1. **Fork** o repositório
2. **Implemente** extensões ou melhorias
3. **Teste** com dados reais
4. **Documente** mudanças
5. **Submeta** pull request

### Áreas de Contribuição
- **Suporte a novas plataformas**
- **Métricas de fairness avançadas**
- **Automação de coleta de dados**
- **Interface web para auditoria**
- **Otimizações de performance**

---
**Framework**: Binary Verdict Analysis v1.0  
**Linguagem**: Python 3.11+  
**Licença**: Acadêmica/Educacional  
**Status**: Pronto para uso e extensão
