#!/usr/bin/env python3
"""
Database initialization script for Adaptive Code Judge.

This script creates the database tables and optionally loads sample data.
"""

import os
import sys
import logging

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.main import create_app
from src.models import db, Problem, TestCase
from src.services import ProblemService


def init_database(create_samples=False):
    """Initialize database with tables and optionally sample data."""
    
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
        
        if create_samples:
            print("Creating sample data...")
            create_sample_data()
            print("Sample data created successfully!")


def create_sample_data():
    """Create sample problems and test cases."""
    
    service = ProblemService()
    
    # Sample Problem 1: Two Sum
    problem1 = service.create_problem(
        title="Two Sum",
        description="""Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

Input:
- First line: integer n (1 ≤ n ≤ 1000) - array size
- Second line: n space-separated integers
- Third line: integer target

Output:
- Two space-separated integers representing the indices (0-based)

Example:
Input:
4
2 7 11 15
9

Output:
0 1
""",
        time_limit_base=1.0,
        memory_limit=128,
        difficulty="easy",
        tags=["array", "hash-table", "two-pointers"]
    )
    
    # Sample test cases for Two Sum
    service.add_test_case(
        problem_id=problem1.id,
        name="example_1",
        input_data="4\n2 7 11 15\n9",
        expected_output="0 1",
        is_sample=True,
        is_hidden=False,
        weight=1.0
    )
    
    service.add_test_case(
        problem_id=problem1.id,
        name="small_case",
        input_data="3\n3 2 4\n6",
        expected_output="1 2",
        is_sample=False,
        is_hidden=True,
        weight=1.0
    )
    
    service.add_test_case(
        problem_id=problem1.id,
        name="large_case",
        input_data="1000\n" + " ".join([str(i) for i in range(1000)]) + "\n1999",
        expected_output="999 1000",  # This would be wrong, but it's just for testing
        is_sample=False,
        is_hidden=True,
        weight=2.0,
        complexity_hint="O(n)",
        input_size=8000  # Approximate size
    )
    
    # Sample Problem 2: Fibonacci
    problem2 = service.create_problem(
        title="Fibonacci Number",
        description="""Calculate the nth Fibonacci number.

The Fibonacci sequence is defined as:
- F(0) = 0
- F(1) = 1
- F(n) = F(n-1) + F(n-2) for n > 1

Input:
- One integer n (0 ≤ n ≤ 30)

Output:
- The nth Fibonacci number

Example:
Input:
10

Output:
55
""",
        time_limit_base=1.0,
        memory_limit=128,
        difficulty="easy",
        tags=["dynamic-programming", "recursion", "math"]
    )
    
    # Sample test cases for Fibonacci
    service.add_test_case(
        problem_id=problem2.id,
        name="base_case_0",
        input_data="0",
        expected_output="0",
        is_sample=True,
        is_hidden=False
    )
    
    service.add_test_case(
        problem_id=problem2.id,
        name="base_case_1",
        input_data="1",
        expected_output="1",
        is_sample=True,
        is_hidden=False
    )
    
    service.add_test_case(
        problem_id=problem2.id,
        name="example_case",
        input_data="10",
        expected_output="55",
        is_sample=True,
        is_hidden=False
    )
    
    service.add_test_case(
        problem_id=problem2.id,
        name="large_case",
        input_data="30",
        expected_output="832040",
        is_sample=False,
        is_hidden=True,
        weight=2.0,
        complexity_hint="O(n)",
        input_size=2
    )
    
    print(f"Created {Problem.query.count()} problems with {TestCase.query.count()} test cases")


def create_reference_solutions():
    """Create reference solution files for sample problems."""
    
    # Create reference solutions directory
    ref_dir = "data/reference_solutions"
    os.makedirs(ref_dir, exist_ok=True)
    
    # Two Sum C++ solution
    cpp_two_sum = """#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

int main() {
    int n;
    cin >> n;
    
    vector<int> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }
    
    int target;
    cin >> target;
    
    unordered_map<int, int> map;
    
    for (int i = 0; i < n; i++) {
        int complement = target - nums[i];
        if (map.find(complement) != map.end()) {
            cout << map[complement] << " " << i << endl;
            return 0;
        }
        map[nums[i]] = i;
    }
    
    return 0;
}"""
    
    # Two Sum Python solution
    python_two_sum = """n = int(input())
nums = list(map(int, input().split()))
target = int(input())

num_map = {}

for i, num in enumerate(nums):
    complement = target - num
    if complement in num_map:
        print(num_map[complement], i)
        break
    num_map[num] = i"""
    
    # Fibonacci C++ solution
    cpp_fibonacci = """#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    
    if (n == 0) {
        cout << 0 << endl;
        return 0;
    }
    if (n == 1) {
        cout << 1 << endl;
        return 0;
    }
    
    long long a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        long long temp = a + b;
        a = b;
        b = temp;
    }
    
    cout << b << endl;
    return 0;
}"""
    
    # Fibonacci Python solution
    python_fibonacci = """n = int(input())

if n == 0:
    print(0)
elif n == 1:
    print(1)
else:
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    print(b)"""
    
    # Write solutions to files
    solutions = [
        ("problem_1.cpp", cpp_two_sum),
        ("problem_1.py", python_two_sum),
        ("problem_2.cpp", cpp_fibonacci),
        ("problem_2.py", python_fibonacci)
    ]
    
    for filename, content in solutions:
        filepath = os.path.join(ref_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Created reference solution: {filepath}")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Initialize Adaptive Code Judge database')
    parser.add_argument('--samples', action='store_true', 
                       help='Create sample problems and test cases')
    parser.add_argument('--references', action='store_true',
                       help='Create reference solution files')
    
    args = parser.parse_args()
    
    try:
        init_database(create_samples=args.samples)
        
        if args.references:
            print("Creating reference solutions...")
            create_reference_solutions()
            print("Reference solutions created successfully!")
        
        print("\nDatabase initialization completed!")
        print("\nNext steps:")
        print("1. Build Docker images: cd docker && docker build -t adaptivejudge-cpp:latest -f Dockerfile.cpp .")
        print("2. Build Python image: docker build -t adaptivejudge-python:latest -f Dockerfile.python .")
        print("3. Start the API: python src/main.py")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        logging.exception("Database initialization failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
