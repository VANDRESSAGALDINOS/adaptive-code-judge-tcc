#!/usr/bin/env python3
"""
Simplified benchmark for Problem03 - focus on working cases
"""

import json
import subprocess
import time
import statistics
from pathlib import Path

def execute_solution(language, test_case, time_limit=30.0):
    """Execute solution with specified time limit"""
    base_dir = Path(".").resolve()
    solutions_dir = base_dir / "solutions"
    tests_dir = base_dir / "tests"
    
    input_file = tests_dir / f"{test_case}.in"
    expected_file = tests_dir / f"{test_case}.out"
    
    with open(input_file, 'r') as f:
        input_data = f.read()
    
    if language == "cpp":
        # Compile and run C++
        compile_cmd = [
            "docker", "run", "--rm", "-v", f"{solutions_dir}:/code",
            "gcc:latest", "g++", "-O2", "-std=c++17", 
            "/code/solution.cpp", "-o", "/code/solution_bench"
        ]
        
        compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
        if compile_result.returncode != 0:
            return {"status": "COMPILATION_ERROR", "time": 0}
        
        start_time = time.time()
        run_cmd = [
            "docker", "run", "--rm", "-v", f"{solutions_dir}:/code",
            "gcc:latest", "timeout", str(time_limit), "/code/solution_bench"
        ]
        
        try:
            result = subprocess.run(
                run_cmd, input=input_data, capture_output=True, 
                text=True, timeout=time_limit + 5
            )
            execution_time = time.time() - start_time
            
            if result.returncode == 124:
                return {"status": "TLE", "time": time_limit}
            elif result.returncode != 0:
                return {"status": "RUNTIME_ERROR", "time": execution_time}
            
            # Check output
            with open(expected_file, 'r') as f:
                expected = f.read().strip()
            
            if result.stdout.strip() == expected:
                return {"status": "ACCEPTED", "time": execution_time}
            else:
                return {"status": "WRONG_ANSWER", "time": execution_time}
                
        except subprocess.TimeoutExpired:
            return {"status": "TLE", "time": time_limit}
            
    elif language == "python":
        start_time = time.time()
        run_cmd = [
            "docker", "run", "--rm", "-v", f"{solutions_dir}:/code",
            "python:3.11-slim", "timeout", str(time_limit), 
            "python", "/code/solution.py"
        ]
        
        try:
            result = subprocess.run(
                run_cmd, input=input_data, capture_output=True, 
                text=True, timeout=time_limit + 5
            )
            execution_time = time.time() - start_time
            
            if result.returncode == 124:
                return {"status": "TLE", "time": time_limit}
            elif result.returncode != 0:
                return {"status": "RUNTIME_ERROR", "time": execution_time}
            
            # Check output
            with open(expected_file, 'r') as f:
                expected = f.read().strip()
            
            if result.stdout.strip() == expected:
                return {"status": "ACCEPTED", "time": execution_time}
            else:
                return {"status": "WRONG_ANSWER", "time": execution_time}
                
        except subprocess.TimeoutExpired:
            return {"status": "TLE", "time": time_limit}

def main():
    print("CSES 1750 - Simplified Benchmark")
    print("=" * 40)
    
    # Test only small cases first
    test_cases = [1, 2, 3, 4, 5]
    
    results = {"cpp": {}, "python": {}}
    
    for test_case in test_cases:
        print(f"\nTesting case {test_case}...")
        
        # Test C++
        cpp_result = execute_solution("cpp", test_case, 5.0)
        print(f"  C++: {cpp_result['status']} ({cpp_result['time']:.3f}s)")
        results["cpp"][test_case] = cpp_result
        
        # Test Python
        python_result = execute_solution("python", test_case, 5.0)
        print(f"  Python: {python_result['status']} ({python_result['time']:.3f}s)")
        results["python"][test_case] = python_result
    
    # Save results
    with open("simple_benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to simple_benchmark_results.json")
    
    # Summary
    cpp_success = sum(1 for r in results["cpp"].values() if r["status"] == "ACCEPTED")
    python_success = sum(1 for r in results["python"].values() if r["status"] == "ACCEPTED")
    
    print(f"\nSUMMARY:")
    print(f"C++ Success: {cpp_success}/{len(test_cases)}")
    print(f"Python Success: {python_success}/{len(test_cases)}")

if __name__ == "__main__":
    main()





