# Binary Verdict Analysis Framework

## Overview

Reusable framework for implementing Binary Verdict Analysis methodology in linguistic bias detection experiments across online judge systems.

## Framework Components

### 1. Base Class: BinaryVerdictAnalyzer

```python
class BinaryVerdictAnalyzer:
    """Base framework for binary verdict analysis"""
    
    def __init__(self, platform_name, time_limit, critical_cases):
        self.platform_name = platform_name
        self.time_limit = time_limit
        self.critical_cases = critical_cases
        self.control_cases = []
        
    def load_validation_results(self, results_file):
        """Load validation results"""
        pass
        
    def analyze_binary_verdict(self, results):
        """Apply binary methodology"""
        pass
        
    def generate_report(self, analysis):
        """Generate scientific report"""
        pass
```

### 2. Execution Module: BenchmarkExecutor

```python
class BenchmarkExecutor:
    """Standardized benchmark executor"""
    
    def __init__(self, docker_config, solutions_dir, tests_dir):
        self.docker_config = docker_config
        self.solutions_dir = solutions_dir
        self.tests_dir = tests_dir
        
    def run_calibration(self, case_id, repetitions, time_limit):
        """Calibration phase"""
        pass
        
    def run_validation(self, cases, repetitions, adjustment_factor, time_limit):
        """Binary validation phase"""
        pass
        
    def validate_selectivity(self, slow_solutions, cases, adjustment_factor):
        """Selectivity validation"""
        pass
```

### 3. Utilities: VerdictUtils

```python
class VerdictUtils:
    """Utilities for verdict analysis"""
    
    @staticmethod
    def is_tle_status(status):
        """Check if status indicates TLE"""
        return status in ["TLE", "TIME_LIMIT_EXCEEDED"]
        
    @staticmethod
    def calculate_final_verdict(detailed_results):
        """Calculate final verdict based on detailed results"""
        for result in detailed_results:
            if VerdictUtils.is_tle_status(result["status"]):
                return "REJECTED"
        return "ACCEPTED"
        
    @staticmethod
    def detect_injustice(traditional_results, adaptive_results):
        """Detect linguistic injustice"""
        trad_cpp = traditional_results["cpp"]["final_verdict"]
        trad_python = traditional_results["python"]["final_verdict"]
        adapt_cpp = adaptive_results["cpp"]["final_verdict"]
        adapt_python = adaptive_results["python"]["final_verdict"]
        
        injustice_detected = (trad_cpp == "ACCEPTED" and trad_python == "REJECTED")
        injustice_corrected = (adapt_cpp == "ACCEPTED" and adapt_python == "ACCEPTED")
        
        return {
            "injustice_detected": injustice_detected,
            "injustice_corrected": injustice_corrected,
            "python_rescued": trad_python == "REJECTED" and adapt_python == "ACCEPTED"
        }
```

## Implementation Templates

### 1. Binary Analysis Script

```python
#!/usr/bin/env python3
"""
Template: Binary Verdict Analysis
Adapt for your specific experiment
"""

import json
from pathlib import Path
from binary_verdict_framework import BinaryVerdictAnalyzer

def main():
    # Experiment-specific configuration
    analyzer = BinaryVerdictAnalyzer(
        platform_name="CSES",  # Adapt for your platform
        time_limit=1.0,        # Real platform limit
        critical_cases=[6, 7, 8, 9, 10]  # Cases that cause TLE
    )
    
    # Load results
    results = analyzer.load_validation_results("results/validation_results.json")
    
    # Apply binary analysis
    analysis = analyzer.analyze_binary_verdict(results)
    
    # Generate report
    report = analyzer.generate_report(analysis)
    
    # Save results
    with open("binary_verdict_analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)
    
    with open("BINARY_VERDICT_REPORT.md", "w") as f:
        f.write(report)
    
    print("Binary analysis completed")

if __name__ == "__main__":
    main()
```

### 2. Standard Docker Configuration

```python
DOCKER_CONFIG = {
    "cpp": {
        "image": "gcc:latest",
        "compile_cmd": "g++ -O2 -std=c++17 solution.cpp -o solution",
        "run_cmd": "timeout {time_limit}s ./solution"
    },
    "python": {
        "image": "python:3.11-slim", 
        "compile_cmd": None,
        "run_cmd": "timeout {time_limit}s python3 solution.py"
    }
}
```

### 3. Metadata Structure

```json
{
  "experiment": {
    "problem": "problemXX",
    "platform": "CSES",
    "date": "2025-08-30",
    "status": "complete"
  },
  "binary_methodology": {
    "traditional_cpp": "ACCEPTED|REJECTED",
    "traditional_python": "ACCEPTED|REJECTED",
    "adaptive_cpp": "ACCEPTED|REJECTED", 
    "adaptive_python": "ACCEPTED|REJECTED",
    "injustice_detected": true,
    "injustice_corrected": true,
    "python_rescued": true
  },
  "parameters": {
    "time_limit": 1.0,
    "critical_cases": [6, 7, 8, 9, 10],
    "adjustment_factor": 4.33,
    "repetitions": 10
  }
}
```

## Implementation Checklist

### Preparation
- [ ] Identify critical cases via external data
- [ ] Configure Docker with appropriate images
- [ ] Prepare algorithmically equivalent solutions
- [ ] Create slow solutions for validation

### Execution
- [ ] Execute calibration to determine factor
- [ ] Execute validation with binary analysis
- [ ] Validate selectivity with slow solutions
- [ ] Compare with external platform data

### Analysis
- [ ] Apply binary methodology to results
- [ ] Verify injustice criteria
- [ ] Generate scientific report
- [ ] Document specific discoveries

### Validation
- [ ] Confirm correlation with external data
- [ ] Verify statistical reliability
- [ ] Validate selectivity preservation
- [ ] Document limitations and insights

## Platform Adaptations

### CSES
```python
CSES_CONFIG = {
    "time_limit": 1.0,  # CSES standard
    "memory_limit": "512MB",
    "languages": ["C++17", "Python3"],
    "verdict_format": ["ACCEPTED", "TLE", "WA", "RE"]
}
```

### AtCoder
```python
ATCODER_CONFIG = {
    "time_limit": 2.0,  # AtCoder standard
    "memory_limit": "1024MB", 
    "languages": ["C++17", "Python3"],
    "verdict_format": ["AC", "TLE", "WA", "RE"]
}
```

### LeetCode
```python
LEETCODE_CONFIG = {
    "time_limit": "variable",  # Problem-dependent
    "memory_limit": "variable",
    "languages": ["C++", "Python3"],
    "verdict_format": ["Accepted", "Time Limit Exceeded", "Wrong Answer"]
}
```

## Future Extensions

### Multi-dimensional Analysis
```python
class MultiDimensionalAnalyzer(BinaryVerdictAnalyzer):
    """Extension for analysis beyond TLE"""
    
    def analyze_all_verdicts(self, results):
        """Analyze TLE, WA, RE, etc."""
        pass
        
    def calculate_fairness_index(self, results):
        """Calculate quantitative fairness index"""
        pass
```

### Complete Automation
```python
class AutomatedPipeline:
    """Fully automated pipeline"""
    
    def collect_external_data(self, platform, problem_id):
        """Collect external data automatically"""
        pass
        
    def run_complete_experiment(self, config):
        """Execute complete experiment"""
        pass
        
    def generate_final_report(self, results):
        """Generate final report automatically"""
        pass
```

## Installation and Usage

### Dependencies
```bash
pip install docker pandas numpy matplotlib seaborn
```

### Basic Usage
```python
from binary_verdict_framework import BinaryVerdictAnalyzer

# Configure experiment
analyzer = BinaryVerdictAnalyzer("CSES", 1.0, [6, 7, 8, 9, 10])

# Execute analysis
results = analyzer.load_validation_results("results.json")
analysis = analyzer.analyze_binary_verdict(results)
report = analyzer.generate_report(analysis)

# Save results
analyzer.save_results(analysis, report)
```

## Technical Specifications

### System Requirements
- Python 3.11+
- Docker Engine
- Minimum 4GB RAM
- Linux/Unix environment recommended

### Performance Considerations
- Parallel execution support for multiple test cases
- Memory-efficient result storage
- Configurable timeout mechanisms
- Resource monitoring capabilities

### Security Features
- Sandboxed code execution via Docker
- Input validation for all user data
- Safe file handling procedures
- Resource limit enforcement

## Validation Protocol

### Statistical Validation
- Minimum 10 repetitions per test case
- Confidence interval calculation
- Outlier detection and handling
- Statistical significance testing

### External Validation
- Cross-platform result comparison
- Independent verification procedures
- Reproducibility documentation
- Peer review preparation

### Quality Assurance
- Automated testing suite
- Code coverage analysis
- Performance benchmarking
- Documentation completeness verification

## Academic Applications

### Research Integration
- Standardized methodology for bias detection studies
- Reproducible experimental framework
- Comparative analysis across platforms
- Longitudinal bias monitoring

### Educational Use
- Teaching tool for algorithmic fairness concepts
- Hands-on experience with bias detection
- Real-world application of statistical methods
- Programming language comparison studies

### Industry Applications
- Platform fairness auditing
- Quality assurance for online judges
- Competitive programming equity assessment
- Technical interview bias detection

## Framework Limitations

### Known Constraints
- Focus on temporal bias (TLE) detection
- Binary classification approach
- Platform-specific calibration requirements
- Docker dependency for execution

### Mitigation Strategies
- Multi-dimensional extension development
- Continuous calibration procedures
- Alternative execution environment support
- Comprehensive documentation of limitations

## Technical Documentation

**Framework**: Binary Verdict Analysis Framework  
**Language**: Python 3.11+  
**License**: Academic/Educational Use  
**Status**: Production-ready for research applications
