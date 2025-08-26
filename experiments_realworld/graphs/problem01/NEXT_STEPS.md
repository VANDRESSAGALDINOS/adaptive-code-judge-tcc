# Next Steps - Implementation Guide

## **Context Summary**
You are continuing work on an adaptive code judge experiment to detect and correct language bias between C++ and Python in online judges. The theoretical groundwork is COMPLETE, and you now need to implement the benchmark execution.

## **What's Already Done ✅**

### **Scientific Foundation:**
- ✅ **Problem Selected**: CSES 1672 - Shortest Routes II (Floyd-Warshall O(n³))
- ✅ **Algorithms Implemented**: C++ and Python solutions ready
- ✅ **Formal Proof**: Mathematical equivalence proven (`formal_proof.md`)
- ✅ **External Validation**: CSES submissions completed and documented
- ✅ **Test Cases**: All 16 official CSES cases available
- ✅ **Methodology**: Complete experimental protocol defined

### **CSES Validation Results:**
```
C++ Efficient: ACCEPTED (16/16 cases) - https://cses.fi/problemset/result/14297533/
Python Efficient: TLE (9/16 cases) - Injustice demonstrated
C++ Slow: TLE (16/16 cases) - https://cses.fi/problemset/result/14298232/  
Python Slow: TLE (16/16 cases) - https://cses.fi/problemset/result/14298238/
```

### **Key Insight Established:**
**Python fails 56.25% of cases despite algorithmic correctness - this is the injustice we will fix with adaptive time limits.**

## **What You Need To Implement ⏳**

### **Priority 1: Benchmark Execution Script**
```bash
File: run_benchmark.py
Purpose: Automated execution of calibration and validation phases
Input: Test cases from tests_cses/
Output: Raw timing data + success/failure status
Time: ~2-3 hours implementation
```

### **Priority 2: Results Analysis Script**  
```bash
File: analyze_results.py
Purpose: Statistical analysis and metric calculation
Input: Raw benchmark data
Output: Final metrics for TCC (adjustment factor, TLE reduction, etc.)
Time: ~1-2 hours implementation
```

### **Priority 3: Docker Environment Setup**
```bash
Purpose: Isolated execution environment
Components: C++ compilation + Python execution containers
Base: Existing system setup (you already have Docker working)
Time: ~1 hour adaptation
```

## **Detailed Implementation Plan**

### **Step 1: Benchmark Script (`run_benchmark.py`)**

#### **Core Function - Calibration Phase:**
```python
def run_calibration(case_id=8, repetitions=15):
    """
    Execute calibration on primary test case (#8)
    Returns: cpp_times[], python_times[]
    """
    # Implementation based on experiment_plan.md section 4.2
```

#### **Core Function - Validation Phase:**
```python
def run_validation(strategic_cases=[1,8,12,13,15,16], repetitions=5):
    """
    Execute validation on strategic test cases
    Returns: traditional_results, adaptive_results
    """
    # Implementation based on experiment_plan.md section 4.4
```

### **Step 2: Analysis Script (`analyze_results.py`)**

#### **Statistical Calculations:**
```python
def calculate_calibration_metrics(cpp_times, python_times):
    """
    Calculate adjustment factor and reliability metrics
    Returns: adjustment_factor, reliability_status
    """
    # Based on experiment_plan.md section 5.1
```

#### **Injustice Metrics:**
```python
def calculate_injustice_correction(traditional_results, adaptive_results):
    """
    Calculate TLE reduction and cases rescued
    Returns: tle_reduction_absolute, cases_rescued
    """
    # Zero-division safe metrics from experiment_plan.md section 5.2
```

### **Step 3: Execution Protocol**

#### **Recommended Execution Order:**
```bash
# 1. Setup environment
cd experiments_realworld/graphs/problem01
python -m venv venv
source venv/bin/activate  # macOS
pip install numpy pandas docker

# 2. Run calibration
python run_benchmark.py --phase=calibration --case=8 --repetitions=15

# 3. Run validation  
python run_benchmark.py --phase=validation --cases=1,8,12,13,15,16 --repetitions=5

# 4. Analyze results
python analyze_results.py --input=results/ --output=final_report.json

# 5. Generate TCC report
python generate_tcc_report.py --results=final_report.json
```

## **Expected Results (Based on CSES Evidence)**

### **Calibration Results:**
```
C++ median time (Test #8): ~0.5s
Python median time (Test #8): ~1.4s  
Adjustment factor: ~2.8x
Adaptive limit: ~2.8s (vs 1.0s original)
```

### **Validation Results:**
```
Traditional System:
- C++ success rate: 100% (6/6 cases)
- Python success rate: 50% (3/6 cases) - only controls pass

Adaptive System:
- C++ success rate: 100% (6/6 cases) - preserved
- Python success rate: 100% (6/6 cases) - injustice corrected
```

### **Key Metrics for TCC:**
```
TLE Reduction: 50 percentage points (50% → 0%)
Cases Rescued: 3 critical cases (#8, #12, #15)
Adjustment Factor: ~2.8x (empirically derived)
Selectivity Preserved: 100% (slow solutions still TLE)
```

## **Files Location Reference**

### **Implementation Specs:**
- **Main Plan**: `experiment_plan.md` (sections 4-6)
- **Docker Setup**: `experiment_plan.md` section 4.1
- **Metrics Details**: `experiment_plan.md` section 5
- **Success Criteria**: `experiment_plan.md` section 6

### **Code Assets:**
- **Solutions**: `solutions/solution.cpp`, `solutions/solution.py`
- **Test Cases**: `tests_cses/1.in` through `tests_cses/16.in`
- **Slow Validation**: `slow_validation/solutions_slow/`

### **Documentation:**
- **Problem Context**: `problem_description.md`
- **Formal Proof**: `formal_proof.md`
- **TLE Validation**: `slow_validation/tle_validation_report.md`

## **Timeline Realistic**

### **Implementation Phase:**
- **Day 1 Morning**: Docker setup + run_benchmark.py calibration
- **Day 1 Afternoon**: run_benchmark.py validation + analyze_results.py
- **Day 2 Morning**: Testing, debugging, final execution
- **Day 2 Afternoon**: Report generation + TCC integration

### **Execution Phase:**
- **Benchmark Runtime**: ~5 minutes total
- **Analysis Runtime**: ~1 minute
- **Report Generation**: ~10 minutes

**Total Project Time: 2 days maximum (most is implementation, execution is very fast)**

## **Success Indicators**

### **Technical Success:**
```
✅ Calibration reliable (both languages CV < 20%)
✅ Adjustment factor reasonable (2.5-3.0x range)
✅ TLE reduction > 50 percentage points
✅ No C++ regression (maintains 100% success)
✅ Selectivity preserved (slow solutions still fail)
```

### **Academic Success:**
```
✅ Methodology rigorously followed
✅ External validation confirmed
✅ Statistical significance achieved
✅ Results align with CSES observations
✅ Framework generalizable and replicable
```

## **Emergency Simplification**

### **If Time Constrained:**
**Minimum Viable Experiment**: Focus only on Test Case #8 with 10 repetitions each
- Still demonstrates core concept
- Reduces implementation complexity
- Maintains scientific validity
- Takes 2 hours vs 2 days

### **Core Value Preserved:**
Even with simplification, you still get:
- Empirical adjustment factor  
- Demonstration of injustice correction
- Validation of adaptive approach
- Sufficient data for TCC conclusions

---

## **Final Note**
**The hardest work is done!** You have complete scientific foundation, validated external evidence, and clear implementation roadmap. The coding is now straightforward execution of the documented protocols.

**Focus on `experiment_plan.md` - it contains every technical detail you need.**
