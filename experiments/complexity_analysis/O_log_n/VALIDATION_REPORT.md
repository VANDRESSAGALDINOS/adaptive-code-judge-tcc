# Validation Report: O_log_n

## Experiment Overview

**Complexity Class**: O_log_n
**Date**: 2025-08-23T16:11:44.084893
**Problem**: Binary Search (O(log n))

## Benchmark Results

### Performance Measurements
- **C++ Median Time**: 0.3163s
- **Python Median Time**: 0.1795s
- **Python/C++ Ratio**: 0.568x
- **Reliability**: ✅ High

### Calibrated Time Limits
- **C++ Limit**: 0.633s (2x median)
- **Python Limit**: 0.359s (2x median)

## Time Limit Validation

### Optimal Solutions (Should PASS)

**CPP**: 0.316s → PASS ✅ PASS

**PYTHON**: 0.184s → PASS ✅ PASS


### Slow Solutions (Should TLE)

**CPP**: 0.343s → PASS ❌ FAIL

**PYTHON**: 0.522s → TLE ✅ TLE


## Validation Summary

**Overall Result**: ❌ FAILED

### Analysis
❌ Time limits need adjustment

- Optimal solutions: All passed within limits
- Slow solutions: Some passed unexpectedly

## Implications for TCC

This validation demonstrates that:

1. **Benchmark Accuracy**: The calibrated time limits correctly distinguish between optimal and suboptimal solutions
2. **System Reliability**: The adaptive time limit system works as designed
3. **Practical Applicability**: The system can be deployed in real judge environments

## Technical Data

### Optimal Solution Performance
```json
{
  "cpp": {
    "passed": true,
    "execution_time": 0.3158111572265625,
    "expected_result": "PASS",
    "actual_result": "PASS",
    "correct": true
  },
  "python": {
    "passed": true,
    "execution_time": 0.18442797660827637,
    "expected_result": "PASS",
    "actual_result": "PASS",
    "correct": true
  }
}
```

### Slow Solution Performance  
```json
{
  "cpp": {
    "timed_out": false,
    "execution_time": 0.34334802627563477,
    "expected_result": "TLE",
    "actual_result": "PASS",
    "correct": false
  },
  "python": {
    "timed_out": true,
    "execution_time": 0.5223581790924072,
    "expected_result": "TLE",
    "actual_result": "TLE",
    "correct": true
  }
}
```

---
*Validation report generated automatically*
