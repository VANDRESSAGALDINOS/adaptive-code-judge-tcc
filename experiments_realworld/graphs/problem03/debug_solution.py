#!/usr/bin/env python3
"""Debug script to test solutions manually"""

import subprocess
from pathlib import Path

def test_cpp_solution(test_case):
    base_dir = Path(".").resolve()
    solutions_dir = base_dir / "solutions"
    tests_dir = base_dir / "tests"
    
    # Compile C++
    compile_cmd = [
        "docker", "run", "--rm", "-v", f"{solutions_dir}:/code",
        "gcc:latest", "g++", "-O2", "-std=c++17", 
        "/code/solution.cpp", "-o", "/code/solution_debug"
    ]
    
    compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
    if compile_result.returncode != 0:
        print(f"Compilation error: {compile_result.stderr}")
        return
    
    # Test C++
    input_file = tests_dir / f"{test_case}.in"
    expected_file = tests_dir / f"{test_case}.out"
    
    with open(input_file, 'r') as f:
        input_data = f.read()
    
    run_cmd = [
        "docker", "run", "--rm", "-v", f"{solutions_dir}:/code",
        "gcc:latest", "/code/solution_debug"
    ]
    
    result = subprocess.run(run_cmd, input=input_data, capture_output=True, text=True)
    
    with open(expected_file, 'r') as f:
        expected = f.read()
    
    print(f"=== Test Case {test_case} ===")
    print(f"Return code: {result.returncode}")
    print(f"Stderr: {result.stderr}")
    print(f"Output length: {len(result.stdout)}")
    print(f"Expected length: {len(expected)}")
    print(f"Output (first 200 chars): {repr(result.stdout[:200])}")
    print(f"Expected (first 200 chars): {repr(expected[:200])}")
    print(f"Match: {result.stdout.strip() == expected.strip()}")

def test_python_solution(test_case):
    base_dir = Path(".").resolve()
    solutions_dir = base_dir / "solutions"
    tests_dir = base_dir / "tests"
    
    input_file = tests_dir / f"{test_case}.in"
    expected_file = tests_dir / f"{test_case}.out"
    
    with open(input_file, 'r') as f:
        input_data = f.read()
    
    run_cmd = [
        "docker", "run", "--rm", "-v", f"{solutions_dir}:/code",
        "python:3.11-slim", "python", "/code/solution.py"
    ]
    
    result = subprocess.run(run_cmd, input=input_data, capture_output=True, text=True)
    
    with open(expected_file, 'r') as f:
        expected = f.read()
    
    print(f"=== Python Test Case {test_case} ===")
    print(f"Return code: {result.returncode}")
    print(f"Stderr: {result.stderr}")
    print(f"Output length: {len(result.stdout)}")
    print(f"Expected length: {len(expected)}")
    print(f"Output (first 200 chars): {repr(result.stdout[:200])}")
    print(f"Expected (first 200 chars): {repr(expected[:200])}")
    print(f"Match: {result.stdout.strip() == expected.strip()}")

if __name__ == "__main__":
    test_cpp_solution(1)
    test_python_solution(1)
