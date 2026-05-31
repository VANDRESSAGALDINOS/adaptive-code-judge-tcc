#!/usr/bin/env /usr/bin/python3
"""
Complexity Analysis Experiment Runner
Uses existing MVP services for scientific experiments
"""
import sys
import os
import json
from datetime import datetime

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from models import db
from services.problem_service import ProblemService
from services.benchmark_service import BenchmarkService
from config.database import DatabaseConfig
from flask import Flask

def create_app():
    """Create Flask app for experiments"""
    app = Flask(__name__)
    config = DatabaseConfig.get_config()
    app.config.update(config)
    db.init_app(app)
    return app

def run_complexity_experiment(complexity_class: str):
    """Run experiment for a specific complexity class"""
    app = create_app()
    
    with app.app_context():
        print(f"🧪 Running {complexity_class} Complexity Experiment")
        print("=" * 60)
        
        # Import problem definition
        problem_module = __import__(f'{complexity_class}.problem_definition', fromlist=[''])
        
        # Create problem and test cases
        problem_service = ProblemService()
        problem = problem_module.create_problem(problem_service)
        
        print(f"✅ Problem created: {problem.title}")
        print(f"   📊 Test cases: {len(problem.test_cases)}")
        
        # Create benchmarks
        benchmark_service = BenchmarkService()
        benchmark = benchmark_service.create_benchmark(
            problem_id=problem.id,
            repetitions=10,
            activated_by=f"experiment_{complexity_class}"
        )
        
        print(f"✅ Benchmark completed: ID {benchmark.id}")
        print(f"   🕐 C++ base time: {benchmark.base_time_cpp}s")
        print(f"   🐍 Python factor: {benchmark.adjustment_factor_python}x")
        print(f"   📈 Reliable: {'Yes' if benchmark.is_reliable else 'No'}")
        
        # Export results
        results = {
            'experiment': complexity_class,
            'timestamp': datetime.now().isoformat(),
            'problem': {
                'id': problem.id,
                'title': problem.title,
                'complexity': complexity_class
            },
            'benchmark': {
                'id': benchmark.id,
                'cpp_base_time': benchmark.base_time_cpp,
                'python_factor': benchmark.adjustment_factor_python,
                'is_reliable': benchmark.is_reliable,
                'repetitions': benchmark.repetitions
            }
        }
        
        # Save results
        results_file = f"{complexity_class}/results.json"
        os.makedirs(os.path.dirname(results_file), exist_ok=True)
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📄 Results saved to: {results_file}")
        return results

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_experiment.py <complexity_class>")
        print("Example: python run_experiment.py O1_constant")
        sys.exit(1)
    
    complexity_class = sys.argv[1]
    results = run_complexity_experiment(complexity_class)
    
    print(f"\n🎉 Experiment {complexity_class} completed!")
    print(f"Python overhead: {results['benchmark']['python_factor']:.2f}x")
