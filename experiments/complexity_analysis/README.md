# Complexity Analysis Experiments

## Overview
Scientific experiments to validate the thesis claim: **"Python and C++ behave similarly in simple problems, but diverge significantly in recursive/complex patterns — justifying adaptive time limits per language."**

## Methodology
- **Framework**: Uses existing MVP services (ProblemService, BenchmarkService)
- **Execution**: Docker-based isolated environments
- **Metrics**: Execution time, memory usage, IQR stability analysis
- **Repetitions**: 10 runs per language/problem for statistical significance

## Experiment Design

### Complexity Classes Tested

| Class | Problem Type | Expected Divergence | Justification |
|-------|--------------|-------------------|---------------|
| **O(1)** | Arithmetic Operations | Minimal (1.1-1.3x) | Simple operations, no algorithmic complexity |
| **O(log n)** | Binary Search | Low (1.3-1.8x) | Efficient algorithms, minimal Python overhead |
| **O(n)** | Linear Search | Moderate (1.8-2.5x) | Loop iteration differences |
| **O(n log n)** | Merge Sort | High (2.5-4.0x) | Recursion + complex operations |
| **O(n²)** | Bubble Sort | Very High (4.0-8.0x) | Nested loops, significant overhead |

### Expected vs Observed Results

#### Initial Hypothesis (REFUTED)
```
Performance Gap (Python/C++):
O(1)      ████ 1.2x (Python slower)
O(log n)  ██████ 1.5x (Python slower)
```

#### Observed Results (SURPRISING)
```
Performance Gap (Python/C++):
O(1)      ███ 0.63x (Python FASTER)
O(log n)  ███ 0.59x (Python FASTER)
```

## Running Experiments

### Prerequisites
- Docker environment set up
- MVP system running
- Reference solutions placed in `reference_solutions/` folders

### Execute Experiments

#### Real-World Performance (Includes Docker overhead)
```bash
cd experiments/
python run_experiment_direct.py O1_constant
python run_experiment_direct.py O_log_n
```

#### Refined Analysis (Separates overhead from algorithmic performance)
```bash
cd experiments/
python run_experiment_refined.py
```

#### Both Approaches (Recommended for complete analysis)
```bash
# Real-world first
python run_experiment_direct.py O1_constant
python run_experiment_direct.py O_log_n

# Then refined analysis
python run_experiment_refined.py
```

## Results Structure

Each experiment generates:
- **`results.json`**: Raw performance data
- **`analysis.md`**: Statistical interpretation
- **Database records**: Problems, test cases, benchmarks

### Sample Results Format
```json
{
  "experiment": "O1_constant",
  "timestamp": "2025-01-23T15:30:00",
  "benchmark": {
    "cpp_base_time": 0.045,
    "python_factor": 1.23,
    "is_reliable": true,
    "repetitions": 10
  }
}
```

## Scientific Validity

### Statistical Rigor
- **Confidence**: 95% (10 repetitions minimum)
- **Stability**: IQR < 15% for reliable benchmarks
- **Controls**: Same hardware, Docker isolation
- **Reproducibility**: All code and data versioned

### Hypothesis Testing
- **H₀**: Performance ratio is constant across complexity classes
- **H₁**: Performance ratio increases with algorithmic complexity
- **Test**: ANOVA + post-hoc analysis

## TCC Integration

### Chapter 5: Results and Analysis
Use these experiments to demonstrate:
1. **Empirical validation** of adaptive time limits
2. **Quantitative evidence** for language-specific factors
3. **Scientific methodology** in system design
4. **Performance characterization** across complexity classes

### Academic Contributions
- **Novel benchmarking methodology** for multi-language judges
- **Adaptive algorithm** based on complexity analysis
- **Empirical performance model** for C++/Python comparison

---
*Experiments conducted as part of the Adaptive Code Judge thesis project*
