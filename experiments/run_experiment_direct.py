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
from lib.benchmark_engine import measure_language, compute_beta, select_largest_test_case, run_timed_trials

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


def run_selectivity(complexity_class: str, problem_id: int, beta: float, base_limit: float = 1.0):
    """
    Selectivity check (theoretical axis): run the deliberately-inefficient
    slow_solution under the adaptive limit and confirm it stays rejected.
    Mirrors a real judge: C++ under the traditional base limit, Python under the
    adaptive limit (beta x base). The reference is run too, as a control (must
    pass). Returns None when selectivity does not apply (overhead-floor classes,
    or no slow_solutions/).
    """
    from models import TestCase

    # O(1) and O(log n) sit below the 10:1 scale-dominance floor (S3.2): runtime is
    # dominated by fixed overhead, so beta is not calibratable and selectivity is
    # vacuous (the slow is too trivial to be rejected). Reported as overhead floor only.
    if complexity_class in ('O1_constant', 'O_log_n'):
        print("Overhead-floor class -> skipping selectivity (beta not calibratable).")
        return None

    slow_cpp_path = f'complexity_analysis/{complexity_class}/slow_solutions/slow_solution.cpp'
    slow_py_path = f'complexity_analysis/{complexity_class}/slow_solutions/slow_solution.py'
    if not (os.path.exists(slow_cpp_path) and os.path.exists(slow_py_path)):
        print("No slow_solutions/ -> skipping selectivity (floor class).")
        return None

    test_cases = TestCase.query.filter_by(problem_id=problem_id).all()
    tc = select_largest_test_case(
        test_cases,
        size_fn=lambda c: c.input_size or len(c.input_data),
        id_fn=lambda c: c.id,
    )

    with open(f'complexity_analysis/{complexity_class}/reference_solutions/solution.cpp') as f:
        ref_cpp = f.read()
    with open(f'complexity_analysis/{complexity_class}/reference_solutions/solution.py') as f:
        ref_py = f.read()
    with open(slow_cpp_path) as f:
        slow_cpp = f.read()
    with open(slow_py_path) as f:
        slow_py = f.read()

    cpp_limit = base_limit            # C++ stays on the traditional limit (it is the ruler)
    py_limit = beta * base_limit      # Python gets the adaptive (beta-scaled) limit

    print(f"\nSELECTIVITY on '{tc.name}': C++ limit {cpp_limit:.3f}s, "
          f"Python limit {py_limit:.3f}s (= beta {beta:.3f} x {base_limit}s)")

    def status(src, lang, limit):
        return run_timed_trials(src, tc.input_data, tc.expected_output, lang, 1, limit)[0]['status']

    ref = {'cpp': status(ref_cpp, 'cpp', cpp_limit), 'python': status(ref_py, 'python', py_limit)}
    slow = {'cpp': status(slow_cpp, 'cpp', cpp_limit), 'python': status(slow_py, 'python', py_limit)}

    # Selectivity preserved = the slow submission is rejected (TLE) in BOTH
    # languages even under the generous adaptive limit; reference passes (control).
    preserved = (slow['cpp'] == 'TLE') and (slow['python'] == 'TLE')

    print(f"   reference (control): C++ {ref['cpp']} / Python {ref['python']}")
    print(f"   slow (target)      : C++ {slow['cpp']} / Python {slow['python']}")
    print(f"   selectivity_preserved: {preserved}")

    return {
        'experiment': complexity_class,
        'timestamp': datetime.now().isoformat(),
        'test_case_used': tc.name,
        'base_limit_s': base_limit,
        'beta': beta,
        'cpp_limit_s': cpp_limit,
        'python_limit_s': py_limit,
        'n_trials': 1,
        'reference_verdict': ref,
        'slow_verdict': slow,
        'selectivity_preserved': preserved,
    }


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

        results_dir = f"complexity_analysis/{complexity_class}/results"
        os.makedirs(results_dir, exist_ok=True)
        results_file = f"{results_dir}/calibration.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {results_file}")

        # Selectivity (theoretical axis): the slow_solution must stay rejected
        # under the adaptive limit. Skipped for floor classes (no slow_solutions/).
        sel = run_selectivity(complexity_class, problem.id,
                              benchmark_results['adjustment_factor'])
        if sel is not None:
            sel_file = f"{results_dir}/selectivity.json"
            with open(sel_file, 'w') as f:
                json.dump(sel, f, indent=2)
            print(f"Selectivity saved to: {sel_file}")

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
