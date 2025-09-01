# CSES 1750 - Python Submission Results

## Submission Details
- **Task**: Planets Queries I
- **Sender**: dressa
- **Submission time**: 2025-08-31 05:08:00 +0300
- **Language**: Python3 (CPython3)
- **Status**: READY
- **Result**: TIME LIMIT EXCEEDED
- **Code Link**: https://cses.fi/paste/3217da14abbf4b85db25c0/

## Test Results Summary
- **Total Cases**: 14
- **Passed**: 8/14 (57.1%)
- **Failed (TLE)**: 6/14 (42.9%)
- **Max Time**: 0.26s (case 14)
- **Min Time**: 0.02s (cases 1,2,3,4,5,11,13)

## Detailed Results
| Test | Verdict | Time | C++ Time | Status Comparison |
|------|---------|------|----------|-------------------|
| #1   | ACCEPTED | 0.02s | 0.00s | ✅ Both Pass |
| #2   | ACCEPTED | 0.02s | 0.00s | ✅ Both Pass |
| #3   | ACCEPTED | 0.02s | 0.00s | ✅ Both Pass |
| #4   | ACCEPTED | 0.02s | 0.00s | ✅ Both Pass |
| #5   | ACCEPTED | 0.02s | 0.00s | ✅ Both Pass |
| #6   | **TIME LIMIT EXCEEDED** | -- | 0.23s | ❌ **INJUSTICE** |
| #7   | **TIME LIMIT EXCEEDED** | -- | 0.21s | ❌ **INJUSTICE** |
| #8   | **TIME LIMIT EXCEEDED** | -- | 0.61s | ❌ **INJUSTICE** |
| #9   | **TIME LIMIT EXCEEDED** | -- | 0.38s | ❌ **INJUSTICE** |
| #10  | **TIME LIMIT EXCEEDED** | -- | 0.35s | ❌ **INJUSTICE** |
| #11  | ACCEPTED | 0.02s | 0.00s | ✅ Both Pass |
| #12  | **TIME LIMIT EXCEEDED** | -- | 0.99s | ❌ **INJUSTICE** |
| #13  | ACCEPTED | 0.02s | 0.00s | ✅ Both Pass |
| #14  | ACCEPTED | 0.26s | 0.02s | ✅ Both Pass |

## Binary Verdict Analysis
- **C++ Traditional**: ACCEPTED (14/14 cases passed)
- **Python Traditional**: REJECTED (6/14 cases TLE)
- **Injustice Detected**: ✅ **CONFIRMED**
- **Critical Cases**: 6, 7, 8, 9, 10, 12

## Performance Analysis
- **TLE Cases**: 6 out of 14 (42.9% failure rate)
- **Perfect Prediction**: Cases 8, 12 TLE as expected (C++ 0.61s, 0.99s)
- **Surprising TLEs**: Cases 6, 7, 9, 10 (C++ 0.21-0.38s range)
- **Algorithm Sensitivity**: Binary lifting severely penalizes Python

## Key Insights
1. **Severe Injustice Confirmed**: 42.9% of cases fail in Python vs 100% success in C++
2. **Algorithmic Complexity Validation**: Binary lifting creates massive performance gap
3. **Critical Case 12**: C++ barely passes (0.99s), Python fails completely
4. **Pattern Confirmation**: Recursive/simulation algorithms show extreme language bias

## Expected Adaptive Benchmark Results
- **Adjustment Factor Prediction**: >15x (based on TLE pattern)
- **Python Rescue Potential**: High (algorithmic equivalence confirmed)
- **Selectivity Preservation**: Expected (slow solutions should still TLE)