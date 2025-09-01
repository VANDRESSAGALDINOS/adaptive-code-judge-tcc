#!/usr/bin/env python3
"""
Binary Verdict Analysis for Problem03 CSES 1750
Applies CSES logic: any TLE = REJECTED
"""

import json
from pathlib import Path

def analyze_binary_verdict():
    """Apply binary verdict logic to validation results"""
    
    # Load validation results
    results_file = Path("results/validation_results.json")
    if not results_file.exists():
        print("❌ Validation results not found")
        return
    
    with open(results_file, 'r') as f:
        validation_data = f.read()
        if not validation_data.strip():
            print("❌ Validation results file is empty")
            return
        validation_results = json.loads(validation_data)
    
    print("=== BINARY VERDICT ANALYSIS ===")
    print("Applying CSES logic: Any TLE in any test case = REJECTED")
    
    # Analyze traditional system
    traditional = validation_results.get("traditional_system", {})
    
    # Analyze adaptive system  
    adaptive = validation_results.get("adaptive_system", {})
    
    # Apply binary logic
    def get_binary_verdict(system_results, language):
        """Return ACCEPTED only if ALL test cases pass for given language"""
        if not system_results:
            return "NO_DATA"
        
        for case_id, case_data in system_results.items():
            if case_id == "experiment_metadata":
                continue
                
            lang_data = case_data.get(language, {})
            detailed_results = lang_data.get("detailed_results", [])
            
            # Check if any run had TLE
            for run in detailed_results:
                if run.get("status") in ["TLE", "TIME_LIMIT_EXCEEDED"]:
                    return "REJECTED"
        
        return "ACCEPTED"
    
    # Calculate binary verdicts
    verdicts = {
        "traditional": {
            "cpp": get_binary_verdict(traditional, "cpp"),
            "python": get_binary_verdict(traditional, "python")
        },
        "adaptive": {
            "cpp": get_binary_verdict(adaptive, "cpp"), 
            "python": get_binary_verdict(adaptive, "python")
        }
    }
    
    print(f"\n📊 BINARY VERDICT RESULTS:")
    print(f"Traditional System:")
    print(f"  C++: {verdicts['traditional']['cpp']}")
    print(f"  Python: {verdicts['traditional']['python']}")
    print(f"Adaptive System:")
    print(f"  C++: {verdicts['adaptive']['cpp']}")
    print(f"  Python: {verdicts['adaptive']['python']}")
    
    # Analyze injustice
    injustice_detected = (
        verdicts['traditional']['cpp'] == "ACCEPTED" and 
        verdicts['traditional']['python'] == "REJECTED"
    )
    
    injustice_corrected = (
        verdicts['adaptive']['cpp'] == "ACCEPTED" and
        verdicts['adaptive']['python'] == "ACCEPTED"
    )
    
    python_rescued = (
        verdicts['traditional']['python'] == "REJECTED" and
        verdicts['adaptive']['python'] == "ACCEPTED"
    )
    
    print(f"\n⚖️ INJUSTICE ANALYSIS:")
    print(f"Injustice detected: {'✅ YES' if injustice_detected else '❌ NO'}")
    print(f"Injustice corrected: {'✅ YES' if injustice_corrected else '❌ NO'}")
    print(f"Python rescued: {'✅ YES' if python_rescued else '❌ NO'}")
    
    # Save binary analysis
    binary_analysis = {
        "methodology": "Binary Verdict (CSES Logic)",
        "logic": "Any TLE in any test case = REJECTED",
        "verdicts": verdicts,
        "injustice_analysis": {
            "detected": injustice_detected,
            "corrected": injustice_corrected,
            "python_rescued": python_rescued
        },
        "scientific_contribution": {
            "traditional_gap": f"C++ {verdicts['traditional']['cpp']} vs Python {verdicts['traditional']['python']}",
            "adaptive_gap": f"C++ {verdicts['adaptive']['cpp']} vs Python {verdicts['adaptive']['python']}",
            "methodology_impact": "Binary verdict reveals true injustice vs statistical masking"
        }
    }
    
    with open("binary_verdict_analysis.json", "w") as f:
        json.dump(binary_analysis, f, indent=2)
    
    print(f"\n💾 Binary verdict analysis saved to: binary_verdict_analysis.json")
    
    # Generate summary report
    with open("BINARY_VERDICT_REPORT.md", "w") as f:
        f.write("# Binary Verdict Analysis - Problem03 CSES 1750\n\n")
        f.write("## Methodology\n")
        f.write("Applied CSES binary logic: Any TLE in any test case results in REJECTED verdict.\n\n")
        f.write("## Results\n\n")
        f.write("### Traditional System (1.0s limit)\n")
        f.write(f"- **C++**: {verdicts['traditional']['cpp']}\n")
        f.write(f"- **Python**: {verdicts['traditional']['python']}\n\n")
        f.write("### Adaptive System (C++: 1.0s, Python: 3.19s)\n")
        f.write(f"- **C++**: {verdicts['adaptive']['cpp']}\n")
        f.write(f"- **Python**: {verdicts['adaptive']['python']}\n\n")
        f.write("## Injustice Analysis\n\n")
        f.write(f"- **Injustice Detected**: {'✅ YES' if injustice_detected else '❌ NO'}\n")
        f.write(f"- **Injustice Corrected**: {'✅ YES' if injustice_corrected else '❌ NO'}\n")
        f.write(f"- **Python Rescued**: {'✅ YES' if python_rescued else '❌ NO'}\n\n")
        f.write("## Scientific Impact\n\n")
        f.write("Binary verdict methodology reveals true competitive programming injustice ")
        f.write("that statistical success rates can mask. This approach mirrors real-world ")
        f.write("online judge behavior where any single TLE results in solution rejection.\n")
    
    print(f"📄 Binary verdict report saved to: BINARY_VERDICT_REPORT.md")
    
    return binary_analysis

if __name__ == "__main__":
    analyze_binary_verdict()
