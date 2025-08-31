# Experiment Plan: CSES 1197 - Cycle Finding

## Objective
Validate the adaptive time limit system for Bellman-Ford negative cycle detection, demonstrating correction of language-based injustice while preserving algorithmic selectivity.

## Problem Characteristics
- **Algorithm**: Bellman-Ford negative cycle detection
- **Complexity**: O(nm) where n ≤ 2500, m ≤ 5000
- **Platform**: CSES Problem 1197
- **Known Bias**: Python TLE in 10/27 test cases (37% failure rate)

## Experimental Design

### Phase 1: Calibration Protocol
**Objective**: Derive empirical adjustment factor through controlled benchmarking

**Method**:
- **Test Case Selection**: Largest available test case (highest n,m values)
- **Repetitions**: 30 executions per language
- **Measurement**: Wall-clock execution time using Docker isolation
- **Environment**: 
  - C++: `gcc:latest` with `-O3` optimization
  - Python: `python:3.11-slim` with CPython interpreter

**Success Criteria**:
- C++ IQR < 15% (stable performance)
- Python IQR < 20% (acceptable variability)
- Adjustment factor between 1.5x and 50x (realistic range)

### Phase 2: Validation Protocol
**Objective**: Demonstrate injustice correction across representative test cases

**Method**:
- **Test Case Selection**: Strategic sampling of CSES test cases
  - Small cases (expected PASS for both languages)
  - Large cases (expected Python TLE in traditional system)
- **Systems Tested**:
  - Traditional: Fixed 1.0s limit for both languages
  - Adaptive: 1.0s for C++, (adjustment_factor × 1.0s) for Python
- **Repetitions**: 10 executions per case per language per system

**Success Criteria**:
- Traditional system shows clear Python disadvantage
- Adaptive system achieves Python success rate > 95%
- C++ performance unchanged between systems
- Overall TLE reduction > 30 percentage points

### Phase 3: Selectivity Validation
**Objective**: Confirm that inefficient algorithms still fail under adaptive limits

**Method**:
- **Slow Solutions**: Artificially inefficient Bellman-Ford implementations
- **Test Cases**: Same cases used in Phase 2
- **Validation**: Slow solutions must TLE in both traditional and adaptive systems

**Success Criteria**:
- Slow C++ solution: TLE in both systems
- Slow Python solution: TLE in both systems (even with extended limit)
- Selectivity preservation rate = 100%

## Data Collection Schema

### Calibration Metrics
```json
{
  "cpp_times": [float],
  "python_times": [float], 
  "cpp_median": float,
  "python_median": float,
  "adjustment_factor": float,
  "cpp_iqr": float,
  "python_iqr": float,
  "reliability": boolean
}
```

### Validation Metrics
```json
{
  "traditional_system": {
    "cpp_success_rate": float,
    "python_success_rate": float
  },
  "adaptive_system": {
    "cpp_success_rate": float,
    "python_success_rate": float
  },
  "improvement_metrics": {
    "tle_reduction": float,
    "cases_rescued": int,
    "cpp_regression": float
  }
}
```

## Statistical Analysis Protocol

### Descriptive Statistics
- Median execution times (robust against outliers)
- Interquartile range (IQR) for stability assessment
- Success rate percentages for each system

### Reliability Assessment
- Coefficient of variation for timing stability
- Confidence intervals for adjustment factor
- Statistical significance of performance differences

### Comparative Analysis
- Traditional vs adaptive system performance
- Language gap quantification
- Correlation with CSES empirical data

## Risk Mitigation

### Technical Risks
- **Docker overhead**: Controlled through consistent environment
- **System variability**: Multiple repetitions and statistical analysis
- **Compiler optimizations**: Standardized build flags

### Methodological Risks
- **Cherry-picking bias**: Systematic test case selection
- **Sample size**: Adequate repetitions for statistical validity
- **Measurement precision**: Docker isolation and timing methodology

## Expected Outcomes

### Primary Hypothesis
Adaptive time limits will reduce Python TLE rate from ~37% to <5% while maintaining C++ performance and algorithmic selectivity.

### Secondary Hypotheses
- Adjustment factor will be in range 4x-8x (moderate compared to Floyd-Warshall)
- Bellman-Ford shows less extreme bias than matrix-based algorithms
- Loop-intensive algorithms demonstrate consistent interpreter overhead patterns

## Timeline
- **Setup and Implementation**: 2 hours
- **Calibration Execution**: 30 minutes
- **Validation Execution**: 45 minutes
- **Analysis and Documentation**: 1 hour
- **Total Duration**: ~4 hours

## Success Criteria Summary
1. **Calibration Reliable**: IQR thresholds met
2. **Injustice Demonstrated**: Clear Python disadvantage in traditional system
3. **Injustice Corrected**: Python success rate >95% in adaptive system
4. **C++ Preserved**: No performance regression
5. **Selectivity Maintained**: Slow solutions fail in both systems
6. **Statistical Validity**: Adequate sample sizes and significance levels

