# Validation Report: On3_cubic

## Experiment Overview

**Complexity Class**: On3_cubic
**Date**: 2025-08-23T16:47:56.255647
**Problem**: Matrix Multiplication (O(n³))

## Benchmark Results

### Performance Measurements
- **C++ Median Time**: 0.3959s
- **Python Median Time**: 1.2957s
- **Python/C++ Ratio**: 3.273x
- **Reliability**: ✅ High

### Calibrated Time Limits
- **C++ Limit**: 0.792s (2x median)
- **Python Limit**: 2.591s (2x median)

## Time Limit Validation

### Optimal Solutions (Should PASS)

**CPP**: 0.410s → PASS ✅ PASS

**PYTHON**: 1.289s → PASS ✅ PASS


### Slow Solutions (Should TLE)

**CPP**: 1.189s → TLE ✅ TLE

**PYTHON**: 2.770s → TLE ✅ TLE


## Validation Summary

**Overall Result**: ✅ SUCCESS

### Analysis
✅ Time limits are properly calibrated

- Optimal solutions: All passed within limits
- Slow solutions: All properly timed out

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
    "execution_time": 0.41049885749816895,
    "expected_result": "PASS",
    "actual_result": "PASS",
    "correct": true
  },
  "python": {
    "passed": true,
    "execution_time": 1.289027214050293,
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
    "timed_out": true,
    "execution_time": 1.1892971992492676,
    "expected_result": "TLE",
    "actual_result": "TLE",
    "correct": true
  },
  "python": {
    "timed_out": true,
    "execution_time": 2.770146131515503,
    "expected_result": "TLE",
    "actual_result": "TLE",
    "correct": true
  }
}
```

---
*Validation report generated automatically*
