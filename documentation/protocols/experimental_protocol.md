# General Experimental Protocol

## Overview

This protocol standardizes the execution of experiments for detecting linguistic bias in online judge systems, based on Binary Verdict Analysis methodology with standardized project structure.

## Prerequisites

### Required Data
1. Specific problem from target platform (e.g., CSES 1197)
2. Algorithmically equivalent solutions in C++ and Python
3. Official test cases from platform
4. Real submission data for external validation

### Technical Environment
1. Docker configured with appropriate images
2. Python 3.11+ for analysis scripts
3. Platform access for external data collection

## Phase 1: Preparation

### 1.1 Problem Analysis
- [ ] Identify algorithmic complexity
- [ ] Classify category (graphs, DP, backtracking, etc.)
- [ ] Determine typical test case size
- [ ] Verify output types (unique vs multiple valid outputs)

### 1.2 External Data Collection
- [ ] Submit C++ solution on real platform
- [ ] Submit Python solution on real platform
- [ ] Document cases that cause TLE in Python
- [ ] Identify critical cases vs control cases

### 1.3 Solution Preparation
- [ ] Formal proof of algorithmic equivalence
- [ ] Optimized solutions for both languages
- [ ] Suboptimal solutions for selectivity validation
- [ ] Correctness validation on small cases

## Phase 2: Configuration

### 2.1 Experimental Parameters
```json
{
  "time_limit": "equal_to_real_platform",
  "repetitions": "minimum_10_per_case",
  "docker_images": {
    "cpp": "gcc:latest",
    "python": "python:3.11-slim"
  },
  "critical_cases": "based_on_external_data",
  "control_cases": "representative_sample"
}
```

### 2.2 Standardized Directory Structure
```
problemXX/
├── implementations/
│   ├── optimal/
│   │   ├── solution.cpp
│   │   └── solution.py
│   └── suboptimal/
│       ├── solution.cpp
│       └── solution.py
├── test_data/
│   ├── input/
│   │   ├── 1.in, 2.in, ...
│   └── output/
│       ├── 1.out, 2.out, ...
├── benchmarking/
│   ├── run_benchmark.py
│   ├── analyze_binary_verdict.py
│   └── validate_suboptimal.py
├── results/
│   ├── benchmark_results.json
│   ├── binary_analysis.json
│   └── validation_results.json
├── metadata/
│   └── problem_metadata.json
├── README.md
├── problem_specification.md
├── algorithmic_analysis.md
└── experimental_results.md
```

## Phase 3: Execution

### 3.1 Calibration
```bash
python3 benchmarking/run_benchmark.py \
  --phase=calibration \
  --case=REPRESENTATIVE_CASE \
  --repetitions=30 \
  --time-limit=REAL_LIMIT
```

**Objective**: Determine adjustment factor based on representative case

### 3.2 Binary Validation
```bash
python3 benchmarking/run_benchmark.py \
  --phase=validation \
  --cases=CRITICAL_CASES \
  --repetitions=10 \
  --time-limit=REAL_LIMIT \
  --adjustment-factor=CALIBRATED_FACTOR
```

**Objective**: Test traditional vs adaptive system

### 3.3 Binary Analysis
```bash
python3 benchmarking/analyze_binary_verdict.py
```

**Objective**: Apply binary methodology to results

### 3.4 Selectivity Validation
```bash
python3 benchmarking/validate_suboptimal.py \
  --cases=SAMPLE_CASES \
  --adjustment-factor=CALIBRATED_FACTOR
```

**Objective**: Confirm suboptimal solutions are rejected

## Phase 4: Analysis

### 4.1 Validation Criteria
- [ ] **Bias detected**: `traditional_cpp == ACCEPTED && traditional_python == REJECTED`
- [ ] **Bias corrected**: `adaptive_cpp == ACCEPTED && adaptive_python == ACCEPTED`
- [ ] **Selectivity preserved**: `suboptimal_solutions == REJECTED` in both systems
- [ ] **Realistic factor**: `1.5x <= adjustment_factor <= 50x`

### 4.2 Quality Metrics
```python
metrics = {
    "cpp_reliability": "relative_IQR < 0.15",
    "python_reliability": "relative_IQR < 0.15", 
    "rescued_cases": "count(python_rescued)",
    "external_correlation": "comparison_with_real_data"
}
```

### 4.3 Required Documentation
- [ ] **Problem specification**: `problem_specification.md`
- [ ] **Algorithmic analysis**: `algorithmic_analysis.md` (formal proofs)
- [ ] **Experimental results**: `experimental_results.md`
- [ ] **Main documentation**: `README.md`
- [ ] **Metadata**: `metadata/problem_metadata.json`
- [ ] **Raw data**: `results/*.json`

## Phase 5: External Validation

### 5.1 Real Data Comparison
- [ ] Correlation between local results and platform
- [ ] Explanation of identified discrepancies
- [ ] Validation of critical vs control cases

### 5.2 Quality Assurance
```python
# Execute automated quality checks
python3 /path/to/quality_assurance.py
```

## Success Criteria

### Valid Experiment
- Bias detected in traditional system
- Bias corrected in adaptive system  
- Selectivity preserved in both systems
- External correlation with real data
- Complete documentation generated

### Inconclusive Experiment
- No bias detected (investigate parameters)
- Compromised selectivity (adjust suboptimal solutions)
- Unrealistic factor (> 50x or < 1.5x)
- Low reliability (IQR > 0.15)

## Common Problem Resolution

### Problem: No Bias Detected
**Possible causes**:
- Time limit too permissive
- Insufficient critical cases
- Environment too different from real platform

**Solutions**:
- Reduce time limit
- Focus on cases that cause TLE on real platform
- Adjust Docker configuration

### Problem: Unrealistic Adjustment Factor
**Possible causes**:
- Large environment differences
- Non-equivalent algorithms
- Excessive Docker overhead

**Solutions**:
- Verify algorithmic equivalence
- Optimize Docker configuration
- Consider overhead as scientific insight

### Problem: Compromised Selectivity
**Possible causes**:
- Insufficiently slow suboptimal solutions
- Too permissive adjustment factor

**Solutions**:
- Increase computational overhead in suboptimal solutions
- Validate suboptimal solutions consistently cause TLE

## Automation Framework

### Reusable Scripts
1. **`run_benchmark.py`** - Benchmark execution
2. **`analyze_binary_verdict.py`** - Binary analysis
3. **`validate_suboptimal.py`** - Selectivity validation
4. **`quality_assurance.py`** - Automated quality checks

### Documentation Templates
1. **`README.md`** - Standard project overview
2. **`problem_specification.md`** - Academic problem description
3. **`algorithmic_analysis.md`** - Formal proofs and analysis
4. **`experimental_results.md`** - Results and findings
5. **`problem_metadata.json`** - Structured metadata

## Academic Documentation Requirements

### Problem Specification
- Formal problem statement
- Complexity analysis
- Input/output specifications
- Platform context (CSES problem number)

### Algorithmic Analysis
- Formal proof of algorithmic equivalence
- Loop invariants and correctness proofs
- Complexity analysis for both implementations
- Performance differential analysis

### Experimental Results
- Binary verdict analysis results
- Statistical significance testing
- External validation comparison
- Platform-specific findings

### Quality Standards
- Objective, academic language
- No promotional content
- English language throughout
- Formal mathematical notation where appropriate

## Methodological Validation

### Statistical Requirements
- Minimum 10 repetitions per critical case
- Confidence interval calculation
- Outlier detection and handling
- Significance testing where applicable

### External Validation Protocol
- Cross-platform result comparison
- Independent verification procedures
- Reproducibility documentation
- Peer review preparation

### Documentation Standards
- Complete experimental methodology
- Raw data preservation
- Analysis code availability
- Limitation acknowledgment

## Technical Specifications

### Execution Environment
- Docker containerization for consistency
- Standardized compiler flags and versions
- Resource monitoring and limitation
- Timeout mechanisms for safety

### Data Management
- Structured JSON format for all results
- Version control for all experimental assets
- Backup procedures for critical data
- Data integrity verification

### Quality Assurance
- Automated testing of analysis scripts
- Code review procedures
- Documentation completeness verification
- Reproducibility validation

## Protocol Evolution

### Current Implementation
- Binary methodology established
- Standardized directory structure
- Automated analysis pipeline
- Quality assurance procedures

### Future Enhancements
- Multi-platform support extension
- Multi-dimensional analysis beyond TLE
- Complete pipeline automation
- Real-time platform monitoring

## Technical Documentation

**Protocol**: General Experimental Protocol  
**Methodology**: Binary Verdict Analysis  
**Structure**: Standardized Academic Format  
**Status**: Production-ready for research applications
