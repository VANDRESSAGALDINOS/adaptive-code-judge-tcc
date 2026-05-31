#!/usr/bin/env python3
"""
Slow Validation Script para Chessboard and Queens - Backtracking Problem01
Seguindo Protocolo Metodológico Rigoroso
Foco: Quantificar Seletividade Diferencial ao Overhead
"""

import subprocess
import time
import json
import os
import sys
from pathlib import Path

def compile_cpp_slow():
    """Compila a solução C++ slow"""
    try:
        result = subprocess.run([
            'g++', '-O2', '-std=c++17', 
            'slow_validation/solutions_slow/slow_solution.cpp', 
            '-o', 'slow_validation/solutions_slow/slow_solution_cpp'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            print(f"Erro na compilação C++ slow: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Erro ao compilar C++ slow: {e}")
        return False

def run_solution(executable, input_data, timeout=15):
    """Executa uma solução e mede o tempo"""
    try:
        start_time = time.perf_counter()
        
        if executable.endswith('.py'):
            result = subprocess.run([
                sys.executable, executable
            ], input=input_data, capture_output=True, text=True, timeout=timeout)
        else:
            result = subprocess.run([
                executable
            ], input=input_data, capture_output=True, text=True, timeout=timeout)
        
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        if result.returncode != 0:
            return None, execution_time, f"Runtime error: {result.stderr}"
        
        return result.stdout.strip(), execution_time, None
    
    except subprocess.TimeoutExpired:
        return None, timeout, "Timeout"
    except Exception as e:
        return None, 0, f"Error: {str(e)}"

def generate_critical_test_cases():
    """Gera casos críticos para testar seletividade diferencial"""
    test_cases = []
    
    # Caso 1: Tabuleiro livre (máximo overhead)
    free_board = ["." * 8 for _ in range(8)]
    test_cases.append(("free_board_critical", free_board, "Máximo de possibilidades - overhead extremo"))
    
    # Caso 2: CSES example (caso padrão)
    cses_example = [
        "........",
        "........", 
        "..*.....",
        "........",
        "........",
        ".....**..",
        "...*....",
        "........"
    ]
    test_cases.append(("cses_example_critical", cses_example, "Caso padrão CSES"))
    
    # Caso 3: Poucas restrições (alto overhead)
    few_restrictions = [
        "........",
        "........",
        "........",
        "....*...",
        "........",
        "........",
        "........",
        "........"
    ]
    test_cases.append(("few_restrictions", few_restrictions, "Poucas restrições - overhead alto"))
    
    # Caso 4: Primeira coluna livre (força backtracking)
    first_col_free = [
        ".......* ",
        ".......* ",
        ".......* ",
        ".......* ",
        ".......* ",
        ".......* ",
        ".......* ",
        ".......* "
    ]
    # Corrigir espaços extras
    first_col_free = [line.rstrip() + "*" for line in first_col_free]
    test_cases.append(("first_col_free", first_col_free, "Força backtracking intenso"))
    
    return test_cases

def run_slow_validation():
    """Executa validação das soluções slow"""
    print("🐌 EXECUTANDO SLOW VALIDATION - Chessboard and Queens")
    print("🎯 Foco: Quantificar Seletividade Diferencial ao Overhead")
    print("=" * 70)
    
    critical_cases = generate_critical_test_cases()
    
    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "algorithm": "backtracking_n_queens",
        "extra_work": 2000,
        "focus": "seletividade_diferencial",
        "test_cases": critical_cases,
        "validation_results": []
    }
    
    print(f"🎯 Casos Críticos: {len(critical_cases)}")
    print(f"⚙️  EXTRA_WORK: {results['extra_work']}")
    print(f"⏱️  Timeout: 15s por execução")
    print(f"🔬 Objetivo: Medir sensibilidade diferencial ao overhead")
    
    for case_name, board, description in critical_cases:
        print(f"\n🔍 Validando: {case_name}")
        print(f"   Descrição: {description}")
        
        test_input = "\n".join(board)
        
        case_result = {
            "case_name": case_name,
            "description": description,
            "board": board,
            "optimized": {"cpp": {}, "python": {}},
            "slow": {"cpp": {}, "python": {}},
            "slowdown_factors": {},
            "differential_selectivity": {}
        }
        
        # Executar soluções otimizadas (referência)
        print("  📈 Executando soluções otimizadas...")
        
        # C++ Otimizado
        cpp_opt_output, cpp_opt_time, cpp_opt_error = run_solution('./solutions/solution_cpp', test_input)
        case_result["optimized"]["cpp"] = {
            "time": cpp_opt_time,
            "output": cpp_opt_output,
            "status": "error" if cpp_opt_error else "success",
            "error": cpp_opt_error
        }
        
        # Python Otimizado
        py_opt_output, py_opt_time, py_opt_error = run_solution('solutions/solution.py', test_input)
        case_result["optimized"]["python"] = {
            "time": py_opt_time,
            "output": py_opt_output,
            "status": "error" if py_opt_error else "success",
            "error": py_opt_error
        }
        
        # Executar soluções slow
        print("  🐌 Executando soluções slow...")
        
        # C++ Slow
        cpp_slow_output, cpp_slow_time, cpp_slow_error = run_solution('./slow_validation/solutions_slow/slow_solution_cpp', test_input)
        case_result["slow"]["cpp"] = {
            "time": cpp_slow_time,
            "output": cpp_slow_output,
            "status": "error" if cpp_slow_error else "success",
            "error": cpp_slow_error
        }
        
        # Python Slow
        py_slow_output, py_slow_time, py_slow_error = run_solution('slow_validation/solutions_slow/slow_solution.py', test_input)
        case_result["slow"]["python"] = {
            "time": py_slow_time,
            "output": py_slow_output,
            "status": "error" if py_slow_error else "success",
            "error": py_slow_error
        }
        
        # Calcular fatores de slowdown
        if cpp_opt_time and cpp_slow_time:
            case_result["slowdown_factors"]["cpp"] = cpp_slow_time / cpp_opt_time
        
        if py_opt_time and py_slow_time:
            case_result["slowdown_factors"]["python"] = py_slow_time / py_opt_time
        
        # Calcular seletividade diferencial
        if ("cpp" in case_result["slowdown_factors"] and 
            "python" in case_result["slowdown_factors"]):
            cpp_slowdown = case_result["slowdown_factors"]["cpp"]
            py_slowdown = case_result["slowdown_factors"]["python"]
            
            case_result["differential_selectivity"] = {
                "cpp_slowdown": cpp_slowdown,
                "python_slowdown": py_slowdown,
                "selectivity_ratio": py_slowdown / cpp_slowdown if cpp_slowdown > 0 else float('inf'),
                "cpp_tolerance": "high" if cpp_slowdown < 10 else "medium" if cpp_slowdown < 100 else "low",
                "python_tolerance": "high" if py_slowdown < 10 else "medium" if py_slowdown < 100 else "low"
            }
        
        # Relatório do caso
        print(f"    C++ Otimizado: {cpp_opt_time:.4f}s {'✅' if not cpp_opt_error else '❌'}")
        print(f"    Python Otimizado: {py_opt_time:.4f}s {'✅' if not py_opt_error else '❌'}")
        print(f"    C++ Slow: {cpp_slow_time:.4f}s {'✅' if not cpp_slow_error else '❌'}")
        print(f"    Python Slow: {py_slow_time:.4f}s {'✅' if not py_slow_error else '❌'}")
        
        if "cpp" in case_result["slowdown_factors"]:
            print(f"    📊 Slowdown C++: {case_result['slowdown_factors']['cpp']:.2f}x")
        
        if "python" in case_result["slowdown_factors"]:
            print(f"    📊 Slowdown Python: {case_result['slowdown_factors']['python']:.2f}x")
        
        if case_result["differential_selectivity"]:
            ds = case_result["differential_selectivity"]
            print(f"    🎯 Seletividade Diferencial: {ds['selectivity_ratio']:.2f}x")
            print(f"    🎯 Tolerância C++: {ds['cpp_tolerance']}")
            print(f"    🎯 Tolerância Python: {ds['python_tolerance']}")
        
        # Verificar consistência de outputs
        outputs = [cpp_opt_output, py_opt_output, cpp_slow_output, py_slow_output]
        valid_outputs = [out for out in outputs if out is not None]
        
        if len(set(valid_outputs)) > 1:
            print(f"    ⚠️  Outputs inconsistentes detectados!")
        else:
            print(f"    ✅ Outputs consistentes")
        
        results["validation_results"].append(case_result)
    
    # Análise geral da seletividade diferencial
    print(f"\n📊 ANÁLISE GERAL DA SELETIVIDADE DIFERENCIAL")
    print("=" * 50)
    
    successful_cases = [r for r in results["validation_results"] 
                       if r["differential_selectivity"]]
    
    if successful_cases:
        selectivity_ratios = [r["differential_selectivity"]["selectivity_ratio"] 
                            for r in successful_cases 
                            if r["differential_selectivity"]["selectivity_ratio"] != float('inf')]
        
        if selectivity_ratios:
            avg_selectivity = sum(selectivity_ratios) / len(selectivity_ratios)
            max_selectivity = max(selectivity_ratios)
            min_selectivity = min(selectivity_ratios)
            
            print(f"📈 Seletividade Diferencial Média: {avg_selectivity:.2f}x")
            print(f"📈 Seletividade Diferencial Máxima: {max_selectivity:.2f}x")
            print(f"📈 Seletividade Diferencial Mínima: {min_selectivity:.2f}x")
        
        # Contar tolerâncias
        cpp_tolerances = [r["differential_selectivity"]["cpp_tolerance"] for r in successful_cases]
        py_tolerances = [r["differential_selectivity"]["python_tolerance"] for r in successful_cases]
        
        print(f"\n🎯 Distribuição de Tolerância:")
        print(f"   C++ - Alta: {cpp_tolerances.count('high')}, Média: {cpp_tolerances.count('medium')}, Baixa: {cpp_tolerances.count('low')}")
        print(f"   Python - Alta: {py_tolerances.count('high')}, Média: {py_tolerances.count('medium')}, Baixa: {py_tolerances.count('low')}")
        
        # Detectar casos críticos
        timeout_cases = [r for r in results["validation_results"] 
                        if any(r["slow"][lang]["status"] == "error" and "Timeout" in str(r["slow"][lang]["error"]) 
                               for lang in ["cpp", "python"])]
        
        if timeout_cases:
            print(f"\n⏰ Casos com Timeout: {len(timeout_cases)}/{len(results['validation_results'])}")
            for case in timeout_cases:
                print(f"    {case['case_name']}: Timeout detectado")
        
        print(f"\n✅ Casos com Seletividade Válida: {len(successful_cases)}/{len(results['validation_results'])}")
    
    # Salvar resultados
    with open('slow_validation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Resultados salvos em: slow_validation_results.json")
    return True

def main():
    """Função principal"""
    print("🐌 SLOW VALIDATION CHESSBOARD AND QUEENS - BACKTRACKING PROBLEM01")
    print("📋 Protocolo Metodológico Rigoroso - Fase 2.3")
    print("🎯 Foco: Seletividade Diferencial ao Overhead")
    print("=" * 70)
    
    # Verificar estrutura
    required_files = [
        'solutions/solution.cpp',
        'solutions/solution.py',
        'slow_validation/solutions_slow/slow_solution.cpp',
        'slow_validation/solutions_slow/slow_solution.py'
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Arquivo {file_path} não encontrado")
            return False
    
    # Verificar se soluções otimizadas estão compiladas
    if not os.path.exists('./solutions/solution_cpp'):
        print("❌ Solução C++ otimizada não compilada. Execute run_benchmark.py primeiro.")
        return False
    
    # Compilar soluções slow
    print("🔧 Compilando solução C++ slow...")
    if not compile_cpp_slow():
        return False
    print("✅ Compilação C++ slow concluída")
    
    # Executar validação slow
    if not run_slow_validation():
        return False
    
    print("\n🎉 SLOW VALIDATION CONCLUÍDA COM SUCESSO!")
    print("📊 Verifique o arquivo de resultados:")
    print("   - slow_validation_results.json")
    print("\n🔬 Seletividade Diferencial quantificada com precisão!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
