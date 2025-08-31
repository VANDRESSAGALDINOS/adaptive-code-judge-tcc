#!/usr/bin/env python3
"""
Análise Binária de Veredicto - Problem02
Simula exatamente como o CSES avalia: qualquer TLE = REJECTED
"""

import json
import os
from pathlib import Path

def load_validation_results():
    """Carrega os resultados de validação"""
    results_file = Path("results/validation_results.json")
    if not results_file.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {results_file}")
    
    with open(results_file, 'r') as f:
        return json.load(f)

def analyze_binary_verdict(results):
    """
    Analisa com lógica binária do CSES:
    - Se QUALQUER caso dá TLE → VEREDICTO FINAL = REJECTED
    - Se TODOS os casos passam → VEREDICTO FINAL = ACCEPTED
    """
    
    analysis = {
        "traditional_system": {},
        "adaptive_system": {},
        "summary": {}
    }
    
    # Analisar sistema tradicional
    traditional = results["traditional_system"]
    for lang in ["cpp", "python"]:
        has_any_tle = False
        total_cases = 0
        
        for case_id, case_data in traditional.items():
            if lang in case_data:
                total_cases += 1
                lang_data = case_data[lang]
                
                # Verificar se houve algum TLE neste caso
                for result in lang_data["detailed_results"]:
                    if result["status"] in ["TIME_LIMIT_EXCEEDED", "TLE"]:
                        has_any_tle = True
                        break
                
                if has_any_tle:
                    break
        
        # Veredicto final
        final_verdict = "REJECTED" if has_any_tle else "ACCEPTED"
        analysis["traditional_system"][lang] = {
            "final_verdict": final_verdict,
            "total_cases_tested": total_cases,
            "had_tle": has_any_tle
        }
    
    # Analisar sistema adaptativo
    adaptive = results["adaptive_system"]
    for lang in ["cpp", "python"]:
        has_any_tle = False
        total_cases = 0
        
        for case_id, case_data in adaptive.items():
            if lang in case_data:
                total_cases += 1
                lang_data = case_data[lang]
                
                # Verificar se houve algum TLE neste caso
                for result in lang_data["detailed_results"]:
                    if result["status"] in ["TIME_LIMIT_EXCEEDED", "TLE"]:
                        has_any_tle = True
                        break
                
                if has_any_tle:
                    break
        
        # Veredicto final
        final_verdict = "REJECTED" if has_any_tle else "ACCEPTED"
        analysis["adaptive_system"][lang] = {
            "final_verdict": final_verdict,
            "total_cases_tested": total_cases,
            "had_tle": has_any_tle
        }
    
    # Resumo comparativo
    trad_cpp = analysis["traditional_system"]["cpp"]["final_verdict"]
    trad_python = analysis["traditional_system"]["python"]["final_verdict"]
    adapt_cpp = analysis["adaptive_system"]["cpp"]["final_verdict"]
    adapt_python = analysis["adaptive_system"]["python"]["final_verdict"]
    
    # Detectar injustiça
    injustice_detected = (trad_cpp == "ACCEPTED" and trad_python == "REJECTED")
    injustice_corrected = (adapt_cpp == "ACCEPTED" and adapt_python == "ACCEPTED")
    
    analysis["summary"] = {
        "injustice_detected": injustice_detected,
        "injustice_corrected": injustice_corrected,
        "traditional_system": {
            "cpp_verdict": trad_cpp,
            "python_verdict": trad_python,
            "language_parity": trad_cpp == trad_python
        },
        "adaptive_system": {
            "cpp_verdict": adapt_cpp,
            "python_verdict": adapt_python,
            "language_parity": adapt_cpp == adapt_python
        },
        "improvement": {
            "python_rescued": trad_python == "REJECTED" and adapt_python == "ACCEPTED",
            "selectivity_preserved": adapt_cpp == "ACCEPTED"  # C++ deve continuar passando
        }
    }
    
    return analysis

def generate_binary_report(analysis):
    """Gera relatório em formato acadêmico"""
    
    report = []
    report.append("# ANÁLISE BINÁRIA DE VEREDICTO - Problem02")
    report.append("## Metodologia CSES Simulada")
    report.append("")
    report.append("**Lógica de Avaliação:**")
    report.append("- Qualquer caso com TLE → VEREDICTO FINAL = REJECTED")
    report.append("- Todos os casos ACCEPTED → VEREDICTO FINAL = ACCEPTED")
    report.append("")
    
    # Resultados Sistema Tradicional
    report.append("## 🔴 Sistema Tradicional (Limite Fixo)")
    trad = analysis["traditional_system"]
    report.append(f"- **C++**: {trad['cpp']['final_verdict']}")
    report.append(f"- **Python**: {trad['python']['final_verdict']}")
    report.append("")
    
    # Resultados Sistema Adaptativo
    report.append("## 🟢 Sistema Adaptativo (Fator 4.33x)")
    adapt = analysis["adaptive_system"]
    report.append(f"- **C++**: {adapt['cpp']['final_verdict']}")
    report.append(f"- **Python**: {adapt['python']['final_verdict']}")
    report.append("")
    
    # Análise de Injustiça
    summary = analysis["summary"]
    report.append("## 📊 Análise de Injustiça")
    
    if summary["injustice_detected"]:
        report.append("✅ **INJUSTIÇA DETECTADA**: C++ aprovado, Python rejeitado (sistema tradicional)")
    else:
        report.append("❌ **Injustiça não detectada** no sistema tradicional")
    
    if summary["injustice_corrected"]:
        report.append("✅ **INJUSTIÇA CORRIGIDA**: Ambas linguagens aprovadas (sistema adaptativo)")
    else:
        report.append("❌ **Injustiça não corrigida** pelo sistema adaptativo")
    
    report.append("")
    
    # Métricas Científicas
    report.append("## 🎯 Métricas Científicas")
    improvement = summary["improvement"]
    report.append(f"- **Python Resgatado**: {'✅ SIM' if improvement['python_rescued'] else '❌ NÃO'}")
    report.append(f"- **Seletividade Preservada**: {'✅ SIM' if improvement['selectivity_preserved'] else '❌ NÃO'}")
    report.append(f"- **Paridade Linguística Tradicional**: {'✅ SIM' if summary['traditional_system']['language_parity'] else '❌ NÃO'}")
    report.append(f"- **Paridade Linguística Adaptativa**: {'✅ SIM' if summary['adaptive_system']['language_parity'] else '❌ NÃO'}")
    report.append("")
    
    # Conclusão Científica
    report.append("## 🏆 Conclusão Científica")
    if summary["injustice_detected"] and summary["injustice_corrected"]:
        report.append("**EXPERIMENTO VÁLIDO**: Demonstra injustiça e sua correção com rigor metodológico.")
        report.append("- Sistema tradicional: Discriminação linguística")
        report.append("- Sistema adaptativo: Paridade linguística alcançada")
    else:
        report.append("**EXPERIMENTO INCONCLUSIVO**: Não demonstra claramente injustiça ou correção.")
    
    return "\n".join(report)

def main():
    """Execução principal"""
    try:
        print("🔍 Carregando resultados de validação...")
        results = load_validation_results()
        
        print("⚖️ Analisando com lógica binária...")
        analysis = analyze_binary_verdict(results)
        
        print("📝 Gerando relatório...")
        report = generate_binary_report(analysis)
        
        # Salvar análise JSON
        with open("binary_verdict_analysis.json", "w") as f:
            json.dump(analysis, f, indent=2)
        
        # Salvar relatório markdown
        with open("BINARY_VERDICT_REPORT.md", "w") as f:
            f.write(report)
        
        print("✅ Análise binária concluída!")
        print("\nArquivos gerados:")
        print("- binary_verdict_analysis.json")
        print("- BINARY_VERDICT_REPORT.md")
        
        # Mostrar resumo
        print("\n" + "="*60)
        print("RESUMO EXECUTIVO")
        print("="*60)
        summary = analysis["summary"]
        print(f"Injustiça Detectada: {'✅ SIM' if summary['injustice_detected'] else '❌ NÃO'}")
        print(f"Injustiça Corrigida: {'✅ SIM' if summary['injustice_corrected'] else '❌ NÃO'}")
        print(f"Python Resgatado: {'✅ SIM' if summary['improvement']['python_rescued'] else '❌ NÃO'}")
        print(f"Seletividade Preservada: {'✅ SIM' if summary['improvement']['selectivity_preserved'] else '❌ NÃO'}")
        
    except Exception as e:
        print(f"❌ Erro na análise: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
