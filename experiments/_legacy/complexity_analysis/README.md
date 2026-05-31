# Complexity Analysis Framework

## Research Objective

This framework investigates performance characteristics of programming languages across algorithmic complexity classes in containerized environments. The research tests the hypothesis that language-specific performance patterns justify adaptive time limit allocation in automated code evaluation systems.

## Methodology

### Experimental Protocol
- **Execution Environment**: Docker containerization for process isolation
- **Statistical Framework**: 10 independent trials per language/algorithm combination
- **Reliability Criterion**: Interquartile Range (IQR) < 15% of median execution time
- **Performance Metric**: Median execution time (robust against outliers)

### Complexity Classes Under Investigation

| Class | Algorithm | Theoretical Complexity | Research Focus |
|-------|-----------|----------------------|----------------|
| **O(1)** | Arithmetic Operations | Constant time | Baseline overhead analysis |
| **O(log n)** | Binary Search | Logarithmic | Minimal algorithmic divergence |
| **O(n)** | Array Sum | Linear | Moderate complexity impact |
| **O(n²)** | Matrix Sum | Quadratic | Significant algorithmic differences |
| **O(n³)** | Matrix Multiplication | Cubic | High complexity performance gaps |
| **O(2ⁿ)** | Subset Sum | Exponential | Maximum performance variance |

### Empirical Results

#### Performance Ratios (Python/C++)

| Complexity | Observed Ratio | Statistical Significance |
|------------|---------------|-------------------------|
| **O(1)** | 0.626 | p < 0.001 (37.4% faster) |
| **O(log n)** | 0.594 | p < 0.001 (40.6% faster) |

**Key Finding**: Python demonstrates consistent performance advantages over C++ in containerized environments for low-complexity algorithms, contradicting conventional performance assumptions.

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
