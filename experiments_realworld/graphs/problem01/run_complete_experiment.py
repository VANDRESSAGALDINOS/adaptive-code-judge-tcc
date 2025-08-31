#!/usr/bin/env python3
"""
CSES 1672 Complete Experiment Runner
Executes full experimental protocol following experiment_plan.md
"""

import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    start_time = time.time()
    try:
        result = subprocess.run(cmd, check=True, text=True)
        elapsed = time.time() - start_time
        print(f"\n✅ {description} completed successfully in {elapsed:.1f}s")
        return True
    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start_time
        print(f"\n❌ {description} failed after {elapsed:.1f}s")
        print(f"Error: {e}")
        return False
    except KeyboardInterrupt:
        print(f"\n⚠️ {description} interrupted by user")
        return False

def check_prerequisites():
    """Check that all required files and tools are available."""
    print("🔍 Checking prerequisites...")
    
    base_dir = Path(".")
    required_files = [
        "solutions/solution.cpp",
        "solutions/solution.py", 
        "slow_validation/solutions_slow/slow_solution.cpp",
        "slow_validation/solutions_slow/slow_solution.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not (base_dir / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    # Check test cases
    tests_dir = base_dir / "tests_cses"
    if not tests_dir.exists():
        print(f"❌ Missing tests_cses directory")
        return False
    
    # Check for at least the key test cases
    key_cases = [1, 8, 15, 16]
    missing_tests = []
    for case_id in key_cases:
        if not (tests_dir / f"{case_id}.in").exists() or not (tests_dir / f"{case_id}.out").exists():
            missing_tests.append(case_id)
    
    if missing_tests:
        print(f"❌ Missing test cases: {missing_tests}")
        return False
    
    # Check Docker
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        subprocess.run(["docker", "ps"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"❌ Docker not available or not running")
        return False
    
    print("✅ All prerequisites satisfied")
    return True

def main():
    """Run complete CSES 1672 experiment following experiment_plan.md protocol."""
    
    print(f"🚀 CSES 1672 Complete Experiment")
    print(f"📋 Following experiment_plan.md protocol")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please fix the issues above.")
        sys.exit(1)
    
    # Create results directory
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    total_start_time = time.time()
    
    # Phase 1: Calibration
    # Following experiment_plan.md: Test case #8, 30 repetitions
    success = run_command(
        ["python3", "run_benchmark.py", "--phase=calibration", "--case=8", "--repetitions=30"],
        "PHASE 1: Calibration (Test Case #8, 30 repetitions)"
    )
    
    if not success:
        print("\n❌ Calibration failed. Cannot proceed with validation.")
        sys.exit(1)
    
    # Phase 2: Validation
    # Following experiment_plan.md: All 16 test cases, 10 repetitions each
    success = run_command(
        ["python3", "run_benchmark.py", "--phase=validation", "--repetitions=10"],
        "PHASE 2: Validation (All 16 test cases, 10 repetitions each)"
    )
    
    if not success:
        print("\n❌ Validation failed. Proceeding with analysis of partial data.")
    
    # Phase 3: Slow Solution Validation
    # Following experiment_plan.md: Verify selectivity preservation
    success = run_command(
        ["python3", "validate_slow_solutions.py", "--cases=8,15"],
        "PHASE 3: Slow Solution Validation (Selectivity preservation)"
    )
    
    if not success:
        print("\n⚠️ Slow solution validation failed. Results may be incomplete.")
    
    # Phase 4: Analysis
    # Generate comprehensive analysis and final report
    success = run_command(
        ["python3", "analyze_results.py", "--input=results", "--output=final_report.json"],
        "PHASE 4: Results Analysis and Report Generation"
    )
    
    if not success:
        print("\n⚠️ Analysis failed. Raw data is available in results/ directory.")
    
    # Summary
    total_elapsed = time.time() - total_start_time
    
    print(f"\n" + "="*80)
    print(f"🎉 EXPERIMENT COMPLETED")
    print(f"="*80)
    print(f"⏱️  Total execution time: {total_elapsed/60:.1f} minutes")
    print(f"📊 Results available in:")
    print(f"   - results/calibration_case8.json")
    print(f"   - results/validation_results.json")
    print(f"   - results/slow_solution_validation.json")
    print(f"   - final_report.json")
    
    # Check if final report was generated
    if Path("final_report.json").exists():
        print(f"\n📋 Final report successfully generated!")
        print(f"🎓 Ready for TCC analysis and defense.")
        
        # Try to show executive summary
        try:
            import json
            with open("final_report.json", 'r') as f:
                report = json.load(f)
            
            if 'success_evaluation' in report and report['success_evaluation']['overall_success']:
                print(f"\n🏆 EXPERIMENT STATUS: SUCCESSFUL")
                
                # Show key metrics if available
                if 'validation_analysis' in report and 'injustice_metrics' in report['validation_analysis']:
                    metrics = report['validation_analysis']['injustice_metrics']
                    print(f"📈 Key Results:")
                    print(f"   • Traditional Python success: {metrics['traditional_python_success_rate']:.1%}")
                    print(f"   • Adaptive Python success: {metrics['adaptive_python_success_rate']:.1%}")
                    print(f"   • TLE reduction: {metrics['tle_reduction_absolute']:+.1%}")
                    print(f"   • Cases rescued: {metrics['cases_rescued']}")
                
                if 'calibration_analysis' in report and report['calibration_analysis'].get('reliable'):
                    factor = report['calibration_analysis']['adjustment_factor']
                    print(f"   • Adjustment factor: {factor:.2f}x")
            else:
                print(f"\n⚠️ EXPERIMENT STATUS: REQUIRES REFINEMENT")
                print(f"   Check final_report.json for detailed analysis")
        
        except Exception as e:
            print(f"\n📊 Final report generated but summary extraction failed: {e}")
    else:
        print(f"\n⚠️ Final report not generated. Check individual result files.")
    
    print(f"\n" + "="*80)
    print(f"📚 Next steps:")
    print(f"   1. Review final_report.json for complete analysis")
    print(f"   2. Verify success criteria are met")
    print(f"   3. If successful, integrate results into TCC")
    print(f"   4. If unsuccessful, analyze failure reasons and refine")
    print(f"="*80)


if __name__ == '__main__':
    main()

