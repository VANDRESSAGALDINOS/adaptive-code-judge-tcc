# Standard Problem Structure - Real-World Experiments

## Objective

Establish a consistent, scalable, and academically rigorous directory structure for all real-world algorithm analysis problems.

## Standard Directory Structure

```
experiments_realworld/
├── STANDARD_STRUCTURE.md          # This document
├── EXPERIMENTAL_FRAMEWORK.md      # Overall methodology
├── README.md                       # Research overview
└── {category}/                     # Algorithm category
    └── {problem_id}/               # Specific problem
        ├── README.md               # Problem overview
        ├── problem_specification.md # Formal problem definition
        ├── algorithmic_analysis.md  # Formal equivalence proof
        ├── experimental_results.md  # Empirical findings summary
        ├── implementations/         # All algorithm implementations
        │   ├── optimal/            # Efficient algorithms
        │   │   ├── solution.cpp    # C++ optimal implementation
        │   │   └── solution.py     # Python optimal implementation
        │   └── suboptimal/         # Inefficient algorithms
        │       ├── solution.cpp    # C++ suboptimal implementation
        │       └── solution.py     # Python suboptimal implementation
        ├── test_data/              # External validation data
        │   ├── input/              # Test case inputs
        │   │   ├── 01.in
        │   │   ├── 02.in
        │   │   └── ...
        │   └── output/             # Expected outputs
        │       ├── 01.out
        │       ├── 02.out
        │       └── ...
        ├── benchmarking/           # Experimental execution
        │   ├── run_benchmark.py   # Automated benchmark execution
        │   ├── analyze_results.py # Statistical analysis
        │   └── validate_algorithms.py # Algorithm validation
        ├── results/                # Experimental data
        │   ├── benchmark_data.json # Raw performance measurements
        │   ├── statistical_analysis.json # Processed statistics
        │   └── external_validation.json # Platform validation results
        └── metadata/               # Problem metadata
            ├── problem_metadata.json # Structured problem information
            └── experimental_config.json # Benchmark configuration
```

## File Specifications

### Core Documentation Files

#### 1. `README.md` (Problem Level)
- **Purpose**: Problem overview and research context
- **Content**: Problem statement, research objectives, key findings
- **Language**: English, academic tone
- **Length**: 200-500 words

#### 2. `problem_specification.md`
- **Purpose**: Formal mathematical problem definition
- **Content**: Input/output format, constraints, complexity bounds
- **Standard**: Mathematical notation, algorithmic specification
- **Validation**: External platform reference (CSES, etc.)

#### 3. `algorithmic_analysis.md`
- **Purpose**: Formal equivalence proofs and complexity analysis
- **Content**: Mathematical proofs, invariants, complexity theorems
- **Standard**: Academic rigor with formal mathematical notation
- **Requirements**: Peer-review quality analysis

#### 4. `experimental_results.md`
- **Purpose**: Summary of empirical findings
- **Content**: Statistical results, performance comparisons, significance testing
- **Standard**: Scientific reporting with confidence intervals
- **Validation**: External platform verification required

### Implementation Standards

#### Directory: `implementations/optimal/`
- **Files**: `solution.cpp`, `solution.py`
- **Requirements**: Algorithmically equivalent, optimal complexity
- **Documentation**: Minimal inline comments, self-documenting code
- **Validation**: Must pass all test cases on external platform

#### Directory: `implementations/suboptimal/`
- **Files**: `solution.cpp`, `solution.py`  
- **Requirements**: Functionally equivalent, deliberately inefficient
- **Purpose**: Demonstrate differential algorithm selectivity
- **Validation**: Should fail time limits on external platform

### Data Management

#### Directory: `test_data/`
- **Structure**: Separate input/ and output/ subdirectories
- **Naming**: Sequential numbering (01.in, 02.in, ...)
- **Source**: Official platform test cases when available
- **Validation**: Verified against external platform

#### Directory: `results/`
- **Files**: JSON format for structured data
- **Content**: Raw measurements, processed statistics, validation results
- **Standards**: Statistical significance testing, confidence intervals
- **Reproducibility**: Complete experimental configuration preserved

### Execution Scripts

#### `benchmarking/run_benchmark.py`
- **Purpose**: Automated performance measurement
- **Standards**: Docker containerization, statistical repetition
- **Output**: Structured JSON results
- **Configuration**: Parameterized execution settings

#### `benchmarking/analyze_results.py`
- **Purpose**: Statistical analysis of benchmark data
- **Standards**: Significance testing, effect size calculation
- **Output**: Publication-ready statistical summaries
- **Validation**: Confidence interval reporting

#### `benchmarking/validate_algorithms.py`
- **Purpose**: Verify algorithmic correctness and equivalence
- **Standards**: Formal verification against test cases
- **Output**: Validation reports with pass/fail status
- **Requirements**: 100% correctness verification

## Implementation Guidelines

### File Naming Conventions
- **Languages**: Use standard extensions (.cpp, .py)
- **Categories**: lowercase with underscores (e.g., dynamic_programming)
- **Problems**: descriptive names with IDs (e.g., coin_combinations_cses1635)
- **Data Files**: Sequential numbering with zero padding

### Code Standards
- **Comments**: Minimal, academic-appropriate only
- **Language**: English for all identifiers and comments
- **Style**: Consistent formatting, professional quality
- **Documentation**: Self-documenting code preferred

### Data Standards
- **Format**: JSON for structured data, plain text for test cases
- **Encoding**: UTF-8 throughout
- **Precision**: Appropriate numerical precision for measurements
- **Metadata**: Complete experimental configuration preservation

## Quality Assurance

### Validation Requirements
1. **External Platform**: All solutions must be validated on original platform
2. **Algorithmic Equivalence**: Formal mathematical proof required
3. **Statistical Significance**: p < 0.05 threshold for performance claims
4. **Reproducibility**: Complete methodology documentation

### Review Checklist
- [ ] All file names follow naming conventions
- [ ] Documentation is in academic English
- [ ] Formal proofs are mathematically rigorous
- [ ] Statistical analysis includes confidence intervals
- [ ] External validation is documented
- [ ] No development artifacts or binary files
- [ ] Consistent structure across all problems

## Migration Guidelines

### For Existing Problems
1. **Audit Current Structure**: Identify deviations from standard
2. **Reorganize Files**: Move files to standard locations
3. **Rename Files**: Apply consistent naming conventions
4. **Clean Artifacts**: Remove binary files and development debris
5. **Validate Documentation**: Ensure academic quality standards
6. **Update Scripts**: Modify paths and references

### For New Problems
1. **Create Standard Structure**: Use template directory structure
2. **Implement Solutions**: Follow implementation guidelines
3. **Document Analysis**: Create formal proofs and analysis
4. **Validate Externally**: Verify on original platform
5. **Run Benchmarks**: Execute statistical analysis
6. **Review Quality**: Apply quality assurance checklist

## Benefits of Standardization

### Academic Benefits
- **Consistency**: Uniform structure across all experiments
- **Reproducibility**: Clear methodology for replication
- **Scalability**: Easy addition of new problems and categories
- **Quality**: Enforced academic standards throughout

### Practical Benefits
- **Maintenance**: Simplified codebase management
- **Automation**: Standardized scripts across problems
- **Analysis**: Consistent data formats for meta-analysis
- **Collaboration**: Clear structure for multiple researchers

## Conclusion

This standardized structure ensures academic rigor, reproducibility, and scalability for all real-world algorithm analysis experiments. Adherence to these guidelines will produce publication-quality research with consistent methodology and clear presentation.

---

**Version**: 1.0
**Status**: Implementation Required
**Scope**: All experiments_realworld problems
