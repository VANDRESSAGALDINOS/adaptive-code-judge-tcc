#!/usr/bin/env python3

import subprocess
import json
import time
import argparse
import statistics
import os
from pathlib import Path

def compile_cpp(source_file, output_file):
    """Compile C++ solution"""
    try:
        result = subprocess.run([
            'g++', '-O2', '-std=c++17', source_file, '-o', output_file
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            print(f"Compilation failed: {result.stderr}")
            return False
        return True
    except subprocess.TimeoutExpired:
        print("Compilation timeout")
        return False

def run_solution(executable, input_data, time_limit=3.0, is_python=False):
    """Run solution with input data and measure time"""
    try:
        if is_python:
            cmd = ['python3', executable]
        else:
            cmd = [f'./{executable}']
        
        start_time = time.time()
        result = subprocess.run(
            cmd, 
            input=input_data, 
            capture_output=True, 
            text=True, 
            timeout=time_limit
        )
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        if result.returncode != 0:
            return None, execution_time, f"Runtime error: {result.stderr}"
        
        return result.stdout.strip(), execution_time, None
        
    except subprocess.TimeoutExpired:
        return None, time_limit, "Time limit exceeded"
    except Exception as e:
        return None, 0, f"Error: {str(e)}"

def load_test_case(test_dir, case_num):
    """Load input and expected output for a test case"""
    input_file = test_dir / f"{case_num}.in"
    output_file = test_dir / f"{case_num}.out"
    
    if not input_file.exists() or not output_file.exists():
        return None, None
    
    with open(input_file, 'r') as f:
        input_data = f.read()
    
    with open(output_file, 'r') as f:
        expected_output = f.read().strip()
    
    return input_data, expected_output

def run_calibration(args):
    """Run calibration phase"""
    print(f"🔧 CALIBRATION PHASE - Case {args.calibration_case}")
    
    # Paths
    test_dir = Path("tests_cses")
    cpp_source = Path("solutions/solution.cpp")
    python_source = Path("solutions/solution.py")
    cpp_executable = "solution_cpp"
    
    # Compile C++
    if not compile_cpp(cpp_source, cpp_executable):
        return {"error": "C++ compilation failed"}
    
    # Load test case
    input_data, expected_output = load_test_case(test_dir, args.calibration_case)
    if input_data is None:
        return {"error": f"Test case {args.calibration_case} not found"}
    
    results = {
        "test_case": args.calibration_case,
        "repetitions": args.calibration_reps,
        "time_limit": args.time_limit,
        "cpp_times": [],
        "python_times": [],
        "cpp_success": 0,
        "python_success": 0
    }
    
    # Run C++ multiple times
    print(f"Running C++ {args.calibration_reps} times...")
    for i in range(args.calibration_reps):
        output, exec_time, error = run_solution(cpp_executable, input_data, args.time_limit)
        if error is None and output == expected_output:
            results["cpp_times"].append(exec_time)
            results["cpp_success"] += 1
        else:
            print(f"C++ run {i+1} failed: {error}")
    
    # Run Python multiple times
    print(f"Running Python {args.calibration_reps} times...")
    for i in range(args.calibration_reps):
        output, exec_time, error = run_solution(python_source, input_data, args.time_limit, is_python=True)
        if error is None and output == expected_output:
            results["python_times"].append(exec_time)
            results["python_success"] += 1
        else:
            print(f"Python run {i+1} failed: {error}")
    
    # Calculate statistics
    if results["cpp_times"]:
        results["cpp_stats"] = {
            "mean": statistics.mean(results["cpp_times"]),
            "median": statistics.median(results["cpp_times"]),
            "min": min(results["cpp_times"]),
            "max": max(results["cpp_times"]),
            "std": statistics.stdev(results["cpp_times"]) if len(results["cpp_times"]) > 1 else 0
        }
        results["cpp_iqr"] = (results["cpp_stats"]["std"] / results["cpp_stats"]["mean"]) * 100 if results["cpp_stats"]["mean"] > 0 else 0
    
    if results["python_times"]:
        results["python_stats"] = {
            "mean": statistics.mean(results["python_times"]),
            "median": statistics.median(results["python_times"]),
            "min": min(results["python_times"]),
            "max": max(results["python_times"]),
            "std": statistics.stdev(results["python_times"]) if len(results["python_times"]) > 1 else 0
        }
        results["python_iqr"] = (results["python_stats"]["std"] / results["python_stats"]["mean"]) * 100 if results["python_stats"]["mean"] > 0 else 0
    
    # Calculate performance ratio
    if results["cpp_times"] and results["python_times"]:
        results["performance_ratio"] = results["python_stats"]["mean"] / results["cpp_stats"]["mean"]
    
    # Save results
    with open("calibration_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print(f"\n📊 CALIBRATION RESULTS:")
    print(f"C++ Success: {results['cpp_success']}/{args.calibration_reps}")
    print(f"Python Success: {results['python_success']}/{args.calibration_reps}")
    
    if results["cpp_times"]:
        print(f"C++ Mean: {results['cpp_stats']['mean']:.4f}s (IQR: {results['cpp_iqr']:.1f}%)")
    if results["python_times"]:
        print(f"Python Mean: {results['python_stats']['mean']:.4f}s (IQR: {results['python_iqr']:.1f}%)")
    if "performance_ratio" in results:
        print(f"Performance Ratio (Python/C++): {results['performance_ratio']:.2f}x")
    
    # Cleanup
    if os.path.exists(cpp_executable):
        os.remove(cpp_executable)
    
    return results

def run_validation(args):
    """Run validation phase with multiple test cases"""
    print(f"🧪 VALIDATION PHASE - Cases {args.validation_cases}")
    
    # Paths
    test_dir = Path("tests_cses")
    cpp_source = Path("solutions/solution.cpp")
    python_source = Path("solutions/solution.py")
    cpp_executable = "solution_cpp"
    
    # Compile C++
    if not compile_cpp(cpp_source, cpp_executable):
        return {"error": "C++ compilation failed"}
    
    results = {
        "test_cases": args.validation_cases,
        "repetitions": args.validation_reps,
        "time_limit": args.time_limit,
        "cases": {}
    }
    
    for case_num in args.validation_cases:
        print(f"\n📝 Testing case {case_num}...")
        
        # Load test case
        input_data, expected_output = load_test_case(test_dir, case_num)
        if input_data is None:
            print(f"⚠️ Test case {case_num} not found, skipping")
            continue
        
        case_results = {
            "cpp_times": [],
            "python_times": [],
            "cpp_success": 0,
            "python_success": 0
        }
        
        # Run C++
        for i in range(args.validation_reps):
            output, exec_time, error = run_solution(cpp_executable, input_data, args.time_limit)
            if error is None and output == expected_output:
                case_results["cpp_times"].append(exec_time)
                case_results["cpp_success"] += 1
        
        # Run Python
        for i in range(args.validation_reps):
            output, exec_time, error = run_solution(python_source, input_data, args.time_limit, is_python=True)
            if error is None and output == expected_output:
                case_results["python_times"].append(exec_time)
                case_results["python_success"] += 1
        
        # Calculate statistics for this case
        if case_results["cpp_times"]:
            case_results["cpp_mean"] = statistics.mean(case_results["cpp_times"])
        if case_results["python_times"]:
            case_results["python_mean"] = statistics.mean(case_results["python_times"])
        
        if case_results["cpp_times"] and case_results["python_times"]:
            case_results["performance_ratio"] = case_results["python_mean"] / case_results["cpp_mean"]
        
        results["cases"][str(case_num)] = case_results
        
        # Print case summary
        print(f"  C++: {case_results['cpp_success']}/{args.validation_reps} success")
        print(f"  Python: {case_results['python_success']}/{args.validation_reps} success")
        if "performance_ratio" in case_results:
            print(f"  Ratio: {case_results['performance_ratio']:.2f}x")
    
    # Save results
    with open("validation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Cleanup
    if os.path.exists(cpp_executable):
        os.remove(cpp_executable)
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Apple Division Benchmark Tool")
    
    # Calibration arguments
    parser.add_argument("--calibration-case", type=int, help="Test case for calibration")
    parser.add_argument("--calibration-reps", type=int, default=5, help="Repetitions for calibration")
    
    # Validation arguments
    parser.add_argument("--validation-cases", type=int, nargs="+", help="Test cases for validation")
    parser.add_argument("--validation-reps", type=int, default=5, help="Repetitions per validation case")
    
    # Common arguments
    parser.add_argument("--time-limit", type=float, default=3.0, help="Time limit in seconds")
    
    args = parser.parse_args()
    
    if args.calibration_case:
        results = run_calibration(args)
        print(f"\n✅ Calibration completed. Results saved to calibration_results.json")
    elif args.validation_cases:
        results = run_validation(args)
        print(f"\n✅ Validation completed. Results saved to validation_results.json")
    else:
        print("❌ Please specify either --calibration-case or --validation-cases")
        parser.print_help()

if __name__ == "__main__":
    main()
