# CSES 1672 Experiment Execution Guide

## Quick Start

Execute the complete experiment with a single command:

```bash
python3 run_complete_experiment.py
```

This will run all phases automatically following the `experiment_plan.md` protocol.

## Manual Execution (Step by Step)

### Prerequisites Check

Ensure you have:
- Docker installed and running
- Python 3.6+
- All solution files in `solutions/` and `slow_validation/solutions_slow/`
- All 16 test cases in `tests_cses/`

### Phase 1: Calibration

```bash
# Run calibration on test case #8 with 30 repetitions
python3 run_benchmark.py --phase=calibration --case=8 --repetitions=30
```

**Expected output:**
- `results/calibration_case8.json`
- Adjustment factor calculation (expected: 2.5-3.0x)

### Phase 2: Validation

```bash
# Run validation on all 16 test cases with 10 repetitions each
python3 run_benchmark.py --phase=validation --repetitions=10
```

**Expected output:**
- `results/validation_results.json`
- Success/failure rates for traditional vs adaptive systems

### Phase 3: Slow Solution Validation

```bash
# Validate that slow solutions still receive TLE
python3 validate_slow_solutions.py --cases=8,15
```

**Expected output:**
- `results/slow_solution_validation.json`
- Confirmation that selectivity is preserved

### Phase 4: Analysis

```bash
# Generate comprehensive analysis report
python3 analyze_results.py --input=results --output=final_report.json
```

**Expected output:**
- `final_report.json`
- Executive summary and success evaluation

## Expected Results

### Successful Experiment Indicators

1. **Calibration Reliable**: 
   - C++ and Python both have low variability (IQR < 15%/20%)
   - Adjustment factor in reasonable range (1.5-5.0x)

2. **Injustice Demonstrated**:
   - Traditional system: Python success rate < 60%
   - Clear performance gap between C++ and Python

3. **Injustice Corrected**:
   - Adaptive system: Python success rate > 90%
   - TLE reduction > 30 percentage points
   - Multiple cases rescued from TLE to ACCEPTED

4. **Selectivity Preserved**:
   - Slow solutions receive TLE in both systems
   - No gaming of the adaptive limits possible

### Sample Success Output

```
📊 OVERALL RESULTS:
  Traditional: C++ 100.0%, Python 43.8% (gap: 56.2%)
  Adaptive:    C++ 100.0%, Python 100.0% (gap: 0.0%)
  Python improvement: +56.2%
  Cases rescued: 9

⚖️ INJUSTICE CORRECTION METRICS:
  Traditional Python success: 43.8%
  Adaptive Python success: 100.0%
  Absolute TLE reduction: +56.2%
  Cases rescued: 9
  Injustice eliminated: ✓
  Fairness achieved: ✓

✅ EXPERIMENT STATUS: SUCCESSFUL
```

## Troubleshooting

### Common Issues

1. **Docker not available**
   ```bash
   sudo systemctl start docker
   # or
   sudo service docker start
   ```

2. **Permission denied**
   ```bash
   chmod +x *.py
   ```

3. **Missing test cases**
   - Ensure all files from `1.in`/`1.out` to `16.in`/`16.out` exist in `tests_cses/`

4. **Calibration fails**
   - Check that solutions are correct and produce expected output
   - Verify Docker images can be pulled
   - Increase time limits if needed

5. **Validation shows unexpected results**
   - Review solution implementations for correctness
   - Check test case integrity
   - Verify Docker environment consistency

### Debug Mode

For detailed debugging, run individual components:

```bash
# Test single case execution
python3 -c "
from run_benchmark import CSES1672Benchmark
b = CSES1672Benchmark()
result = b.execute_solution('solutions/solution.py', 1, 'python', 5.0)
print(result)
"
```

## File Structure

```
experiments_realworld/graphs/problem01/
├── README_EXECUTION.md          # This file
├── experiment_plan.md           # Scientific protocol
├── NEXT_STEPS.md               # Implementation guide
├── run_complete_experiment.py   # Main execution script
├── run_benchmark.py            # Benchmark execution
├── analyze_results.py          # Results analysis
├── validate_slow_solutions.py  # Selectivity validation
├── solutions/
│   ├── solution.cpp            # Optimal C++ solution
│   └── solution.py             # Optimal Python solution
├── slow_validation/solutions_slow/
│   ├── slow_solution.cpp       # Deliberately slow C++
│   └── slow_solution.py        # Deliberately slow Python
├── tests_cses/
│   ├── 1.in, 1.out, ..., 16.in, 16.out  # Official test cases
└── results/                    # Generated results
    ├── calibration_case8.json
    ├── validation_results.json
    ├── slow_solution_validation.json
    └── final_report.json
```

## Scientific Validity

This experiment follows rigorous scientific protocols:

1. **External Validation**: Results cross-validated with actual CSES submissions
2. **Controlled Environment**: Docker ensures consistent execution environment
3. **Statistical Rigor**: Multiple repetitions with proper statistical analysis
4. **Bias Elimination**: Testing all 16 cases prevents cherry-picking
5. **Selectivity Verification**: Slow solutions validate system integrity

## TCC Integration

Upon successful completion, the `final_report.json` contains all data needed for TCC:

- Empirical evidence of language bias
- Quantified injustice metrics
- Validation of adaptive solution
- Proof of selectivity preservation
- Statistical analysis and confidence measures

Use the executive summary from the final report for thesis defense preparation.

