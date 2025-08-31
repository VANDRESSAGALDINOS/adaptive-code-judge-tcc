# Next Steps: CSES 1197 Implementation Guide

## Implementation Status
- ✅ Problem analysis completed
- ✅ Algorithmic equivalence proven
- ✅ Solutions implemented (C++ and Python)
- ✅ Slow solutions created for validation
- ✅ Test cases acquired (27 official CSES cases)
- ✅ Experimental framework ready

## Execution Plan

### Phase 1: Calibration
Execute calibration using largest test case to derive adjustment factor:
```bash
python3 run_benchmark.py --phase=calibration --case=10 --repetitions=30
```

### Phase 2: Validation
Test strategic cases to demonstrate injustice correction:
```bash
python3 run_benchmark.py --phase=validation --cases=1,10,13,15,20,25,27 --repetitions=10
```

### Phase 3: Selectivity Validation
Verify slow solutions fail in both systems:
```bash
python3 validate_slow_solutions.py --cases=10,13,27
```

### Complete Experiment
Run full automated experiment:
```bash
python3 run_complete_experiment.py
```

## Expected Results

### Calibration Predictions
- **C++ median time**: 0.05-0.15s for large cases
- **Python median time**: 0.20-0.80s for large cases  
- **Adjustment factor**: 4x-8x (moderate compared to Floyd-Warshall)
- **Reliability**: Both languages should meet IQR thresholds

### Validation Predictions
- **Traditional system**: Python TLE rate ~37% (10/27 cases)
- **Adaptive system**: Python success rate >95%
- **C++ performance**: Unchanged between systems
- **Overall improvement**: 30+ percentage point TLE reduction

### Key Test Cases
- **Small cases (1-5)**: Both languages should pass
- **Medium cases (10-15)**: Mixed results, some Python TLE
- **Large cases (20-27)**: Clear Python disadvantage in traditional system

## Success Criteria
1. Calibration produces stable adjustment factor (4x-8x range)
2. Clear injustice demonstrated in traditional system
3. Adaptive system rescues Python without C++ regression
4. Slow solutions maintain TLE in both systems
5. Statistical significance in performance differences

## Post-Execution Analysis
After completion, run automated analysis:
```bash
python3 ../AUTO_CHECKLIST.py problem02/
```

This will generate:
- `metadata_graficos.json` for final notebook
- `RESUMO_AUTO_ANALISE.md` with classification
- Validation of all success criteria

## Integration with TCC Framework
Results will automatically integrate with the final analysis notebook, contributing to:
- Executive graph of adjustment factors by category
- Heatmap of injustice patterns
- Comparative analysis with other algorithm types
- Evidence against fixed adjustment factors

