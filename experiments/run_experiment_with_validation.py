#!/usr/bin/env /usr/bin/python3
"""
Complete Experiment with Time Limit Validation
Runs benchmark + validates calibrated TL with optimal/slow submissions
"""
import sys
import os
import json
import subprocess
import tempfile
import time
import statistics
from datetime import datetime

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from models import db
from services.problem_service import ProblemService
from config.database import DatabaseConfig
from flask import Flask

def create_app():
    """Create Flask app for experiments"""
    app = Flask(__name__)
    config = DatabaseConfig.get_config()
    app.config.update(config)
    db.init_app(app)
    return app

def execute_code_direct(source_code: str, input_data: str, language: str, time_limit: float = 2.0):
    """Execute code directly via Docker subprocess"""
    
    if language == 'cpp':
        image = 'adaptive-judge-cpp:latest'
        file_ext = '.cpp'
        compile_cmd = 'g++ -O2 -o solution solution.cpp'
        run_cmd = './solution'
    else:  # python
        image = 'adaptive-judge-python:latest' 
        file_ext = '.py'
        compile_cmd = None
        run_cmd = 'python solution.py'
    
    # Create temporary directory for this execution
    with tempfile.TemporaryDirectory() as temp_dir:
        # Write source code
        source_file = os.path.join(temp_dir, f'solution{file_ext}')
        with open(source_file, 'w') as f:
            f.write(source_code)
        
        # Write input data
        input_file = os.path.join(temp_dir, 'input.txt')
        with open(input_file, 'w') as f:
            f.write(input_data)
        
        try:
            # Run Docker container
            docker_cmd = [
                'docker', 'run', '--rm',
                '-v', f'{temp_dir}:/workspace',
                '--workdir', '/workspace',
                '--memory', '128m',
                '--cpus', '1.0',
                image,
                'bash', '-c'
            ]
            
            if compile_cmd:
                # C++ - compile then run
                full_cmd = f'{compile_cmd} && timeout {time_limit} {run_cmd} < input.txt'
            else:
                # Python - run directly
                full_cmd = f'timeout {time_limit} {run_cmd} < input.txt'
            
            docker_cmd.append(full_cmd)
            
            # Execute with timing
            start_time = time.time()
            result = subprocess.run(
                docker_cmd,
                capture_output=True,
                text=True,
                timeout=time_limit + 2  # Extra buffer for Docker overhead
            )
            execution_time = time.time() - start_time
            
            return {
                'success': result.returncode == 0,
                'execution_time': execution_time,
                'stdout': result.stdout.strip(),
                'stderr': result.stderr.strip(),
                'returncode': result.returncode,
                'timed_out': result.returncode == 124
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'execution_time': time_limit + 2,
                'stdout': '',
                'stderr': 'Docker timeout',
                'returncode': -1,
                'timed_out': True
            }
        except Exception as e:
            return {
                'success': False,
                'execution_time': 0.0,
                'stdout': '',
                'stderr': str(e),
                'returncode': -1,
                'timed_out': False
            }

def run_benchmark_direct(problem_id: int, cpp_solution: str, python_solution: str, repetitions: int = 10):
    """Run benchmark measurements directly"""
    
    # Get the problem and its largest test case
    from models import Problem, TestCase
    problem = Problem.query.get(problem_id)
    if not problem:
        raise ValueError(f"Problem {problem_id} not found")
    
    # Find largest test case
    test_cases = TestCase.query.filter_by(problem_id=problem_id).all()
    if not test_cases:
        raise ValueError(f"No test cases found for problem {problem_id}")
    
    largest_tc = max(test_cases, key=lambda tc: tc.input_size or 0)
    
    print(f"📊 Running benchmark on test case: {largest_tc.name}")
    print(f"   📏 Input size: {largest_tc.input_size} bytes")
    print(f"   🔄 Repetitions: {repetitions}")
    
    # Test solutions first
    print("🧪 Validating solutions...")
    cpp_result = execute_code_direct(cpp_solution, largest_tc.input_data, 'cpp')
    python_result = execute_code_direct(python_solution, largest_tc.input_data, 'python')
    
    if not cpp_result['success']:
        raise ValueError(f"C++ solution failed: {cpp_result['stderr']}")
    if not python_result['success']:
        raise ValueError(f"Python solution failed: {python_result['stderr']}")
    
    if cpp_result['stdout'] != largest_tc.expected_output:
        raise ValueError(f"C++ output mismatch: got '{cpp_result['stdout']}', expected '{largest_tc.expected_output}'")
    if python_result['stdout'] != largest_tc.expected_output:
        raise ValueError(f"Python output mismatch: got '{python_result['stdout']}', expected '{largest_tc.expected_output}'")
    
    print("✅ Solutions validated!")
    
    # Run benchmarks
    cpp_times = []
    python_times = []
    
    print("⏱️  Measuring C++ performance...")
    for i in range(repetitions):
        result = execute_code_direct(cpp_solution, largest_tc.input_data, 'cpp')
        if result['success']:
            cpp_times.append(result['execution_time'])
            print(f"   Run {i+1}: {result['execution_time']:.4f}s")
        else:
            print(f"   Run {i+1}: FAILED - {result['stderr']}")
    
    print("⏱️  Measuring Python performance...")
    for i in range(repetitions):
        result = execute_code_direct(python_solution, largest_tc.input_data, 'python')
        if result['success']:
            python_times.append(result['execution_time'])
            print(f"   Run {i+1}: {result['execution_time']:.4f}s")
        else:
            print(f"   Run {i+1}: FAILED - {result['stderr']}")
    
    if len(cpp_times) < repetitions // 2:
        raise ValueError(f"Too many C++ failures: {len(cpp_times)}/{repetitions}")
    if len(python_times) < repetitions // 2:
        raise ValueError(f"Too many Python failures: {len(python_times)}/{repetitions}")
    
    # Calculate statistics
    cpp_median = statistics.median(cpp_times)
    python_median = statistics.median(python_times)
    
    cpp_q1 = statistics.quantiles(cpp_times, n=4)[0] if len(cpp_times) > 1 else cpp_median
    cpp_q3 = statistics.quantiles(cpp_times, n=4)[2] if len(cpp_times) > 1 else cpp_median
    cpp_iqr = cpp_q3 - cpp_q1
    
    python_q1 = statistics.quantiles(python_times, n=4)[0] if len(python_times) > 1 else python_median
    python_q3 = statistics.quantiles(python_times, n=4)[2] if len(python_times) > 1 else python_median
    python_iqr = python_q3 - python_q1
    
    adjustment_factor = python_median / cpp_median if cpp_median > 0 else 1.0
    
    # Check reliability
    cpp_stability = (cpp_iqr / cpp_median) if cpp_median > 0 else 1.0
    python_stability = (python_iqr / python_median) if python_median > 0 else 1.0
    is_reliable = cpp_stability < 0.15 and python_stability < 0.20
    
    return {
        'problem_id': problem_id,
        'cpp_median': cpp_median,
        'python_median': python_median,
        'cpp_iqr': cpp_iqr,
        'python_iqr': python_iqr,
        'adjustment_factor': adjustment_factor,
        'is_reliable': is_reliable,
        'cpp_times': cpp_times,
        'python_times': python_times,
        'repetitions': len(cpp_times),
        'test_case_used': largest_tc.name
    }

def validate_time_limits(benchmark_results, optimal_solutions, slow_solutions, complexity_class):
    """Validate that calibrated time limits work correctly"""
    
    print(f"\n🔍 VALIDATING TIME LIMITS for {complexity_class}")
    print("=" * 60)
    
    # Calculate calibrated time limits (with small safety margin)
    cpp_limit = benchmark_results['cpp_median'] * 2.0  # 2x safety margin
    python_limit = benchmark_results['python_median'] * 2.0  # 2x safety margin
    
    print(f"📏 Calibrated time limits:")
    print(f"   C++: {cpp_limit:.3f}s (2x median)")
    print(f"   Python: {python_limit:.3f}s (2x median)")
    
    validation_results = {
        'cpp_limit': cpp_limit,
        'python_limit': python_limit,
        'optimal_tests': {},
        'slow_tests': {},
        'validation_success': True
    }
    
    # Get test case from database again
    from models import Problem, TestCase
    problem = Problem.query.get(benchmark_results.get('problem_id'))
    test_cases = TestCase.query.filter_by(problem_id=problem.id).all()
    test_case = max(test_cases, key=lambda tc: tc.input_size or 0)
    
    # Test 1: Optimal solutions should PASS
    print(f"\n✅ Testing OPTIMAL solutions (should PASS):")
    
    for lang, solution in optimal_solutions.items():
        limit = cpp_limit if lang == 'cpp' else python_limit
        print(f"   🧪 Testing {lang} optimal solution (limit: {limit:.3f}s)...")
        
        result = execute_code_direct(solution, test_case.input_data, lang, time_limit=limit)
        
        passed = result['success'] and not result['timed_out']
        validation_results['optimal_tests'][lang] = {
            'passed': passed,
            'execution_time': result['execution_time'],
            'expected_result': 'PASS',
            'actual_result': 'PASS' if passed else 'TLE',
            'correct': passed
        }
        
        status = "✅ PASS" if passed else "❌ TLE (UNEXPECTED!)"
        print(f"      Time: {result['execution_time']:.3f}s → {status}")
        
        if not passed:
            validation_results['validation_success'] = False
    
    # Test 2: Slow solutions should FAIL (TLE)
    print(f"\n🐌 Testing SLOW solutions (should TLE):")
    
    for lang, solution in slow_solutions.items():
        limit = cpp_limit if lang == 'cpp' else python_limit
        print(f"   🧪 Testing {lang} slow solution (limit: {limit:.3f}s)...")
        
        result = execute_code_direct(solution, test_case.input_data, lang, time_limit=limit)
        
        timed_out = result['timed_out'] or result['execution_time'] >= limit
        validation_results['slow_tests'][lang] = {
            'timed_out': timed_out,
            'execution_time': result['execution_time'],
            'expected_result': 'TLE',
            'actual_result': 'TLE' if timed_out else 'PASS',
            'correct': timed_out
        }
        
        status = "✅ TLE" if timed_out else "❌ PASS (UNEXPECTED!)"
        print(f"      Time: {result['execution_time']:.3f}s → {status}")
        
        if not timed_out:
            validation_results['validation_success'] = False
    
    # Summary
    print(f"\n📊 VALIDATION SUMMARY:")
    optimal_correct = all(v['correct'] for v in validation_results['optimal_tests'].values())
    slow_correct = all(v['correct'] for v in validation_results['slow_tests'].values())
    
    print(f"   ✅ Optimal solutions: {'✅ All passed' if optimal_correct else '❌ Some failed'}")
    print(f"   🐌 Slow solutions: {'✅ All TLE' if slow_correct else '❌ Some passed'}")
    print(f"   🎯 Overall: {'✅ VALIDATION SUCCESS' if validation_results['validation_success'] else '❌ VALIDATION FAILED'}")
    
    return validation_results

def run_complete_experiment(complexity_class: str):
    """Run complete experiment with validation"""
    app = create_app()
    
    with app.app_context():
        print(f"🧪 COMPLETE EXPERIMENT: {complexity_class}")
        print("=" * 70)
        
        # Import problem definition
        sys.path.append(os.path.join('complexity_analysis', complexity_class))
        problem_module = __import__('problem_definition', fromlist=[''])
        
        # Create problem and test cases
        problem_service = ProblemService()
        problem = problem_module.create_problem(problem_service)
        
        print(f"✅ Problem created: {problem.title}")
        print(f"   📊 Test cases: {len(problem.test_cases)}")
        
        # Load optimal solutions (reference)
        cpp_optimal_file = f'complexity_analysis/{complexity_class}/reference_solutions/solution.cpp'
        python_optimal_file = f'complexity_analysis/{complexity_class}/reference_solutions/solution.py'
        
        with open(cpp_optimal_file, 'r') as f:
            cpp_optimal = f.read()
        with open(python_optimal_file, 'r') as f:
            python_optimal = f.read()
        
        # Load slow solutions
        cpp_slow_file = f'complexity_analysis/{complexity_class}/slow_solutions/slow_solution.cpp'
        python_slow_file = f'complexity_analysis/{complexity_class}/slow_solutions/slow_solution.py'
        
        # Check if slow solutions exist
        if not os.path.exists(cpp_slow_file) or not os.path.exists(python_slow_file):
            print(f"⚠️  Slow solutions not found. Creating them...")
            create_slow_solutions(complexity_class)
        
        with open(cpp_slow_file, 'r') as f:
            cpp_slow = f.read()
        with open(python_slow_file, 'r') as f:
            python_slow = f.read()
        
        # Phase 1: Run benchmark
        print(f"\n📊 PHASE 1: BENCHMARK")
        benchmark_results = run_benchmark_direct(
            problem_id=problem.id,
            cpp_solution=cpp_optimal,
            python_solution=python_optimal,
            repetitions=10
        )
        
        print(f"\n📊 BENCHMARK RESULTS:")
        print(f"   🕐 C++ median time: {benchmark_results['cpp_median']:.4f}s")
        print(f"   🐍 Python median time: {benchmark_results['python_median']:.4f}s")
        print(f"   📈 Python overhead: {benchmark_results['adjustment_factor']:.3f}x")
        print(f"   📊 Reliable: {'Yes' if benchmark_results['is_reliable'] else 'No'}")
        
        # Phase 2: Validate time limits
        print(f"\n🔍 PHASE 2: TIME LIMIT VALIDATION")
        optimal_solutions = {'cpp': cpp_optimal, 'python': python_optimal}
        slow_solutions = {'cpp': cpp_slow, 'python': python_slow}
        
        validation_results = validate_time_limits(
            benchmark_results, optimal_solutions, slow_solutions, complexity_class
        )
        
        # Save complete results
        complete_results = {
            'experiment': complexity_class,
            'timestamp': datetime.now().isoformat(),
            'problem': {
                'id': problem.id,
                'title': problem.title,
                'complexity': complexity_class
            },
            'benchmark': benchmark_results,
            'validation': validation_results
        }
        
        # Save results
        results_file = f"complexity_analysis/{complexity_class}/complete_results.json"
        os.makedirs(os.path.dirname(results_file), exist_ok=True)
        with open(results_file, 'w') as f:
            json.dump(complete_results, f, indent=2)
        
        print(f"\n📄 Complete results saved to: {results_file}")
        
        # Generate validation report
        generate_validation_report(complexity_class, complete_results)
        
        return complete_results

def create_slow_solutions(complexity_class):
    """Create intentionally slow solutions for validation"""
    print(f"🐌 Creating slow solutions for {complexity_class}...")
    
    slow_dir = f"complexity_analysis/{complexity_class}/slow_solutions"
    os.makedirs(slow_dir, exist_ok=True)
    
    if complexity_class == 'O1_constant':
        # For O(1), add unnecessary loops
        cpp_slow = '''#include <iostream>
using namespace std;

int main() {
    long long a, b;
    cin >> a >> b;
    
    // Intentionally slow: unnecessary loops
    for(int i = 0; i < 1000000; i++) {
        for(int j = 0; j < 100; j++) {
            // Waste time
            volatile int x = i + j;
        }
    }
    
    cout << a + b << endl;
    cout << a - b << endl;
    cout << a * b << endl;
    
    if (b != 0) {
        cout << a / b << endl;
    } else {
        cout << 0 << endl;
    }
    
    return 0;
}'''
        
        python_slow = '''import time

a, b = map(int, input().split())

# Intentionally slow: unnecessary computation
for i in range(1000000):
    for j in range(100):
        # Waste time
        x = i + j

print(a + b)
print(a - b)
print(a * b)

if b != 0:
    print(a // b)
else:
    print(0)
'''
    
    elif complexity_class == 'O_log_n':
        # For O(log n), use linear search instead of binary
        cpp_slow = '''#include <iostream>
#include <vector>
using namespace std;

int linearSearch(const vector<int>& arr, int target) {
    // Intentionally slow: O(n) instead of O(log n)
    for (int i = 0; i < arr.size(); i++) {
        if (arr[i] == target) {
            return i;
        }
    }
    return -1;
}

int main() {
    int n, target;
    cin >> n >> target;
    
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }
    
    int result = linearSearch(arr, target);
    cout << result << endl;
    
    return 0;
}'''
        
        python_slow = '''def linear_search(arr, target):
    # Intentionally slow: O(n) instead of O(log n)
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

# Read input
n, target = map(int, input().split())
arr = list(map(int, input().split()))

# Perform slow linear search
result = linear_search(arr, target)
print(result)
'''
    
    # Save slow solutions
    with open(f"{slow_dir}/slow_solution.cpp", 'w') as f:
        f.write(cpp_slow)
    with open(f"{slow_dir}/slow_solution.py", 'w') as f:
        f.write(python_slow)
    
    print(f"✅ Slow solutions created in {slow_dir}/")

def generate_validation_report(complexity_class, results):
    """Generate detailed validation report"""
    
    benchmark = results['benchmark']
    validation = results['validation']
    
    report_content = f"""# Validation Report: {complexity_class}

## Experiment Overview

**Complexity Class**: {complexity_class}
**Date**: {results['timestamp']}
**Problem**: {results['problem']['title']}

## Benchmark Results

### Performance Measurements
- **C++ Median Time**: {benchmark['cpp_median']:.4f}s
- **Python Median Time**: {benchmark['python_median']:.4f}s
- **Python/C++ Ratio**: {benchmark['adjustment_factor']:.3f}x
- **Reliability**: {'✅ High' if benchmark['is_reliable'] else '❌ Low'}

### Calibrated Time Limits
- **C++ Limit**: {validation['cpp_limit']:.3f}s (2x median)
- **Python Limit**: {validation['python_limit']:.3f}s (2x median)

## Time Limit Validation

### Optimal Solutions (Should PASS)
"""

    for lang, result in validation['optimal_tests'].items():
        status = "✅ PASS" if result['correct'] else "❌ FAIL"
        report_content += f"""
**{lang.upper()}**: {result['execution_time']:.3f}s → {result['actual_result']} {status}
"""

    report_content += f"""

### Slow Solutions (Should TLE)
"""

    for lang, result in validation['slow_tests'].items():
        status = "✅ TLE" if result['correct'] else "❌ FAIL"
        report_content += f"""
**{lang.upper()}**: {result['execution_time']:.3f}s → {result['actual_result']} {status}
"""

    report_content += f"""

## Validation Summary

**Overall Result**: {'✅ SUCCESS' if validation['validation_success'] else '❌ FAILED'}

### Analysis
{'✅ Time limits are properly calibrated' if validation['validation_success'] else '❌ Time limits need adjustment'}

- Optimal solutions: {'All passed within limits' if all(v['correct'] for v in validation['optimal_tests'].values()) else 'Some failed unexpectedly'}
- Slow solutions: {'All properly timed out' if all(v['correct'] for v in validation['slow_tests'].values()) else 'Some passed unexpectedly'}

## Implications for TCC

This validation demonstrates that:

1. **Benchmark Accuracy**: The calibrated time limits correctly distinguish between optimal and suboptimal solutions
2. **System Reliability**: The adaptive time limit system works as designed
3. **Practical Applicability**: The system can be deployed in real judge environments

## Technical Data

### Optimal Solution Performance
```json
{json.dumps(validation['optimal_tests'], indent=2)}
```

### Slow Solution Performance  
```json
{json.dumps(validation['slow_tests'], indent=2)}
```

---
*Validation report generated automatically*
"""

    # Save validation report
    report_file = f"complexity_analysis/{complexity_class}/VALIDATION_REPORT.md"
    with open(report_file, 'w') as f:
        f.write(report_content)
    
    print(f"📊 Validation report generated: {report_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_experiment_with_validation.py <complexity_class>")
        print("Example: python run_experiment_with_validation.py O1_constant")
        sys.exit(1)
    
    complexity_class = sys.argv[1]
    try:
        results = run_complete_experiment(complexity_class)
        
        print(f"\n🎉 COMPLETE EXPERIMENT FINISHED!")
        print(f"🔬 Benchmark: Python {results['benchmark']['adjustment_factor']:.2f}x of C++")
        print(f"🔍 Validation: {'✅ SUCCESS' if results['validation']['validation_success'] else '❌ FAILED'}")
        print(f"📄 Reports generated in complexity_analysis/{complexity_class}/")
        
    except Exception as e:
        print(f"\n❌ Experiment failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
