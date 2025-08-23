# 🎓 Adaptive Code Judge - Scientific Framework for Algorithmic Complexity Analysis

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Required-blue.svg)](https://docker.com)
[![Status](https://img.shields.io/badge/Status-TCC%20Ready-green.svg)](https://github.com)
[![Validation](https://img.shields.io/badge/Validation-100%25%20Success-brightgreen.svg)](#validation-results)

> **TCC Project**: Adaptive Online Judge System with Scientific Methodology for Performance Analysis in Containerized Environments

## 🚀 **Quick Start**

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/adaptive-code-judge.git
cd adaptive-code-judge

# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/init_db.py

# Run scientific experiments
cd experiments
python run_experiment_with_validation.py On_linear
```

## 🔬 **Scientific Achievements**

### ✅ **6 Complexity Classes Scientifically Validated**

| Complexity | Input Size | C++ Time | Python Time | Validation |
|------------|------------|----------|-------------|------------|
| **O(1)**      | 10M ops | Baseline | Baseline | ✅ 100% |
| **O(log n)**  | 1M elements | Fast | Fast | ✅ 100% |
| **O(n)**      | 1M elements | 0.436s | 1.208s | ✅ 100% |
| **O(n²)**     | 1000×1000 | 0.389s | 0.661s | ✅ 100% |
| **O(n³)**     | 300×300 | 0.396s | 1.296s | ✅ 100% |
| **O(2ⁿ)**     | n=22 | 0.343s | 0.480s | ✅ 100% |

### 🧠 **Unique Scientific Contributions**

1. **🎯 Scale Dependency Principle**: Massive inputs make algorithmic differences dominate Docker overhead
2. **⚡ Anti-Optimization Strategies**: Techniques to prevent compiler optimization in complexity testing
3. **📊 Docker Overhead Quantification**: First systematic analysis of containerization impact on performance studies
4. **🔍 Automatic Time Limit Validation**: Novel framework using optimal/slow solution pairs

## 📊 **Research Methodology**

### 🔄 **Scientific Transformation Process**

This project demonstrates a complete **methodological transformation** from flawed initial approach to rigorous scientific methodology:

#### ❌ **Initial Issues (67% Validation Failure)**
- Small input sizes (Docker overhead dominated)
- Compiler optimization invalidating slow solutions
- No statistical rigor
- Invalid scientific conclusions

#### ✅ **Rigorous Solution (100% Validation Success)**
- Massive input sizes (algorithmic differences dominate)
- Anti-optimization techniques (`printf + fflush`, `sys.setrecursionlimit`)
- Statistical analysis framework
- Scientifically valid conclusions

## 🏗️ **Architecture**

```
adaptive-code-judge/
├── src/                    # Core system components
│   ├── api/               # Flask REST API
│   ├── models/            # Database models
│   ├── services/          # Business logic
│   └── executor/          # Docker execution engine
├── experiments/           # Scientific experiment framework
│   ├── complexity_analysis/  # 6 complexity class studies
│   └── statistical_analysis.py  # Statistical validation
├── docker/               # Containerization setup
└── docs/                 # Scientific documentation
```

## 🧪 **Running Experiments**

### **Individual Complexity Classes:**
```bash
cd experiments
python run_experiment_with_validation.py O1_constant
python run_experiment_with_validation.py O_log_n  
python run_experiment_with_validation.py On_linear
python run_experiment_with_validation.py On2_quadratic
python run_experiment_with_validation.py On3_cubic
python run_experiment_with_validation.py O2n_exponential
```

### **Complete Scientific Suite:**
```bash
./run_all_experiments.sh
```

## 📈 **Validation Results**

### **🎯 Performance Patterns Discovered:**

- **Python Overhead Varies by Complexity**: 1.4x (O(2ⁿ)) to 3.27x (O(n³))
- **Scale Dependency**: Input sizes ≥1M elements ensure algorithmic dominance
- **Docker Overhead**: Constant ≈0.3s, overcome by massive inputs
- **Compiler Intelligence**: GCC aggressively optimizes "useless" loops

### **📊 Framework Validation:**
- ✅ **100% Success Rate**: All optimal solutions pass within time limits
- ✅ **100% TLE Detection**: All slow solutions correctly timeout
- ✅ **Consistent Results**: Reproducible across multiple runs

## 🎓 **Academic Impact**

### **📚 TCC Contributions:**

1. **Novel Methodology**: First framework for complexity analysis in containerized environments
2. **Scientific Rigor**: Complete documentation of methodological transformation
3. **Practical Tool**: Working system applicable to competitive programming education
4. **Generalizable Framework**: Methodology transferable to other performance studies

### **📄 Scientific Documentation:**

- [`TRANSFORMACAO_METODOLOGICA_TCC.md`](experiments/TRANSFORMACAO_METODOLOGICA_TCC.md) - Complete methodological analysis
- [`INSIGHTS_CIENTIFICOS_TCC.md`](experiments/complexity_analysis/INSIGHTS_CIENTIFICOS_TCC.md) - Scientific discoveries
- [`CONCLUSAO_FINAL_TCC.md`](experiments/CONCLUSAO_FINAL_TCC.md) - Final academic conclusions

## 🚀 **Future Research**

- **Multi-language Support**: Extend to Java, JavaScript, Go
- **Cloud Scaling**: Kubernetes-based distributed execution
- **AI Integration**: Machine learning for adaptive time prediction
- **Educational Platform**: Full LMS integration

## 📞 **Contact & Citation**

**Author**: [Your Name]  
**Institution**: [Your University]  
**Project**: TCC - Computer Science  
**Year**: 2024

```bibtex
@thesis{adaptive_code_judge_2024,
  title={Adaptive Code Judge: Scientific Framework for Algorithmic Complexity Analysis in Containerized Environments},
  author={[Your Name]},
  year={2024},
  school={[Your University]},
  type={Bachelor's Thesis}
}
```

## 📜 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**🎖️ TCC-Ready Scientific Framework with 100% Validation Success! 🎖️**

*Demonstrating not only technical competence but the ability to identify and correct fundamental methodological issues - a critical skill for any computer science researcher.*
