# Adaptive Code Judge - Linguistic Bias Detection in Online Judge Systems

## Overview

This research project investigates linguistic bias in online judge systems through development and validation of an adaptive benchmarking framework. The system addresses performance differentials between compiled and interpreted languages in algorithmic evaluation environments.

## Research Objectives

### Primary Objective
Develop and validate a methodology for detecting and correcting linguistic bias in online judge systems, specifically addressing systematic disadvantages faced by interpreted languages (Python) compared to compiled languages (C++).

### Secondary Objectives
1. Quantify performance differentials across algorithmic complexity classes
2. Establish statistical frameworks for bias detection
3. Validate adaptive correction mechanisms through empirical testing
4. Demonstrate practical applicability in real-world competitive programming scenarios

## Methodology

### Binary Verdict Analysis
Core methodology for objective bias detection through exact simulation of platform evaluation logic. Employs binary classification (ACCEPTED/REJECTED) mirroring real online judge systems.

### Experimental Framework
- **Containerized execution environment** using Docker for consistent benchmarking
- **Algorithmic equivalence validation** ensuring fair performance comparisons
- **Statistical analysis** with rigorous hypothesis testing and validation protocols
- **External validation** against real platform data (CSES Online Judge)

### Statistical Methodology
Comprehensive statistical validation framework ensuring scientific rigor:

#### Hypothesis Testing
- **Mann-Whitney U Test**: Non-parametric significance testing for robust analysis
- **Welch t-test**: Parametric testing for normally distributed data
- **Shapiro-Wilk Test**: Normality assessment for appropriate test selection
- **Significance Level**: α = 0.05 for all hypothesis tests

#### Statistical Rigor Requirements
- **Sample Size**: N ≥ 30 per condition (Central Limit Theorem compliance)
- **Confidence Intervals**: 95% confidence intervals for all performance measurements
- **Effect Size**: Cohen's d calculation for practical significance assessment
- **Power Analysis**: Statistical power β ≥ 0.8 for adequate detection capability

#### Quality Assurance Metrics
- **Descriptive Statistics**: Mean, median, standard deviation, and interquartile range
- **Reliability Assessment**: IQR-based stability criteria (≤15% C++, ≤20% Python)
- **Reproducibility Protocols**: Multiple repetitions with controlled environmental conditions

### Problem Categories

#### Complexity Analysis
Six algorithmic complexity classes systematically analyzed:
- **O(1) Constant**: Baseline performance establishment
- **O(log n) Logarithmic**: Binary search implementations with anti-optimization
- **O(n) Linear**: Array processing with 177% performance differential detected
- **O(n²) Quadratic**: Matrix operations with 154% performance differential detected  
- **O(n³) Cubic**: Three-dimensional array processing
- **O(2^n) Exponential**: Subset enumeration problems

#### Real-World Problem Validation
Competitive programming problems from CSES platform organized by algorithmic category:

**Backtracking Problems:**
- **Problem 1**: Chessboard Queens (N-Queens variant) - Severe bias detected
- **Problem 2**: Grid Paths - 30% Python success vs 100% C++ success on CSES
- **Problem 3**: Apple Division - No bias detected (100% success both languages)

**Dynamic Programming Problems:**
- **Problem 1**: Coin Combinations I (CSES 1635) - Iterative vs recursive analysis
- **Problem 2**: Grid Paths (CSES 1638) - Path counting with memoization
- **Problem 3**: Two Sets (CSES 1093) - Subset partitioning problem

**Graph Algorithm Problems:**
- **Problem 1**: Shortest Routes II (Floyd-Warshall) - 56.25% Python TLE rate
- **Problem 2**: Cycle Finding (Bellman-Ford) - First binary verdict methodology application
- **Problem 3**: Planets Queries I (Binary Lifting) - Platform variability analysis

## Key Findings

### Complexity Analysis Results
Systematic analysis across six complexity classes revealed consistent patterns with quantified performance differentials:

**Quantitative Performance Metrics:**
- **O(n) Linear**: 177% algorithmic difference detected (1.2s vs 0.4s execution times)
- **O(n²) Quadratic**: 154% algorithmic difference detected (1000×1000 matrix operations)
- **Validation Success Rate**: Improved from 33% to 100% through methodological refinement
- **Algorithmic Dominance Ratio**: Achieved 5:1 algorithmic-to-overhead ratio (vs initial 0.03:1)

**Key Principles Discovered:**
- **Scale dependency principle**: Large input sizes amplify algorithmic differences while minimizing containerization overhead
- **Critical threshold identification**: Input sizes >5MB required for scientific validity
- **Anti-optimization requirements**: Compiler optimizations can invalidate performance comparisons
- **Docker overhead quantification**: ~0.3s constant startup cost with O(1) scaling behavior

### Real-World Validation
Analysis of competitive programming problems demonstrated:
- **Variable bias presence**: Not all problems exhibit linguistic bias
- **Severity spectrum**: Bias ranges from absent to severe depending on algorithmic characteristics
- **Architectural limitations**: Deep recursion problems reveal fundamental language limitations beyond performance differences

### Methodological Contributions
1. **Binary verdict analysis methodology**: First formalization for online judge bias detection
2. **Platform-agnostic framework**: Applicable across different online judge systems
3. **Adaptive correction mechanisms**: Validated approaches for bias mitigation
4. **Statistical rigor**: Comprehensive validation protocols

## Technical Architecture

### Core Components
```
adaptive-code-judge/
├── src/                          # System implementation
│   ├── api/                     # REST API endpoints
│   ├── models/                  # Database models
│   ├── services/                # Business logic
│   └── executor/                # Docker execution engine
├── experiments/                  # Scientific experiments
│   ├── complexity_analysis/     # Complexity class studies
│   └── experiments_realworld/   # Real-world problem validation
├── documentation/               # Research documentation
│   ├── methodology/            # Core methodologies
│   ├── insights/               # Scientific discoveries
│   ├── frameworks/             # Technical frameworks
│   └── protocols/              # Experimental protocols
└── docker/                     # Containerization setup
```

### Execution Environment
- **Python 3.11+** for analysis and system implementation
- **Docker** for containerized code execution
- **SQLite/PostgreSQL** for data persistence
- **Flask** for API implementation

## Scientific Contributions

### Methodological Innovations
1. **Binary Verdict Analysis**: Novel methodology for objective bias detection in online judge systems
2. **Adaptive Benchmarking Framework**: Platform-agnostic system for bias correction
3. **Statistical Validation Protocols**: Rigorous approaches for experimental validation
4. **Containerized Performance Analysis**: Systematic study of Docker impact on algorithmic benchmarking

### Empirical Discoveries
1. **Algorithmic Complexity Correlation**: Performance differentials vary systematically by complexity class
2. **Platform Variability Analysis**: Identical algorithms exhibit environment-dependent performance variations
3. **Architectural Limitation Identification**: Deep recursion reveals categorical differences between language paradigms
4. **Bias Variability Spectrum**: Comprehensive characterization of when and why bias occurs

## Experimental Validation

### Statistical Rigor
- **Confidence intervals** for all performance measurements
- **Significance testing** for bias detection claims
- **External validation** against real platform data
- **Reproducibility protocols** for independent verification

### Quality Assurance
- **Algorithmic equivalence proofs** for all solution pairs
- **Correctness validation** on sample inputs
- **Performance consistency** verification across multiple runs
- **Platform correlation** analysis

## Usage Instructions

### System Requirements
- Python 3.11 or higher
- Docker Engine
- Minimum 4GB RAM
- Linux/Unix environment (recommended)

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/init_db.py

# Verify Docker setup
docker --version
```

### Running Experiments
```bash
# Individual complexity analysis
cd experiments
python run_experiment_with_validation.py On_linear

# Complete experimental suite
./run_all_experiments.sh

# Real-world problem validation
cd experiments_realworld
python run_benchmark.py
```

### API Usage
```bash
# Start system
python start_server.py

# Access endpoints
curl http://localhost:8000/api/problems
curl http://localhost:8000/api/submissions
```

## Research Applications

### Academic Research
- Comparative language performance studies
- Online judge fairness analysis
- Algorithmic bias detection methodology development
- Educational platform equity assessment

### Industry Applications
- Quality assurance for programming contest platforms
- Technical interview bias detection
- Educational tool fairness verification
- Competitive programming equity improvement

### Policy Development
- Regulatory framework foundation for algorithmic fairness
- Industry standard development for online judge systems
- Best practices documentation for platform operators
- Certification criteria establishment

## Future Research Directions

### Methodological Extensions
- Multi-dimensional bias analysis beyond temporal factors
- Machine learning integration for automated bias detection
- Cross-platform comparative studies
- Real-time monitoring system development

### Broader Applications
- Extension to additional programming languages
- Analysis of memory-based bias factors
- Integration with existing online judge platforms
- Development of standardized fairness metrics

## Documentation Structure

Complete research documentation is organized in the `documentation/` directory:
- **Methodology**: Core research methodologies and frameworks
- **Insights**: Scientific discoveries and empirical findings
- **Protocols**: Experimental procedures and validation protocols
- **Frameworks**: Technical implementation guidelines

## Technical Specifications

**Research Context**: Computer Science - Computational Systems  
**Methodology**: Empirical software engineering with statistical validation  
**Platform**: Cross-platform with Linux optimization  
**License**: Academic research use  
**Status**: Research validation complete, ready for peer review

## Reproducibility

All experimental procedures, data analysis scripts, and validation protocols are documented and available for independent replication. Raw data, analysis code, and complete methodology documentation ensure full reproducibility of results.

## Architectural Design and Development

### Initial Architecture Planning
The system architecture was initially documented through a comprehensive RFC (Request for Comments) that outlined the theoretical framework and design principles. This architectural planning document is available at:

**RFC 001 - Adaptive Code Judge Architecture**: https://github.com/VANDRESSAGALDINOS/adaptive-code-judge-rfc/blob/main/RFC001.md

The RFC documents the original system design, including container architecture, API specifications, and component interactions. As typical in software development, the actual implementation evolved from this initial design based on empirical findings and practical requirements discovered during development.

### Implementation Evolution
The final system architecture incorporates significant refinements from the original RFC design, particularly in:
- Enhanced statistical validation protocols
- Refined binary verdict analysis methodology  
- Expanded experimental framework for real-world validation
- Advanced anti-optimization strategies for compiler interference

## Author Information

**Author**: Vandressa Galdino Soares  
**Student ID**: 120210147  
**Institution**: Universidade Federal de Campina Grande (UFCG)  
**Email**: vandressa.soares@ccc.ufcg.edu.br  

### Academic Profiles and Validation Data
- **Codeforces Profile**: https://codeforces.com/profile/dressa_galdin
- **CSES Profile**: https://cses.fi/user/255266
- **Submission History**: All submissions used in this study can be verified at https://codeforces.com/submissions/dressa_galdin
- **Thesis Document**: https://drive.google.com/file/d/1wB7t_6ghTc5mGiledNRpA1E99-kqb4aA/view?usp=drive_link

The author's competitive programming profiles demonstrate practical experience with the algorithmic problems analyzed in this research, with 137 submissions on CSES (63.50% C++, 35.77% Python3) providing empirical validation data for the bias detection methodology.

## Contact Information

This research was conducted as part of a Computer Science thesis project at UFCG focusing on algorithmic fairness and linguistic bias detection in computational evaluation systems. The work represents a comprehensive investigation into systematic biases affecting competitive programming platforms and educational assessment tools.
