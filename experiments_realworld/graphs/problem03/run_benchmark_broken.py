#!/usr/bin/env python3
"""
CSES 1750 Planets Queries I - Adaptive Benchmark System
Binary Lifting Algorithm Performance Analysis
"""

import json
import os
import subprocess
import time
import statistics
import argparse
from pathlib import Path

class PlanetsQueriesBenchmark:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.solutions_dir = self.base_dir / "solutions"
        self.tests_dir = self.base_dir / "tests"
        self.results_dir = self.base_dir / "results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Critical cases based on CSES validation
        self.critical_cases = [6, 7, 8, 9, 10, 12, 14]
        self.control_cases = [1, 2, 3, 4, 5, 11, 13]
        
    def get_test_cases(self):
        """Get all available test cases"""
        test_files = list(self.tests_dir.glob("*.in"))
        return sorted([int(f.stem) for f in test_files])
    
    def execute_solution(self, language, test_case, time_limit=30.0):
        """Execute solution with specified time limit"""
        if language == "cpp":
            # Compile C++ solution
            cpp_file = self.solutions_dir / "solution.cpp"
            exe_file = self.solutions_dir / "solution_cpp"
            
            compile_cmd = [
                "docker", "run", "--rm", "-v", f"{self.solutions_dir}:/code",
                "gcc:latest", "g++", "-O2", "-std=c++17", 
                "/code/solution.cpp", "-o", "/code/solution_cpp"
            ]
            
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
            if compile_result.returncode != 0:
                return {
                    "status": "COMPILATION_ERROR",
                    "time": 0,
                    "error": compile_result.stderr
                }
            
            # Execute C++ solution
            input_file = self.tests_dir / f"{test_case}.in"
            expected_file = self.tests_dir / f"{test_case}.out"
            
            with open(input_file, 'r') as f:
                input_data = f.read()
            
            start_time = time.time()
            run_cmd = [
                "docker", "run", "--rm", "-v", f"{self.solutions_dir}:/code",
                "gcc:latest", "timeout", str(time_limit), "/code/solution_cpp"
            ]
            
            try:
                result = subprocess.run(
                    run_cmd, input=input_data, capture_output=True, 
                    text=True, timeout=time_limit + 5
                )
                execution_time = time.time() - start_time
                
                if result.returncode == 124:  # timeout exit code
                    return {"status": "TLE", "time": time_limit}
                elif result.returncode != 0:
                    return {"status": "RUNTIME_ERROR", "time": execution_time, "error": result.stderr}
                
                # Validate output
                with open(expected_file, 'r') as f:
                    expected = f.read().strip()
                
                if result.stdout.strip() == expected:
                    return {"status": "ACCEPTED", "time": execution_time}
                else:
                    return {"status": "WRONG_ANSWER", "time": execution_time}
                    
            except subprocess.TimeoutExpired:
                return {"status": "TLE", "time": time_limit}
                
        elif language == "python":
            # Execute Python solution
            py_file = self.solutions_dir / "solution.py"
            input_file = self.tests_dir / f"{test_case}.in"
            expected_file = self.tests_dir / f"{test_case}.out"
            
            with open(input_file, 'r') as f:
                input_data = f.read()
            
            start_time = time.time()
            run_cmd = [
                "docker", "run", "--rm", "-v", f"{self.solutions_dir}:/code",
                "python:3.11-slim", "timeout", str(time_limit), 
                "python", "/code/solution.py"
            ]
            
            try:
                result = subprocess.run(
                    run_cmd, input=input_data, capture_output=True, 
                    text=True, timeout=time_limit + 5
                )
                execution_time = time.time() - start_time
                
                if result.returncode == 124:  # timeout exit code
                    return {"status": "TLE", "time": time_limit}
                elif result.returncode != 0:
                    return {"status": "RUNTIME_ERROR", "time": execution_time, "error": result.stderr}
                
                # Validate output
                with open(expected_file, 'r') as f:
                    expected = f.read().strip()
                
                if result.stdout.strip() == expected:
                    return {"status": "ACCEPTED", "time": execution_time}
                else:
                    return {"status": "WRONG_ANSWER", "time": execution_time}
                    
            except subprocess.TimeoutExpired:
                return {"status": "TLE", "time": time_limit}
    
    def run_calibration(self, time_limit=30.0):
        """Run calibration phase with multiple repetitions"""
        print("=== CALIBRATION PHASE ===")
        print("Running C++ and Python solutions on critical cases...")
        
        # Focus on critical cases for efficiency
        test_cases = self.critical_cases + [1, 11, 13]  # Add some control cases
        repetitions = 10
        
        results = {
            "cpp": {},
            "python": {},
            "metadata": {
                "repetitions": repetitions,
                "test_cases": test_cases,
                "time_limit": time_limit,
                "timestamp": time.time()
            }
        }
        
        for test_case in test_cases:
            print(f"\nTesting case {test_case}...")
            
            # C++ measurements
            cpp_times = []
            cpp_statuses = []
            for rep in range(repetitions):
                result = self.execute_solution("cpp", test_case, time_limit)
                cpp_times.append(result["time"])
                cpp_statuses.append(result["status"])
                print(f"  C++ run {rep+1}: {result['status']} ({result['time']:.3f}s)")
            
            # Python measurements
            python_times = []
            python_statuses = []
            for rep in range(repetitions):
                result = self.execute_solution("python", test_case, time_limit)
                python_times.append(result["time"])
                python_statuses.append(result["status"])
                print(f"  Python run {rep+1}: {result['status']} ({result['time']:.3f}s)")
            
            results["cpp"][test_case] = {
                "times": cpp_times,
                "statuses": cpp_statuses,
                "median_time": statistics.median(cpp_times),
                "success_rate": cpp_statuses.count("ACCEPTED") / repetitions
            }
            
            results["python"][test_case] = {
                "times": python_times,
                "statuses": python_statuses,
                "median_time": statistics.median(python_times),
                "success_rate": python_statuses.count("ACCEPTED") / repetitions
            }
        
        # Save calibration results
        calibration_file = self.results_dir / "calibration_results.json"
        with open(calibration_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nCalibration results saved to {calibration_file}")
        return results
    
    def calculate_adjustment_factor(self, calibration_results):
        """Calculate optimal adjustment factor based on calibration data"""
        print("\n=== ADJUSTMENT FACTOR CALCULATION ===")
        
        cpp_times = []
        python_times = []
        
        # Collect successful execution times
        for test_case in calibration_results["cpp"]:
            cpp_data = calibration_results["cpp"][test_case]
            python_data = calibration_results["python"][test_case]
            
            # Only consider cases where both succeeded at least once
            if cpp_data["success_rate"] > 0 and python_data["success_rate"] > 0:
                cpp_times.append(cpp_data["median_time"])
                python_times.append(python_data["median_time"])
        
        if not cpp_times or not python_times:
            print("Warning: Insufficient data for factor calculation")
            return 15.0  # Conservative default
        
        # Calculate individual ratios
        ratios = [p/c for p, c in zip(python_times, cpp_times) if c > 0]
        
        if ratios:
            median_ratio = statistics.median(ratios)
            # Add safety margin for adaptive system
            adjustment_factor = median_ratio * 1.5
            
            print(f"Individual ratios: {[f'{r:.2f}' for r in ratios]}")
            print(f"Median ratio: {median_ratio:.2f}")
            print(f"Adjustment factor (with 1.5x safety margin): {adjustment_factor:.2f}")
            
            return adjustment_factor
        else:
            print("Warning: No valid ratios found, using default factor")
            return 15.0
    
    def run_validation(self, adjustment_factor, time_limit=1.0):
        """Run validation phase with adaptive time limits"""
        print(f"\n=== VALIDATION PHASE ===")
        print(f"Testing with traditional limit: {time_limit}s")
        print(f"Testing with adaptive limit: {time_limit * adjustment_factor:.2f}s")
        
        test_cases = self.get_test_cases()
        
        results = {
            "traditional": {"cpp": {}, "python": {}},
            "adaptive": {"cpp": {}, "python": {}},
            "metadata": {
                "adjustment_factor": adjustment_factor,
                "traditional_limit": time_limit,
                "adaptive_limit": time_limit * adjustment_factor,
                "timestamp": time.time()
            }
        }
        
        for test_case in test_cases:
            print(f"\nValidating case {test_case}...")
            
            # Traditional system (1.0s for both)
            cpp_traditional = self.execute_solution("cpp", test_case, time_limit)
            python_traditional = self.execute_solution("python", test_case, time_limit)
            
            # Adaptive system (adjusted limit for Python)
            cpp_adaptive = self.execute_solution("cpp", test_case, time_limit)
            python_adaptive = self.execute_solution("python", test_case, time_limit * adjustment_factor)
            
            results["traditional"]["cpp"][test_case] = cpp_traditional
            results["traditional"]["python"][test_case] = python_traditional
            results["adaptive"]["cpp"][test_case] = cpp_adaptive
            results["adaptive"]["python"][test_case] = python_adaptive
            
            print(f"  Traditional: C++ {cpp_traditional['status']}, Python {python_traditional['status']}")
            print(f"  Adaptive: C++ {cpp_adaptive['status']}, Python {python_adaptive['status']}")
        
        # Save validation results
        validation_file = self.results_dir / "validation_results.json"
        with open(validation_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nValidation results saved to {validation_file}")
        return results

def main():
    parser = argparse.ArgumentParser(description="CSES 1750 Adaptive Benchmark")
    parser.add_argument("--time-limit", type=float, default=1.0, help="Base time limit in seconds")
    args = parser.parse_args()
    
    # Initialize benchmark system
    base_dir = Path(__file__).parent
    benchmark = PlanetsQueriesBenchmark(base_dir)
    
    print("CSES 1750 - Planets Queries I Adaptive Benchmark")
    print("=" * 50)
    
    # Phase 1: Calibration
    calibration_results = benchmark.run_calibration(time_limit=30.0)
    
    # Phase 2: Calculate adjustment factor
    adjustment_factor = benchmark.calculate_adjustment_factor(calibration_results)
    
    # Phase 3: Validation
    validation_results = benchmark.run_validation(adjustment_factor, args.time_limit)
    
    print("\n" + "=" * 50)
    print("EXPERIMENT COMPLETED SUCCESSFULLY")
    print(f"Adjustment factor: {adjustment_factor:.2f}x")
    print("Results saved in ./results/ directory")

if __name__ == "__main__":
    main()
