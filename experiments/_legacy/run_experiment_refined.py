#!/usr/bin/env /usr/bin/python3
"""
Refined Experiment - Separates Docker overhead from algorithmic performance
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

def measure_docker_overhead():
    """Measure pure Docker overhead with minimal operations"""
    print("📏 Measuring Docker overhead...")
    
    cpp_times = []
    python_times = []
    
    # Minimal C++ program
    cpp_code = '''
#include <iostream>
using namespace std;
int main() {
    cout << "hello" << endl;
    return 0;
}
'''
    
    # Minimal Python program  
    python_code = '''
print("hello")
'''
    
    for i in range(5):
        # Measure C++ overhead
        with tempfile.TemporaryDirectory() as temp_dir:
            source_file = os.path.join(temp_dir, 'solution.cpp')
            with open(source_file, 'w') as f:
                f.write(cpp_code)
            
            start_time = time.time()
            result = subprocess.run([
                'docker', 'run', '--rm',
                '-v', f'{temp_dir}:/workspace',
                '--workdir', '/workspace',
                'adaptive-judge-cpp:latest',
                'bash', '-c', 'g++ -o solution solution.cpp && ./solution'
            ], capture_output=True, text=True)
            cpp_times.append(time.time() - start_time)
        
        # Measure Python overhead
        with tempfile.TemporaryDirectory() as temp_dir:
            source_file = os.path.join(temp_dir, 'solution.py')
            with open(source_file, 'w') as f:
                f.write(python_code)
            
            start_time = time.time()
            result = subprocess.run([
                'docker', 'run', '--rm',
                '-v', f'{temp_dir}:/workspace',
                '--workdir', '/workspace',
                'adaptive-judge-python:latest',
                'bash', '-c', 'python solution.py'
            ], capture_output=True, text=True)
            python_times.append(time.time() - start_time)
    
    cpp_overhead = statistics.median(cpp_times)
    python_overhead = statistics.median(python_times)
    
    print(f"   🔧 C++ Docker overhead: {cpp_overhead:.4f}s")
    print(f"   🐍 Python Docker overhead: {python_overhead:.4f}s")
    print(f"   📊 Overhead difference: {abs(cpp_overhead - python_overhead):.4f}s")
    
    return {
        'cpp_overhead': cpp_overhead,
        'python_overhead': python_overhead,
        'overhead_difference': abs(cpp_overhead - python_overhead)
    }

def measure_algorithmic_performance_only():
    """Measure pure algorithmic performance without Docker overhead"""
    print("⚡ Measuring pure algorithmic performance...")
    
    # Use pre-compiled binaries approach
    cpp_times = []
    python_times = []
    
    # Complex computation to amplify algorithmic differences
    test_input = "1000000\n" + " ".join(str(i) for i in range(1, 1000001)) + "\n500000"
    
    cpp_code = '''
#include <iostream>
#include <vector>
#include <chrono>
using namespace std;
using namespace std::chrono;

int binarySearch(const vector<int>& arr, int target) {
    int left = 0;
    int right = arr.size() - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}

int main() {
    auto start = high_resolution_clock::now();
    
    int n;
    cin >> n;
    vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }
    int target;
    cin >> target;
    
    // Perform search multiple times to amplify differences
    int result = -1;
    for (int i = 0; i < 1000; i++) {
        result = binarySearch(arr, target);
    }
    
    auto end = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(end - start);
    
    cout << result << endl;
    cout << "Time: " << duration.count() << " microseconds" << endl;
    
    return 0;
}
'''
    
    python_code = '''
import time

def binary_search(arr, target):
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

start_time = time.perf_counter()

n = int(input())
arr = list(map(int, input().split()))
target = int(input())

# Perform search multiple times to amplify differences
result = -1
for i in range(1000):
    result = binary_search(arr, target)

end_time = time.perf_counter()
duration_microseconds = (end_time - start_time) * 1_000_000

print(result)
print(f"Time: {int(duration_microseconds)} microseconds")
'''
    
    print("   🔧 Testing C++ algorithmic performance...")
    for i in range(3):
        with tempfile.TemporaryDirectory() as temp_dir:
            source_file = os.path.join(temp_dir, 'solution.cpp')
            input_file = os.path.join(temp_dir, 'input.txt')
            
            with open(source_file, 'w') as f:
                f.write(cpp_code)
            with open(input_file, 'w') as f:
                f.write(test_input)
            
            result = subprocess.run([
                'docker', 'run', '--rm',
                '-v', f'{temp_dir}:/workspace',
                '--workdir', '/workspace',
                'adaptive-judge-cpp:latest',
                'bash', '-c', 'g++ -O2 -o solution solution.cpp && ./solution < input.txt'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) >= 2 and "Time:" in lines[1]:
                    time_str = lines[1].split(":")[1].strip().split()[0]
                    cpp_times.append(float(time_str))
                    print(f"      Run {i+1}: {time_str} microseconds")
    
    print("   🐍 Testing Python algorithmic performance...")
    for i in range(3):
        with tempfile.TemporaryDirectory() as temp_dir:
            source_file = os.path.join(temp_dir, 'solution.py')
            input_file = os.path.join(temp_dir, 'input.txt')
            
            with open(source_file, 'w') as f:
                f.write(python_code)
            with open(input_file, 'w') as f:
                f.write(test_input)
            
            result = subprocess.run([
                'docker', 'run', '--rm',
                '-v', f'{temp_dir}:/workspace',
                '--workdir', '/workspace',
                'adaptive-judge-python:latest',
                'bash', '-c', 'python solution.py < input.txt'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) >= 2 and "Time:" in lines[1]:
                    time_str = lines[1].split(":")[1].strip().split()[0]
                    python_times.append(float(time_str))
                    print(f"      Run {i+1}: {time_str} microseconds")
    
    if cpp_times and python_times:
        cpp_median = statistics.median(cpp_times)
        python_median = statistics.median(python_times)
        
        print(f"   📊 C++ algorithmic time: {cpp_median} microseconds")
        print(f"   📊 Python algorithmic time: {python_median} microseconds")
        print(f"   📈 Python/C++ ratio: {python_median/cpp_median:.3f}x")
        
        return {
            'cpp_algorithmic': cpp_median,
            'python_algorithmic': python_median,
            'algorithmic_ratio': python_median / cpp_median
        }
    
    return None

def run_refined_analysis():
    """Run refined analysis separating overhead from algorithmic performance"""
    print("🔬 REFINED COMPLEXITY ANALYSIS")
    print("=" * 70)
    print("Goal: Separate Docker overhead from algorithmic performance")
    print()
    
    # Measure overhead
    overhead_results = measure_docker_overhead()
    print()
    
    # Measure algorithmic performance
    algorithmic_results = measure_algorithmic_performance_only()
    print()
    
    if algorithmic_results:
        # Analysis
        print("📊 ANALYSIS:")
        print(f"   🏭 Total overhead difference: {overhead_results['overhead_difference']:.4f}s")
        print(f"   ⚡ Pure algorithmic ratio: {algorithmic_results['algorithmic_ratio']:.3f}x")
        print()
        
        if algorithmic_results['algorithmic_ratio'] > 1.0:
            print("✅ CONCLUSION: When overhead is removed, C++ is faster algorithmically")
            print(f"   📈 C++ algorithmic advantage: {1/algorithmic_results['algorithmic_ratio']:.3f}x")
        else:
            print("🤔 CONCLUSION: Python is still faster even without overhead")
        
        # Save refined results
        results = {
            'timestamp': datetime.now().isoformat(),
            'analysis_type': 'refined_overhead_separation',
            'overhead': overhead_results,
            'algorithmic': algorithmic_results,
            'conclusion': {
                'overhead_explains_difference': algorithmic_results['algorithmic_ratio'] > 1.0,
                'true_algorithmic_winner': 'cpp' if algorithmic_results['algorithmic_ratio'] > 1.0 else 'python'
            }
        }
        
        with open('complexity_analysis/refined_analysis.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📄 Refined analysis saved to: complexity_analysis/refined_analysis.json")
        return results
    
    return None

if __name__ == "__main__":
    try:
        results = run_refined_analysis()
        if results:
            print(f"\n🎯 REFINED SCIENTIFIC CONCLUSION:")
            if results['conclusion']['overhead_explains_difference']:
                print(f"   Docker overhead was masking C++'s algorithmic advantage!")
                print(f"   True performance: C++ is {1/results['algorithmic']['algorithmic_ratio']:.2f}x faster")
            else:
                print(f"   Python is genuinely faster even without overhead!")
        
    except Exception as e:
        print(f"\n❌ Refined analysis failed: {e}")
        import traceback
        traceback.print_exc()
