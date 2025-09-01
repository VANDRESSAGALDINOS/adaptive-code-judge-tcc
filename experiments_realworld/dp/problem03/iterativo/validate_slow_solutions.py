#!/usr/bin/env python3
"""
Slow Validation Script para Two Sets II - DP Problem03 Iterativo
Seguindo Protocolo Metodológico Rigoroso
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

def generate_test_case(n):
    """Gera caso de teste para Two Sets II"""
    return str(n)

def run_slow_validation():
    """Executa validação das soluções slow"""
    print("🐌 EXECUTANDO SLOW VALIDATION - Two Sets II Iterativo")
    print("=" * 70)
    
    # Mesmos casos críticos usados no recursivo para comparação
    critical_cases = [
        50,   # Caso pequeno-médio (trivial)
        100,  # Caso de calibração (complexo)
        150,  # Caso médio (trivial)
        200,  # Caso onde injustiça aparece (complexo)
        250,  # Caso crítico (trivial)
        300   # Caso de alta injustiça (complexo)
    ]
    
    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "implementation": "iterativo",
        "extra_work": 2000,
        "test_cases": critical_cases,
        "validation_results": []
    }
    
    print(f"🎯 Casos Críticos: {critical_cases}")
    print(f"⚙️  EXTRA_WORK: {results['extra_work']}")
    print(f"⏱️  Timeout: 15s por execução")
    
    for n in critical_cases:
        print(f"\n🔍 Validando n = {n}")
        total_sum = n * (n + 1) // 2
        case_type = "Par (Complexo)" if total_sum % 2 == 0 else "Ímpar (Trivial)"
        print(f"   Soma: {total_sum} - {case_type}")
        
        test_input = generate_test_case(n)
        
        case_result = {
            "n": n,
            "total_sum": total_sum,
            "case_type": case_type,
            "optimized": {"cpp": {}, "python": {}},
            "slow": {"cpp": {}, "python": {}},
            "slowdown_factors": {}
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
        
        # Relatório do caso
        print(f"    C++ Otimizado: {cpp_opt_time:.4f}s {'✅' if not cpp_opt_error else '❌'}")
        print(f"    Python Otimizado: {py_opt_time:.4f}s {'✅' if not py_opt_error else '❌'}")
        print(f"    C++ Slow: {cpp_slow_time:.4f}s {'✅' if not cpp_slow_error else '❌'}")
        print(f"    Python Slow: {py_slow_time:.4f}s {'✅' if not py_slow_error else '❌'}")
        
        if "cpp" in case_result["slowdown_factors"]:
            print(f"    📊 Slowdown C++: {case_result['slowdown_factors']['cpp']:.2f}x")
        
        if "python" in case_result["slowdown_factors"]:
            print(f"    📊 Slowdown Python: {case_result['slowdown_factors']['python']:.2f}x")
        
        # Verificar consistência de outputs
        outputs = [cpp_opt_output, py_opt_output, cpp_slow_output, py_slow_output]
        valid_outputs = [out for out in outputs if out is not None]
        
        if len(set(valid_outputs)) > 1:
            print(f"    ⚠️  Outputs inconsistentes detectados!")
        else:
            print(f"    ✅ Outputs consistentes")
        
        results["validation_results"].append(case_result)
    
    # Análise geral
    print(f"\n📊 ANÁLISE GERAL DA SLOW VALIDATION")
    print("=" * 50)
    
    successful_cases = [r for r in results["validation_results"] 
                       if all(r["slow"][lang]["status"] == "success" for lang in ["cpp", "python"])]
    
    if successful_cases:
        cpp_slowdowns = [r["slowdown_factors"]["cpp"] for r in successful_cases if "cpp" in r["slowdown_factors"]]
        py_slowdowns = [r["slowdown_factors"]["python"] for r in successful_cases if "python" in r["slowdown_factors"]]
        
        if cpp_slowdowns:
            avg_cpp_slowdown = sum(cpp_slowdowns) / len(cpp_slowdowns)
            print(f"📈 Slowdown Médio C++: {avg_cpp_slowdown:.2f}x")
        
        if py_slowdowns:
            avg_py_slowdown = sum(py_slowdowns) / len(py_slowdowns)
            print(f"📈 Slowdown Médio Python: {avg_py_slowdown:.2f}x")
        
        # Detectar casos que excedem limites realistas
        timeout_cases = [r for r in results["validation_results"] 
                        if any(r["slow"][lang]["status"] == "error" and "Timeout" in str(r["slow"][lang]["error"]) 
                               for lang in ["cpp", "python"])]
        
        if timeout_cases:
            print(f"⏰ Casos com Timeout: {len(timeout_cases)}/{len(results['validation_results'])}")
            for case in timeout_cases:
                print(f"    n={case['n']}: Timeout detectado")
        
        print(f"✅ Casos Válidos: {len(successful_cases)}/{len(results['validation_results'])}")
    
    # Salvar resultados
    with open('slow_validation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Resultados salvos em: slow_validation_results.json")
    return True

def main():
    """Função principal"""
    print("🐌 SLOW VALIDATION TWO SETS II - DP PROBLEM03 ITERATIVO")
    print("📋 Protocolo Metodológico Rigoroso - Fase 2.3")
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
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
