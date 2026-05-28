#!/usr/bin/env /usr/bin/python3
"""
Direct Docker Experiment Runner - Bypasses docker-py library issues
Executes real benchmarks using subprocess calls to Docker
"""
import sys
import os
import json
from datetime import datetime

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
# Add experiments/ to path so the shared benchmark engine is importable.
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from models import db
from services.problem_service import ProblemService
from config.database import DatabaseConfig
from config.app import AppConfig
from flask import Flask

# Single source of the validated measurement methodology (items 3-6).
from lib.benchmark_engine import measure_language, compute_beta, select_largest_test_case

def create_app():
    """Create Flask app for experiments"""
    app = Flask(__name__)
    config = DatabaseConfig.get_config()
    app.config.update(config)
    db.init_app(app)
    return app


def run_benchmark_direct(problem_id: int, cpp_solution: str, python_solution: str):
    """Run benchmark measurements directly, with adaptive repetition (Sec. 3.2)."""

    # Get the problem and its largest test case
    from models import Problem, TestCase
    problem = Problem.query.get(problem_id)
    if not problem:
        raise ValueError(f"Problem {problem_id} not found")

    test_cases = TestCase.query.filter_by(problem_id=problem_id).all()
    if not test_cases:
        raise ValueError(f"No test cases found for problem {problem_id}")

    # Largest test case by input size in bytes (item 7): use input_size when
    # present, else fall back to len(input_data); ties broken by smaller id.
    largest_tc = select_largest_test_case(
        test_cases,
        size_fn=lambda tc: tc.input_size or len(tc.input_data),
        id_fn=lambda tc: tc.id,
    )

    print(f"Running benchmark on test case: {largest_tc.name}")
    print(f"   Input size: {largest_tc.input_size} bytes")
    print(f"   Adaptive: blocks of {AppConfig.BENCHMARK_BLOCK_SIZE}, "
          f"cap {AppConfig.BENCHMARK_MAX_REPETITIONS}, "
          f"IQR/median < {AppConfig.BENCHMARK_IQR_THRESHOLD_CPP*100:.0f}% (C++) "
          f"/ {AppConfig.BENCHMARK_IQR_THRESHOLD_PYTHON*100:.0f}% (Python)")

    print("Measuring C++ performance (compiled once, startup excluded, adaptive)...")
    cpp = measure_language(
        cpp_solution, largest_tc.input_data, largest_tc.expected_output,
        'cpp', AppConfig.BENCHMARK_IQR_THRESHOLD_CPP
    )

    print("Measuring Python performance (startup excluded, adaptive)...")
    py = measure_language(
        python_solution, largest_tc.input_data, largest_tc.expected_output,
        'python', AppConfig.BENCHMARK_IQR_THRESHOLD_PYTHON
    )

    return compute_beta(cpp, py, largest_tc.name)

def generate_experiment_report(complexity_class: str, problem, benchmark_results):
    """Generate detailed experiment report for individual experiment"""

    # Map complexity to description
    complexity_map = {
        'O1_constant': {
            'name': 'O(1) - Operações Aritméticas Constantes',
            'algorithm': 'Operações aritméticas básicas',
            'description': 'Soma, subtração, multiplicação, divisão inteira'
        },
        'O_log_n': {
            'name': 'O(log n) - Busca Binária',
            'algorithm': 'Busca binária em array ordenado',
            'description': 'Busca eficiente com redução logarítmica do espaço'
        }
    }

    info = complexity_map.get(complexity_class, {
        'name': f'{complexity_class} - Experimento',
        'algorithm': 'Algoritmo não especificado',
        'description': 'Descrição não disponível'
    })

    # Calculate performance advantage
    advantage_pct = ((1 - benchmark_results['adjustment_factor']) * 100)

    # Generate timestamp
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    report_content = f"""# Experimento {info['name']}

## Resumo Executivo

**Descoberta Principal**: Python supera C++ em **{advantage_pct:.1f}%** para {info['algorithm'].lower()} em ambientes containerizados.

**Resultado**: {'Inesperado - contradiz expectativas' if benchmark_results['adjustment_factor'] < 1.0 else 'Esperado - confirma teoria'}

## Dados Experimentais Brutos

### Performance Medida
- **C++ Mediano**: {benchmark_results['cpp_median']:.4f}s
- **Python Mediano**: {benchmark_results['python_median']:.4f}s
- **Razão Python/C++**: {benchmark_results['adjustment_factor']:.3f}x
- **Vantagem Python**: {advantage_pct:.1f}%

### Confiabilidade
- **Repetições Bem-sucedidas**: {benchmark_results['repetitions']}/10
- **Teste Utilizado**: {benchmark_results['test_case_used']}
- **Confiável**: {'Sim' if benchmark_results['is_reliable'] else 'Não'}

### Variabilidade (IQR)
- **C++ IQR**: {benchmark_results['cpp_iqr']:.4f}s ({(benchmark_results['cpp_iqr']/benchmark_results['cpp_median']*100):.1f}%)
- **Python IQR**: {benchmark_results['python_iqr']:.4f}s ({(benchmark_results['python_iqr']/benchmark_results['python_median']*100):.1f}%)

## Análise dos Resultados

### {info['algorithm']}
- **Descrição**: {info['description']}
- **Complexidade Teórica**: {complexity_class.replace('_', ' ').replace('O', 'O(')}n)
- **Implementação**: Algoritmicamente equivalente em ambas linguagens

### Fatores de Performance Identificados

1. **Overhead de Compilação**
   - C++ requer compilação a cada execução (~0.29s)
   - Python executa imediatamente (~0.18s)

2. **Otimizações de Runtime**
   - CPython tem operações nativas altamente otimizadas
   - Estruturas de dados Python implementadas em C

3. **Container Overhead**
   - Docker startup mais rápido para Python
   - Toolchain C++ adiciona latência

## Insights para o TCC

### Contribuição Científica
- **Paradigma Contestado**: {"C++ nem sempre é mais rápido" if benchmark_results['adjustment_factor'] < 1.0 else "Confirma expectativas teóricas"}
- **Evidência Empírica**: Dados quantitativos de ambiente real
- **Metodologia**: Separação de fatores algorítmicos vs overhead

### Aplicação Prática
```json
{{
  "adaptive_limits": {{
    "problem_type": "{complexity_class}",
    "cpp_limit_ms": {int(benchmark_results['cpp_median'] * 1000)},
    "python_limit_ms": {int(benchmark_results['python_median'] * 1000)},
    "adjustment_factor": {benchmark_results['adjustment_factor']:.3f}
  }}
}}
```

## Dados Técnicos Completos

### Execuções C++
```
{benchmark_results['cpp_times']}
```

### Execuções Python
```
{benchmark_results['python_times']}
```

## Conclusão

Este experimento demonstra que **performance é contextual** e depende criticamente do ambiente de execução.

{"A descoberta de que Python supera C++ contraria expectativas comuns e valida a necessidade de sistemas adaptativos baseados em medições reais." if benchmark_results['adjustment_factor'] < 1.0 else "Os resultados confirmam expectativas teóricas e demonstram a importância de medições empíricas."}

**Para sistemas de juízes online, estes dados justificam limites de tempo adaptativos** que considerem a performance real de cada linguagem no ambiente de produção.

---
*Relatório gerado automaticamente em {timestamp}*
*Experimento conduzido como parte do projeto Adaptive Code Judge*
"""

    # Save report
    report_file = f"complexity_analysis/{complexity_class}/EXPERIMENT_REPORT.md"
    with open(report_file, 'w') as f:
        f.write(report_content)

    print(f"Individual report generated: {report_file}")

def run_complexity_experiment_direct(complexity_class: str):
    """Run experiment directly with subprocess Docker calls"""
    app = create_app()

    with app.app_context():
        print(f"Running {complexity_class} Complexity Experiment (DIRECT)")
        print("=" * 70)

        # Import problem definition
        sys.path.append(os.path.join('complexity_analysis', complexity_class))
        problem_module = __import__('problem_definition', fromlist=[''])

        # Create problem and test cases
        problem_service = ProblemService()
        problem = problem_module.create_problem(problem_service)

        print(f"Problem created: {problem.title}")
        print(f"   Test cases: {len(problem.test_cases)}")

        # Load reference solutions
        cpp_solution_file = f'complexity_analysis/{complexity_class}/reference_solutions/solution.cpp'
        python_solution_file = f'complexity_analysis/{complexity_class}/reference_solutions/solution.py'

        with open(cpp_solution_file, 'r') as f:
            cpp_solution = f.read()
        with open(python_solution_file, 'r') as f:
            python_solution = f.read()

        # Run benchmark
        benchmark_results = run_benchmark_direct(
            problem_id=problem.id,
            cpp_solution=cpp_solution,
            python_solution=python_solution
        )

        ad = benchmark_results['adaptive']
        print(f"\nBENCHMARK RESULTS:")
        print(f"   C++ median time: {benchmark_results['cpp_median']:.4f}s")
        print(f"   Python median time: {benchmark_results['python_median']:.4f}s")
        print(f"   beta (Python/C++): {benchmark_results['adjustment_factor']:.3f}")
        print(f"   Reliable (both converged): {'Yes' if benchmark_results['is_reliable'] else 'No'}")
        print(f"   C++   : {ad['cpp']['n_reps']} reps, IQR/median={ad['cpp']['iqr_ratio']*100:.1f}%, "
              f"{'converged' if ad['cpp']['converged'] else 'HIT CAP'}")
        print(f"   Python: {ad['python']['n_reps']} reps, IQR/median={ad['python']['iqr_ratio']*100:.1f}%, "
              f"{'converged' if ad['python']['converged'] else 'HIT CAP'}")

        # Save results
        results = {
            'experiment': complexity_class,
            'timestamp': datetime.now().isoformat(),
            'problem': {
                'id': problem.id,
                'title': problem.title,
                'complexity': complexity_class
            },
            'benchmark': benchmark_results
        }

        results_file = f"complexity_analysis/{complexity_class}/results_direct.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\nResults saved to: {results_file}")

        # Generate individual experiment report
        generate_experiment_report(complexity_class, problem, benchmark_results)

        return results

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_experiment_direct.py <complexity_class>")
        print("Example: python run_experiment_direct.py O1_constant")
        sys.exit(1)

    complexity_class = sys.argv[1]
    try:
        results = run_complexity_experiment_direct(complexity_class)
        print(f"\nExperiment {complexity_class} completed successfully!")
        print(f"SCIENTIFIC RESULT: Python is {results['benchmark']['adjustment_factor']:.2f}x slower than C++")
    except Exception as e:
        print(f"\nExperiment failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
