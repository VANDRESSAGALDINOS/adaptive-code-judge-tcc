#!/usr/bin/env python3
"""
CSES 1672 Slow Solutions Validation
Validates that slow solutions receive TLE in both traditional and adaptive systems
Following experiment_plan.md selectivity preservation protocol
"""

import argparse
import json
import subprocess
import tempfile
import time
from datetime import datetime
from pathlib import Path

class SlowSolutionValidator:
    """Validator for slow solution selectivity preservation."""
    
    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir or ".")
        self.slow_solutions_dir = self.base_dir / "slow_validation" / "solutions_slow"
        self.tests_dir = self.base_dir / "tests"
        self.results_dir = self.base_dir / "results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Docker configuration
        self.cpp_image = "gcc:latest"  # Already has g++ and build tools
        self.python_image = "python:3.11-slim"
    
    def execute_slow_solution(self, solution_file, test_case_id, language, time_limit):
        """Execute slow solution with specified time limit."""
        test_input = self.tests_dir / f"{test_case_id}.in"
        
        if not test_input.exists():
            raise FileNotFoundError(f"Test case {test_case_id}.in not found")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Setup solution file
            if language == "cpp":
                temp_solution = temp_path / "slow_solution.cpp"
                compile_cmd = "g++ -O3 -o slow_solution slow_solution.cpp"
                run_cmd = f"timeout {time_limit}s ./slow_solution"
            else:  # python
                temp_solution = temp_path / "slow_solution.py"
                compile_cmd = None
                run_cmd = f"timeout {time_limit}s python3 slow_solution.py"
            
            # Copy files
            with open(solution_file, 'r') as src, open(temp_solution, 'w') as dst:
                dst.write(src.read())
            
            with open(test_input, 'r') as src, open(temp_path / "input.txt", 'w') as dst:
                dst.write(src.read())
            
            # Docker execution
            docker_base_cmd = [
                "docker", "run", "--rm",
                "--cpus=1.0", "--memory=512m",
                "--network=none",
                "-v", f"{temp_path}:/workspace",
                "-w", "/workspace"
            ]
            
            try:
                # Compilation step (C++ only)
                if compile_cmd:
                    compile_result = subprocess.run(
                        docker_base_cmd + [self.cpp_image, "bash", "-c", compile_cmd],
                        capture_output=True, text=True, timeout=30
                    )
                    if compile_result.returncode != 0:
                        return {
                            'status': 'COMPILATION_ERROR',
                            'execution_time': 0.0,
                            'stderr': compile_result.stderr
                        }
                
                # Execution step
                image = self.cpp_image if language == "cpp" else self.python_image
                start_time = time.time()
                
                exec_result = subprocess.run(
                    docker_base_cmd + [image, "bash", "-c", f"{run_cmd} < input.txt"],
                    capture_output=True, text=True, timeout=time_limit + 5
                )
                
                wall_time = time.time() - start_time
                
                # Use wall time since we're not using /usr/bin/time anymore
                execution_time = wall_time
                
                # Determine status
                if exec_result.returncode == 124 or execution_time >= time_limit:
                    status = 'TLE'
                elif exec_result.returncode != 0:
                    status = 'RUNTIME_ERROR'
                else:
                    status = 'ACCEPTED'  # This would be unexpected for slow solutions
                
                return {
                    'status': status,
                    'execution_time': execution_time,
                    'wall_time': wall_time,
                    'returncode': exec_result.returncode
                }
                
            except subprocess.TimeoutExpired:
                return {
                    'status': 'TLE',
                    'execution_time': time_limit,
                    'wall_time': time_limit
                }
            except Exception as e:
                return {
                    'status': 'INTERNAL_ERROR',
                    'execution_time': 0.0,
                    'error': str(e)
                }
    
    def validate_selectivity(self, test_cases=None, adjustment_factor=None):
        """
        Validate that slow solutions receive TLE in both systems.
        This ensures adaptive limits don't compromise algorithmic selectivity.
        """
        if test_cases is None:
            test_cases = [8, 15]  # Representative medium and large cases
        
        # Load adjustment factor from calibration if not provided
        if adjustment_factor is None:
            try:
                calibration_file = self.results_dir / "calibration_case8.json"
                with open(calibration_file, 'r') as f:
                    calibration_data = json.load(f)
                    adjustment_factor = calibration_data['statistics']['adjustment_factor']
            except (FileNotFoundError, KeyError):
                print("⚠️  No calibration data found, using default factor 2.5x")
                adjustment_factor = 2.5
        
        print(f"=== SLOW SOLUTION VALIDATION ===")
        print(f"Test cases: {test_cases}")
        print(f"Adjustment factor: {adjustment_factor:.2f}x")
        print(f"Purpose: Verify algorithmic selectivity preservation")
        
        # Solution files
        cpp_slow = self.slow_solutions_dir / "slow_solution.cpp"
        python_slow = self.slow_solutions_dir / "slow_solution.py"
        
        if not cpp_slow.exists() or not python_slow.exists():
            raise FileNotFoundError("Slow solution files not found in slow_validation/solutions_slow/")
        
        results = {
            'experiment_metadata': {
                'validation_type': 'selectivity_preservation',
                'test_cases': test_cases,
                'adjustment_factor': adjustment_factor,
                'timestamp': datetime.now().isoformat(),
                'protocol': 'experiment_plan.md'
            },
            'traditional_system': {},
            'adaptive_system': {},
            'selectivity_analysis': {}
        }
        
        for case_id in test_cases:
            print(f"\n🐌 Testing slow solutions on case {case_id}...")
            
            case_results = {
                'traditional': {'cpp': None, 'python': None},
                'adaptive': {'cpp': None, 'python': None}
            }
            
            # Traditional system (1.0s limit for both)
            print(f"  Traditional system (1.0s limit):")
            
            # C++ slow traditional
            print(f"    C++ slow solution: ", end="", flush=True)
            result = self.execute_slow_solution(cpp_slow, case_id, "cpp", time_limit=1.0)
            case_results['traditional']['cpp'] = result
            print(f"{result['status']} ({result['execution_time']:.2f}s)")
            
            # Python slow traditional
            print(f"    Python slow solution: ", end="", flush=True)
            result = self.execute_slow_solution(python_slow, case_id, "python", time_limit=1.0)
            case_results['traditional']['python'] = result
            print(f"{result['status']} ({result['execution_time']:.2f}s)")
            
            # Adaptive system (1.0s C++, adjusted Python)
            adaptive_python_limit = 1.0 * adjustment_factor
            print(f"  Adaptive system (C++: 1.0s, Python: {adaptive_python_limit:.1f}s):")
            
            # C++ slow adaptive (same as traditional)
            print(f"    C++ slow solution: ", end="", flush=True)
            result = self.execute_slow_solution(cpp_slow, case_id, "cpp", time_limit=1.0)
            case_results['adaptive']['cpp'] = result
            print(f"{result['status']} ({result['execution_time']:.2f}s)")
            
            # Python slow adaptive (with increased limit)
            print(f"    Python slow solution: ", end="", flush=True)
            result = self.execute_slow_solution(python_slow, case_id, "python", time_limit=adaptive_python_limit)
            case_results['adaptive']['python'] = result
            print(f"{result['status']} ({result['execution_time']:.2f}s)")
            
            # Store results
            results['traditional_system'][case_id] = case_results['traditional']
            results['adaptive_system'][case_id] = case_results['adaptive']
            
            # Analyze selectivity for this case
            selectivity_preserved = (
                case_results['traditional']['cpp']['status'] == 'TLE' and
                case_results['traditional']['python']['status'] == 'TLE' and
                case_results['adaptive']['cpp']['status'] == 'TLE' and
                case_results['adaptive']['python']['status'] == 'TLE'
            )
            
            results['selectivity_analysis'][case_id] = {
                'selectivity_preserved': selectivity_preserved,
                'all_systems_tle': selectivity_preserved,
                'explanation': 'All slow solutions correctly receive TLE' if selectivity_preserved else 'Some slow solutions unexpectedly passed'
            }
            
            print(f"  Selectivity preserved: {'✓' if selectivity_preserved else '✗'}")
        
        # Overall selectivity analysis
        overall_selectivity = all(
            results['selectivity_analysis'][case_id]['selectivity_preserved']
            for case_id in test_cases
        )
        
        results['overall_selectivity'] = {
            'preserved': overall_selectivity,
            'test_cases_count': len(test_cases),
            'successful_cases': sum(
                1 for case_id in test_cases
                if results['selectivity_analysis'][case_id]['selectivity_preserved']
            ),
            'analysis': 'Selectivity preserved - adaptive limits do not compromise algorithmic discrimination' if overall_selectivity else 'Selectivity compromised - some inefficient solutions incorrectly passed'
        }
        
        print(f"\n📊 SELECTIVITY VALIDATION SUMMARY:")
        print(f"  Cases tested: {len(test_cases)}")
        print(f"  Selectivity preserved: {results['overall_selectivity']['successful_cases']}/{len(test_cases)}")
        print(f"  Overall result: {'✅ SELECTIVITY PRESERVED' if overall_selectivity else '❌ SELECTIVITY COMPROMISED'}")
        
        if overall_selectivity:
            print(f"  ✓ Adaptive system maintains algorithmic rigor")
            print(f"  ✓ Inefficient O(n⁴) solutions correctly fail")
            print(f"  ✓ No gaming of the system possible")
        else:
            print(f"  ✗ Adaptive limits may be too lenient")
            print(f"  ✗ System vulnerable to gaming")
        
        # Save results
        validation_file = self.results_dir / "slow_solution_validation.json"
        with open(validation_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Slow solution validation saved to: {validation_file}")
        return results


def main():
    parser = argparse.ArgumentParser(description='CSES 1672 Slow Solution Validator')
    parser.add_argument('--cases', type=str, default='8,15',
                        help='Comma-separated test cases for validation (default: 8,15)')
    parser.add_argument('--adjustment-factor', type=float, default=None,
                        help='Manual adjustment factor (default: load from calibration)')
    
    args = parser.parse_args()
    
    # Parse test cases
    test_cases = [int(x.strip()) for x in args.cases.split(',')]
    
    validator = SlowSolutionValidator()
    validator.validate_selectivity(test_cases=test_cases, adjustment_factor=args.adjustment_factor)


if __name__ == '__main__':
    main()
