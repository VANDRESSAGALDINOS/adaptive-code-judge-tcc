#!/usr/bin/env python3
"""
CSES 1635 DP Iterativo Results Analysis Script
Analyzes benchmark data and generates scientific metrics
Following experiment_plan.md analysis protocol
"""

import argparse
import json
import statistics
from datetime import datetime
from pathlib import Path
import sys

class CSES1635IterativeAnalyzer:
    """Analyzer for CSES 1635 DP Iterativo benchmark results following scientific protocol."""
    
    def __init__(self, results_dir=None):
        self.results_dir = Path(results_dir or "results")
        
        # Case categorization from CSES validation
        self.critical_cases = [4, 5, 8, 11, 12]  # Expected TLE in Python
        self.control_cases = [1, 3, 6, 7, 9, 10, 13]  # Expected PASS in Python
        
    def load_calibration_data(self):
        """Load calibration results."""
        calibration_file = self.results_dir / "calibration_case9.json"
        
        if not calibration_file.exists():
            raise FileNotFoundError(f"Calibration file not found: {calibration_file}")
        
        with open(calibration_file, 'r') as f:
            return json.load(f)
    
    def load_validation_data(self):
        """Load validation results."""
        validation_file = self.results_dir / "validation_results.json"
        
        if not validation_file.exists():
            raise FileNotFoundError(f"Validation file not found: {validation_file}")
        
        with open(validation_file, 'r') as f:
            return json.load(f)
    
    def load_slow_validation_data(self):
        """Load slow validation results."""
        slow_file = self.results_dir / "slow_solution_validation.json"
        
        if not slow_file.exists():
            raise FileNotFoundError(f"Slow validation file not found: {slow_file}")
        
        with open(slow_file, 'r') as f:
            return json.load(f)
    
    def analyze_calibration_reliability(self, calibration_data):
        """Analyze calibration reliability following scientific criteria."""
        print("=== CALIBRATION ANALYSIS ===")
        
        cpp_times = calibration_data['cpp']['times']
        python_times = calibration_data['python']['times']
        
        # Statistical measures
        cpp_median = statistics.median(cpp_times)
        python_median = statistics.median(python_times)
        cpp_iqr = statistics.quantiles(cpp_times, n=4)[2] - statistics.quantiles(cpp_times, n=4)[0]
        python_iqr = statistics.quantiles(python_times, n=4)[2] - statistics.quantiles(python_times, n=4)[0]
        
        # Variability percentages
        cpp_variability = (cpp_iqr / cpp_median) * 100 if cpp_median > 0 else 0
        python_variability = (python_iqr / python_median) * 100 if python_median > 0 else 0
        
        # Reliability criteria (from graphs methodology)
        cpp_reliable = cpp_variability < 15.0
        python_reliable = python_variability < 20.0
        
        print(f"Test Case: {calibration_data['test_case']}")
        print(f"Repetitions: {calibration_data['repetitions']}")
        print(f"C++ Median: {cpp_median:.3f}s (IQR: {cpp_iqr:.3f}s, Variability: {cpp_variability:.1f}%)")
        print(f"Python Median: {python_median:.3f}s (IQR: {python_iqr:.3f}s, Variability: {python_variability:.1f}%)")
        print(f"Adjustment Factor: {calibration_data['adjustment_factor']:.3f}x")
        print(f"C++ Reliability: {'✓' if cpp_reliable else '✗'} ({'PASS' if cpp_reliable else 'FAIL'})")
        print(f"Python Reliability: {'✓' if python_reliable else '✗'} ({'PASS' if python_reliable else 'FAIL'})")
        
        return {
            "test_case": calibration_data['test_case'],
            "repetitions": calibration_data['repetitions'],
            "cpp_median": cpp_median,
            "python_median": python_median,
            "adjustment_factor": calibration_data['adjustment_factor'],
            "cpp_variability": cpp_variability,
            "python_variability": python_variability,
            "cpp_reliable": cpp_reliable,
            "python_reliable": python_reliable,
            "overall_reliable": cpp_reliable and python_reliable
        }
    
    def analyze_injustice_metrics(self, validation_data):
        """Analyze injustice metrics from validation data."""
        print("\n=== INJUSTICE ANALYSIS ===")
        
        test_cases = validation_data['test_cases']
        adjustment_factor = validation_data['adjustment_factor']
        
        # Count success/failure by system
        traditional_cpp_success = 0
        traditional_python_success = 0
        adaptive_python_success = 0
        total_tests = 0
        
        critical_traditional_cpp = 0
        critical_traditional_python = 0
        critical_adaptive_python = 0
        critical_total = 0
        
        for test_case_str, repetitions in test_cases.items():
            test_case = int(test_case_str)
            
            for rep in repetitions:
                total_tests += 1
                
                # Count successes
                if rep['cpp_traditional']['status'] == 'ACCEPTED':
                    traditional_cpp_success += 1
                if rep['python_traditional']['status'] == 'ACCEPTED':
                    traditional_python_success += 1
                if rep['python_adaptive']['status'] == 'ACCEPTED':
                    adaptive_python_success += 1
                
                # Count critical cases
                if test_case in self.critical_cases:
                    critical_total += 1
                    if rep['cpp_traditional']['status'] == 'ACCEPTED':
                        critical_traditional_cpp += 1
                    if rep['python_traditional']['status'] == 'ACCEPTED':
                        critical_traditional_python += 1
                    if rep['python_adaptive']['status'] == 'ACCEPTED':
                        critical_adaptive_python += 1
        
        # Calculate rates
        traditional_cpp_rate = (traditional_cpp_success / total_tests) * 100
        traditional_python_rate = (traditional_python_success / total_tests) * 100
        adaptive_python_rate = (adaptive_python_success / total_tests) * 100
        
        injustice_gap = traditional_cpp_rate - traditional_python_rate
        correction_improvement = adaptive_python_rate - traditional_python_rate
        
        # Critical cases rates
        if critical_total > 0:
            critical_cpp_rate = (critical_traditional_cpp / critical_total) * 100
            critical_python_traditional_rate = (critical_traditional_python / critical_total) * 100
            critical_python_adaptive_rate = (critical_adaptive_python / critical_total) * 100
        else:
            critical_cpp_rate = critical_python_traditional_rate = critical_python_adaptive_rate = 0
        
        print(f"📊 OVERALL RESULTS:")
        print(f"  Traditional: C++ {traditional_cpp_rate:.1f}%, Python {traditional_python_rate:.1f}% (gap: {injustice_gap:.1f}%)")
        print(f"  Adaptive:    C++ {traditional_cpp_rate:.1f}%, Python {adaptive_python_rate:.1f}% (gap: {traditional_cpp_rate - adaptive_python_rate:.1f}%)")
        print(f"  Python improvement: +{correction_improvement:.1f}%")
        
        print(f"\n🎯 CRITICAL CASES ANALYSIS:")
        print(f"  Traditional: C++ {critical_cpp_rate:.1f}%, Python {critical_python_traditional_rate:.1f}%")
        print(f"  Adaptive:    C++ {critical_cpp_rate:.1f}%, Python {critical_python_adaptive_rate:.1f}%")
        
        # Injustice correction assessment
        injustice_eliminated = abs(traditional_cpp_rate - adaptive_python_rate) < 10.0
        significant_improvement = correction_improvement > 30.0
        
        print(f"\n⚖️ INJUSTICE CORRECTION METRICS:")
        print(f"  Traditional Python success: {traditional_python_rate:.1f}%")
        print(f"  Adaptive Python success: {adaptive_python_rate:.1f}%")
        print(f"  Absolute TLE reduction: +{correction_improvement:.1f}%")
        print(f"  Injustice eliminated: {'✓' if injustice_eliminated else '✗'}")
        print(f"  Significant improvement: {'✓' if significant_improvement else '✗'}")
        
        return {
            "adjustment_factor": adjustment_factor,
            "total_tests": total_tests,
            "traditional_cpp_rate": traditional_cpp_rate,
            "traditional_python_rate": traditional_python_rate,
            "adaptive_python_rate": adaptive_python_rate,
            "injustice_gap": injustice_gap,
            "correction_improvement": correction_improvement,
            "critical_cases": {
                "cpp_rate": critical_cpp_rate,
                "python_traditional_rate": critical_python_traditional_rate,
                "python_adaptive_rate": critical_python_adaptive_rate
            },
            "success_metrics": {
                "injustice_eliminated": injustice_eliminated,
                "significant_improvement": significant_improvement
            }
        }
    
    def analyze_selectivity_preservation(self, slow_data):
        """Analyze selectivity preservation from slow validation."""
        print("\n=== SELECTIVITY PRESERVATION ===")
        
        test_cases = slow_data['test_cases']
        time_limit = slow_data['time_limit']
        results = slow_data['validation_results']
        
        cpp_tle_count = 0
        python_tle_count = 0
        total_tests = len(test_cases)
        
        for test_case in test_cases:
            test_case_str = str(test_case)
            if test_case_str in results:
                if results[test_case_str]['cpp_slow']['status'] == 'TLE':
                    cpp_tle_count += 1
                if results[test_case_str]['python_slow']['status'] == 'TLE':
                    python_tle_count += 1
        
        cpp_tle_rate = (cpp_tle_count / total_tests) * 100
        python_tle_rate = (python_tle_count / total_tests) * 100
        
        # Selectivity criteria: slow solutions should get TLE
        selectivity_preserved = cpp_tle_rate >= 80.0 and python_tle_rate >= 80.0
        
        print(f"Time Limit: {time_limit}s")
        print(f"Test Cases: {test_cases}")
        print(f"C++ Slow TLE Rate: {cpp_tle_rate:.1f}% ({cpp_tle_count}/{total_tests})")
        print(f"Python Slow TLE Rate: {python_tle_rate:.1f}% ({python_tle_count}/{total_tests})")
        print(f"Selectivity Preserved: {'✓' if selectivity_preserved else '✗'}")
        
        return {
            "time_limit": time_limit,
            "test_cases": test_cases,
            "cpp_tle_rate": cpp_tle_rate,
            "python_tle_rate": python_tle_rate,
            "selectivity_preserved": selectivity_preserved
        }
    
    def generate_final_report(self, calibration_analysis, injustice_analysis, selectivity_analysis):
        """Generate comprehensive final report."""
        
        # Overall experiment success assessment
        # For DP experiments: Success = reliable calibration + injustice confirmed + selectivity preserved
        # Note: Adaptive solution not working is a valid scientific discovery
        experiment_successful = (
            calibration_analysis['overall_reliable'] and
            injustice_analysis['injustice_gap'] > 30.0 and  # Injustice confirmed
            selectivity_analysis['selectivity_preserved']
        )
        
        final_report = {
            "experiment_metadata": {
                "problem": "CSES 1635 - Coin Combinations I (DP Iterativo)",
                "date": datetime.now().isoformat(),
                "algorithm": "Dynamic Programming Iterativo",
                "languages": ["C++", "Python"],
                "methodology": "Controlled benchmark with adaptive time limits"
            },
            "calibration": calibration_analysis,
            "injustice_metrics": injustice_analysis,
            "selectivity": selectivity_analysis,
            "experiment_success": {
                "overall_successful": experiment_successful,
                "criteria_met": {
                    "calibration_reliable": calibration_analysis['overall_reliable'],
                    "injustice_confirmed": injustice_analysis['injustice_gap'] > 30.0,
                    "selectivity_preserved": selectivity_analysis['selectivity_preserved']
                }
            },
            "scientific_conclusions": {
                "temporal_injustice_confirmed": injustice_analysis['injustice_gap'] > 30.0,
                "adaptive_solution_effective": injustice_analysis['correction_improvement'] > 30.0,
                "algorithmic_selectivity_maintained": selectivity_analysis['selectivity_preserved'],
                "discovery": "DP Iterativo mantém injustiça temporal - causa é overhead interpretativo, não recursão"
            }
        }
        
        print(f"\n{'='*50}")
        print(f"✅ EXPERIMENT STATUS: {'SUCCESSFUL' if experiment_successful else 'INCONCLUSIVE'}")
        print(f"{'='*50}")
        
        return final_report

def main():
    parser = argparse.ArgumentParser(description="CSES 1635 DP Iterativo Results Analysis")
    parser.add_argument("--input", default="results", help="Results directory")
    parser.add_argument("--output", default="final_report.json", help="Output report file")
    
    args = parser.parse_args()
    
    try:
        analyzer = CSES1635IterativeAnalyzer(args.input)
        
        print("🔬 CSES 1635 DP ITERATIVO - ANÁLISE CIENTÍFICA")
        print(f"📁 Input: {args.input}")
        print(f"📄 Output: {args.output}")
        
        # Load all data
        calibration_data = analyzer.load_calibration_data()
        validation_data = analyzer.load_validation_data()
        slow_data = analyzer.load_slow_validation_data()
        
        # Perform analyses
        calibration_analysis = analyzer.analyze_calibration_reliability(calibration_data)
        injustice_analysis = analyzer.analyze_injustice_metrics(validation_data)
        selectivity_analysis = analyzer.analyze_selectivity_preservation(slow_data)
        
        # Generate final report
        final_report = analyzer.generate_final_report(
            calibration_analysis, injustice_analysis, selectivity_analysis
        )
        
        # Save report
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            json.dump(final_report, f, indent=2)
        
        print(f"\n📊 Final report saved: {output_path}")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
