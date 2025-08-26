# Comprehensive Experiment Plan - Shortest Routes II (CSES 1672)

## Experiment Overview

### Primary Objective
Demonstrate empirically that Python suffers unfair penalty in traditional online judges compared to C++ for algorithmically equivalent solutions, and validate that adaptive time limits restore fairness while preserving algorithmic selectivity.

### Research Questions
1. **Injustice Quantification**: How much does Python underperform vs C++ on CSES 1672?
2. **Adaptive Solution Effectiveness**: Can calibrated time limits achieve fair evaluation without compromising rigor?
3. **Selectivity Preservation**: Do adaptive limits maintain distinction between efficient and inefficient algorithms?
4. **Cross-Platform Consistency**: Does our local system accurately replicate CSES behavior?

## Experimental Design

### Phase 1: Implementation Development
- [x] Implement C++ solution (Floyd-Warshall O(n³))
- [x] Implement Python solution (algorithmically identical)
- [x] Verify correctness on CSES platform ([C++ ACCEPTED #14297533](https://cses.fi/problemset/result/14297533/))
- [x] Ensure formal algorithmic equivalence (see `formal_proof.md`)
- [x] Implement deliberately slow solutions for TLE validation
- [x] Verify slow solutions receive TLE on CSES ([C++ #14298232](https://cses.fi/problemset/result/14298232/), [Python #14298238](https://cses.fi/problemset/result/14298238/))

### Phase 2: Test Case Acquisition and Analysis
- [x] Download official CSES test cases for problem 1672 (16 cases)
- [x] Categorize by criticality:
  - **Critical Cases** (TLE in Python): #6-12, #14-15 (9 cases)
  - **Control Cases** (ACCEPTED in Python): #1-5, #13, #16 (7 cases)
- [x] Identify primary benchmark case: **Test #8** (n=500, m=500, q=100k)
- [x] Select validation cases: #12 (high density), #15 (max density)

### Phase 3: Controlled Benchmarking Protocol

#### Environment Setup
```bash
# C++ Environment
docker run --rm --cpus="1.0" --memory="512m" \
  -v $(pwd):/workspace -w /workspace debian:stable-slim bash -c "
  apt-get update && apt-get install -y g++ time
  g++ -O3 -march=native -pipe -o solution_cpp solutions/solution.cpp
"

# Python Environment  
docker run --rm --cpus="1.0" --memory="512m" \
  -v $(pwd):/workspace -w /workspace python:3.11-slim bash -c "
  python3 solutions/solution.py
"
```

#### Benchmark Execution (Calibration - Test Case #8)
```bash
# Primary calibration using largest critical case
CASE_ID=8
REPETITIONS=30

for i in {1..${REPETITIONS}}; do
  echo "Calibration run $i"
  
  # C++ execution
  timeout 2s /usr/bin/time -f "%e" ./solution_cpp < tests_cses/${CASE_ID}.in \
    > results/cpp_${CASE_ID}_${i}.out 2> results/cpp_${CASE_ID}_${i}.time
  
  # Python execution
  timeout 2s /usr/bin/time -f "%e" python3 solutions/solution.py < tests_cses/${CASE_ID}.in \
    > results/py_${CASE_ID}_${i}.out 2> results/py_${CASE_ID}_${i}.time
done
```

#### Validation Execution (All Test Cases)
```bash
# Traditional system simulation (1.0s limit)
# Adaptive system simulation (calibrated limits)
for case_id in {1..16}; do
  for lang in cpp python; do
    for i in {1..10}; do  # Fewer repetitions for validation
      # Execute with appropriate time limits
      # Record success/failure status
    done
  done
done
```

## Comprehensive Metrics Collection

### Phase 1 Metrics: Benchmark Calibration (Test Case #8)

#### Performance Statistics
```python
calibration_metrics = {
    'cpp': {
        'median_time': float,           # Median execution time (s)
        'p90_time': float,              # 90th percentile (s)
        'iqr': float,                   # Interquartile range (s)
        'coefficient_variation': float,  # IQR/median
        'reliable': bool                # cv < 0.15
    },
    'python': {
        'median_time': float,           # Median execution time (s)
        'p90_time': float,              # 90th percentile (s)
        'iqr': float,                   # Interquartile range (s)
        'coefficient_variation': float,  # IQR/median
        'reliable': bool                # cv < 0.20
    }
}
```

#### Adjustment Factor Calculation
```python
adjustment_metrics = {
    'adjustment_factor': float,         # median_py / median_cpp
    'adaptive_limit_python': float,     # 1.0 * adjustment_factor
    'slowdown_percentage': float,       # (factor - 1.0) * 100
    'calibration_valid': bool          # factor < 5.0 and both reliable
}
```

### Phase 2 Metrics: System Validation (All Test Cases)

#### Traditional System Performance
```python
traditional_results = {
    'cpp': {
        'total_cases': 16,
        'pass_count': int,              # Cases with status ACCEPTED
        'tle_count': int,               # Cases with status TLE
        'pass_rate': float,             # pass_count / total_cases * 100
        'tle_rate': float               # tle_count / total_cases * 100
    },
    'python': {
        'total_cases': 16,
        'pass_count': int,              # Expected: ~7 (control cases)
        'tle_count': int,               # Expected: ~9 (critical cases)
        'pass_rate': float,             # Expected: ~44%
        'tle_rate': float               # Expected: ~56%
    }
}
```

#### Adaptive System Performance
```python
adaptive_results = {
    'cpp': {
        'pass_count': int,              # Should equal traditional (no regression)
        'pass_rate': float              # Should maintain 100%
    },
    'python': {
        'pass_count': int,              # Expected: ~15-16 (major improvement)
        'tle_count': int,               # Expected: ~0-1 (major reduction)
        'pass_rate': float,             # Expected: ~94-100%
        'tle_rate': float               # Expected: ~0-6%
    }
}
```

### Critical Injustice Metrics (Zero-Division Safe)

#### Primary Metric: Absolute TLE Reduction
```python
injustice_correction = {
    'tle_reduction_absolute': float,    # traditional_py_tle_rate - adaptive_py_tle_rate
    'tle_reduction_cases': int,         # traditional_py_tle_count - adaptive_py_tle_count
    'cases_rescued': int,               # adaptive_py_pass_count - traditional_py_pass_count
    'injustice_eliminated': bool        # tle_reduction_absolute > 50.0
}
```

#### Secondary Metric: Performance Characterization
```python
performance_gap = {
    'speed_ratio': float,               # adjustment_factor
    'time_increase_needed': float,      # adaptive_limit_python - 1.0
    'critical_cases_affected': int      # Count of cases changed from TLE to ACCEPTED
}
```

### Segmented Analysis by Case Criticality

#### Critical Cases Analysis (TLE-prone)
```python
critical_cases = [6, 7, 8, 9, 10, 11, 12, 14, 15]
critical_analysis = {
    'traditional_python_success_rate': float,  # Expected: ~0%
    'adaptive_python_success_rate': float,     # Expected: ~95-100%
    'improvement_magnitude': float             # Dramatic improvement expected
}
```

#### Control Cases Analysis (Already passing)
```python
control_cases = [1, 2, 3, 4, 5, 13, 16]
control_analysis = {
    'traditional_python_success_rate': float,  # Expected: ~100%
    'adaptive_python_success_rate': float,     # Expected: ~100% (no change)
    'no_regression': bool                      # Verify no negative impact
}
```

### TLE Cross-Validation Metrics (Slow Solutions)

#### Selectivity Preservation Validation
```python
tle_validation = {
    'external_validation': {
        'cses_cpp_slow_status': 'TLE',         # Submission #14298232
        'cses_python_slow_status': 'TLE',      # Submission #14298238
        'no_wrong_answers': True               # Critical: TLE only, no WA
    },
    'local_traditional_validation': {
        'cpp_slow_status': 'TLE',              # Expected with 1.0s limit
        'python_slow_status': 'TLE'            # Expected with 1.0s limit
    },
    'local_adaptive_validation': {
        'cpp_slow_status': 'TLE',              # Expected with 1.0s limit (unchanged)
        'python_slow_status': 'TLE'            # Expected even with adaptive limit
    },
    'selectivity_preserved': bool              # Inefficient algorithms still rejected
}
```

## Explicit Success Criteria

### Calibration Phase Success
```python
calibration_success = {
    'reliability': (reliable_cpp and reliable_py),
    'reasonable_factor': (1.5 <= adjustment_factor <= 5.0),
    'statistical_power': (len(successful_runs) >= 20)  # At least 20/30 successful
}
```

### Validation Phase Success
```python
validation_success = {
    'injustice_demonstration': traditional_results['python']['tle_rate'] > 50.0,
    'injustice_correction': injustice_correction['tle_reduction_absolute'] > 50.0,
    'cpp_preservation': adaptive_results['cpp']['pass_rate'] >= traditional_results['cpp']['pass_rate'],
    'python_improvement': adaptive_results['python']['pass_rate'] > traditional_results['python']['pass_rate'],
    'correctness_maintained': count_wrong_answers == 0,
    'selectivity_preserved': tle_validation['selectivity_preserved']
}
```

### Overall Experiment Success
```python
experiment_success = all([
    calibration_success['reliability'],
    calibration_success['reasonable_factor'],
    validation_success['injustice_demonstration'],
    validation_success['injustice_correction'],
    validation_success['correctness_maintained'],
    validation_success['selectivity_preserved']
])
```

## Data Collection Schema

### Benchmark Data Structure
```json
{
  "experiment_metadata": {
    "problem_id": "cses_1672",
    "calibration_case": 8,
    "total_cases": 16,
    "execution_date": "2025-01-XX",
    "environment": "docker_controlled"
  },
  "calibration_results": {
    "test_case_8": {
      "cpp_executions": [0.456, 0.461, ...],
      "python_executions": [1.234, 1.267, ...],
      "cpp_statistics": {...},
      "python_statistics": {...},
      "adjustment_factor": 2.7
    }
  },
  "validation_results": {
    "traditional_system": {
      "cpp": {"pass_cases": [1,2,...,16], "tle_cases": []},
      "python": {"pass_cases": [1,2,3,4,5,13,16], "tle_cases": [6,7,8,9,10,11,12,14,15]}
    },
    "adaptive_system": {
      "cpp": {"pass_cases": [1,2,...,16], "tle_cases": []},
      "python": {"pass_cases": [1,2,...,15,16], "tle_cases": []}
    }
  }
}
```

## Statistical Analysis Protocol

### Descriptive Statistics
- **Central Tendency**: Median (robust to outliers)
- **Variability**: IQR, Coefficient of Variation
- **Distribution**: Percentiles (p90 for worst-case analysis)

### Reliability Assessment
- **C++ Threshold**: Coefficient of Variation < 15%
- **Python Threshold**: Coefficient of Variation < 20% (more tolerant)
- **Minimum Success Rate**: ≥50% successful executions

### Comparative Analysis
- **Effect Size**: Performance ratio (median_py / median_cpp)
- **Practical Significance**: Adjustment factor magnitude
- **Correctness Validation**: Output equivalence verification

## Risk Mitigation Strategies

### Technical Risks
- **Docker Overhead**: Consistent containerized environment, measure baseline overhead
- **System Interference**: Dedicated execution environment, resource isolation
- **Measurement Precision**: High-resolution timing, multiple repetitions
- **Timeout Handling**: Graceful timeout detection, status classification

### Methodological Risks
- **Implementation Bugs**: Formal proof of algorithmic equivalence
- **Cherry-picking**: Test all 16 official cases, segment by criticality
- **External Validity**: Cross-validation with actual CSES submissions
- **Regression Risks**: Verify no negative impact on control cases

### Statistical Risks
- **Multiple Comparisons**: Focus on primary hypotheses, clear success criteria
- **Sample Size**: Adequate repetitions for statistical power
- **Assumption Violations**: Use non-parametric methods when appropriate

## Implementation Timeline

### Phase 1: Setup and Calibration (2 days)
- [ ] Environment setup and validation
- [ ] Calibration execution (Test Case #8, 30 repetitions)
- [ ] Adjustment factor calculation
- [ ] Reliability assessment

### Phase 2: System Validation (2 days)
- [ ] Traditional system validation (all 16 cases, 10 repetitions)
- [ ] Adaptive system validation (all 16 cases, 10 repetitions)
- [ ] TLE cross-validation (slow solutions)
- [ ] Correctness verification

### Phase 3: Analysis and Documentation (1 day)
- [ ] Statistical analysis and metric calculation
- [ ] Success criteria evaluation
- [ ] Results documentation and visualization
- [ ] Integration with thesis framework

**Total Estimated Time**: 5 days

## Expected Results and Impact

### Quantitative Predictions
- **Adjustment Factor**: 2.5-3.0x (based on preliminary evidence)
- **TLE Reduction**: 56% → 6% (50+ percentage point improvement)
- **Cases Rescued**: 9 cases (from TLE to ACCEPTED)
- **Selectivity Maintained**: 100% (slow solutions remain TLE)

### Scientific Contributions
1. **Empirical Injustice Documentation**: First systematic quantification of language bias
2. **Adaptive Solution Validation**: Proof-of-concept for fair evaluation systems
3. **Cross-Platform Methodology**: Replicable framework for platform analysis
4. **Selectivity Preservation**: Demonstration that fairness doesn't compromise rigor

### Thesis Integration
- **Problem Statement**: Concrete evidence of systematic bias
- **Solution Validation**: Empirical proof of adaptive approach effectiveness  
- **Methodology**: Rigorous experimental framework for future research
- **Results**: Statistically robust findings with practical implications

---

**Plan Version**: 2.0 (Comprehensive)
**Created**: January 2025  
**Status**: Ready for execution  
**Validation**: Cross-platform verified with CSES submissions