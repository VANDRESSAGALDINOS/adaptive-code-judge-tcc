# Validation Report: On_linear

## Experiment Overview

**Complexity Class**: On_linear
**Date**: 2025-08-23T16:38:40.774025
**Problem**: Array Sum (O(n))

## Benchmark Results

### Performance Measurements
- **C++ Median Time**: 0.4406s
- **Python Median Time**: 0.2793s
- **Python/C++ Ratio**: 0.634x
- **Reliability**: ✅ High

### Calibrated Time Limits
- **C++ Limit**: 0.881s (2x median)
- **Python Limit**: 0.559s (2x median)

## Time Limit Validation

### Optimal Solutions (Should PASS)

**CPP**: 0.436s → PASS ✅ PASS

**PYTHON**: 0.284s → PASS ✅ PASS


### Slow Solutions (Should TLE)

**CPP**: 1.208s → TLE ✅ TLE

**PYTHON**: 0.738s → TLE ✅ TLE


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
    "execution_time": 0.43638014793395996,
    "expected_result": "PASS",
    "actual_result": "PASS",
    "correct": true
  },
  "python": {
    "passed": true,
    "execution_time": 0.2835807800292969,
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
    "execution_time": 1.20759916305542,
    "expected_result": "TLE",
    "actual_result": "TLE",
    "correct": true
  },
  "python": {
    "timed_out": true,
    "execution_time": 0.7382040023803711,
    "expected_result": "TLE",
    "actual_result": "TLE",
    "correct": true
  }
}
```

---
*Validation report generated automatically*
