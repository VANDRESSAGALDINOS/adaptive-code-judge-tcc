# Validation Report: On2_quadratic

## Experiment Overview

**Complexity Class**: On2_quadratic
**Date**: 2025-08-23T16:39:34.080392
**Problem**: Matrix Sum (O(n²))

## Benchmark Results

### Performance Measurements
- **C++ Median Time**: 0.3890s
- **Python Median Time**: 0.2573s
- **Python/C++ Ratio**: 0.661x
- **Reliability**: ✅ High

### Calibrated Time Limits
- **C++ Limit**: 0.778s (2x median)
- **Python Limit**: 0.515s (2x median)

## Time Limit Validation

### Optimal Solutions (Should PASS)

**CPP**: 0.389s → PASS ✅ PASS

**PYTHON**: 0.266s → PASS ✅ PASS


### Slow Solutions (Should TLE)

**CPP**: 0.989s → TLE ✅ TLE

**PYTHON**: 0.693s → TLE ✅ TLE


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
    "execution_time": 0.38852524757385254,
    "expected_result": "PASS",
    "actual_result": "PASS",
    "correct": true
  },
  "python": {
    "passed": true,
    "execution_time": 0.2656707763671875,
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
    "execution_time": 0.9891250133514404,
    "expected_result": "TLE",
    "actual_result": "TLE",
    "correct": true
  },
  "python": {
    "timed_out": true,
    "execution_time": 0.6931860446929932,
    "expected_result": "TLE",
    "actual_result": "TLE",
    "correct": true
  }
}
```

---
*Validation report generated automatically*
