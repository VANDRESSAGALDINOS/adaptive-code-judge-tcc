# Validation Report: O2n_exponential

## Experiment Overview

**Complexity Class**: O2n_exponential
**Date**: 2025-08-23T16:50:48.285476
**Problem**: Subset Sum (O(2ⁿ))

## Benchmark Results

### Performance Measurements
- **C++ Median Time**: 0.3434s
- **Python Median Time**: 0.4798s
- **Python/C++ Ratio**: 1.397x
- **Reliability**: ✅ High

### Calibrated Time Limits
- **C++ Limit**: 0.687s (2x median)
- **Python Limit**: 0.960s (2x median)

## Time Limit Validation

### Optimal Solutions (Should PASS)

**CPP**: 0.364s → PASS ✅ PASS

**PYTHON**: 0.491s → PASS ✅ PASS


### Slow Solutions (Should TLE)

**CPP**: 1.128s → TLE ✅ TLE

**PYTHON**: 1.136s → TLE ✅ TLE


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
    "execution_time": 0.363753080368042,
    "expected_result": "PASS",
    "actual_result": "PASS",
    "correct": true
  },
  "python": {
    "passed": true,
    "execution_time": 0.4914281368255615,
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
    "execution_time": 1.1280388832092285,
    "expected_result": "TLE",
    "actual_result": "TLE",
    "correct": true
  },
  "python": {
    "timed_out": true,
    "execution_time": 1.1356158256530762,
    "expected_result": "TLE",
    "actual_result": "TLE",
    "correct": true
  }
}
```

---
*Validation report generated automatically*
