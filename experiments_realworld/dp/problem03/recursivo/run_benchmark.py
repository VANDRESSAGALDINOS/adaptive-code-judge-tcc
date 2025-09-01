#!/usr/bin/env python3
"""
Benchmark Script para Two Sets II - DP Problem03 Recursivo
Seguindo Protocolo Metodológico Rigoroso
"""

import subprocess
import time
import json
import os
import sys
from pathlib import Path

def compile_cpp():
    """Compila a solução C++"""
    try:
        result = subprocess.run([
            'g++', '-O2', '-std=c++17', 
            'solutions/solution.cpp', 
            '-o', 'solutions/solution_cpp'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            print(f"Erro na compilação C++: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Erro ao compilar C++: {e}")
        return False

def run_solution(executable, input_data, timeout=5):
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

def run_calibration():
    """Executa calibração com caso representativo"""
    print("🔬 EXECUTANDO CALIBRAÇÃO - Two Sets II Recursivo")
    print("=" * 60)
    
    # Caso representativo baseado nos resultados CSES
    # n=100 é um bom caso médio que não causa TLE mas é computacionalmente significativo
    calibration_case = 100
    test_input = generate_test_case(calibration_case)
    
    print(f"📊 Caso de Calibração: n = {calibration_case}")
    print(f"📊 Complexidade Esperada: O(n×sum) = O({calibration_case}×{calibration_case*(calibration_case+1)//4})")
    
    results = {
        "calibration_case": calibration_case,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "cpp": {"times": [], "outputs": []},
        "python": {"times": [], "outputs": []}
    }
    
    # Múltiplas execuções para estatística robusta
    num_runs = 10
    
    print(f"\n🔄 Executando {num_runs} repetições...")
    
    for i in range(num_runs):
        print(f"  Execução {i+1}/{num_runs}", end=" ")
        
        # C++
        cpp_output, cpp_time, cpp_error = run_solution('./solutions/solution_cpp', test_input)
        if cpp_error:
            print(f"❌ C++ Error: {cpp_error}")
            continue
        
        results["cpp"]["times"].append(cpp_time)
        results["cpp"]["outputs"].append(cpp_output)
        
        # Python
        py_output, py_time, py_error = run_solution('solutions/solution.py', test_input)
        if py_error:
            print(f"❌ Python Error: {py_error}")
            continue
        
        results["python"]["times"].append(py_time)
        results["python"]["outputs"].append(py_output)
        
        # Verificar consistência
        if cpp_output != py_output:
            print(f"⚠️  Outputs diferentes: C++={cpp_output}, Python={py_output}")
        else:
            print("✅")
    
    # Calcular estatísticas
    if results["cpp"]["times"] and results["python"]["times"]:
        cpp_times = results["cpp"]["times"]
        py_times = results["python"]["times"]
        
        results["cpp"]["median_time"] = sorted(cpp_times)[len(cpp_times)//2]
        results["cpp"]["avg_time"] = sum(cpp_times) / len(cpp_times)
        results["cpp"]["min_time"] = min(cpp_times)
        results["cpp"]["max_time"] = max(cpp_times)
        
        results["python"]["median_time"] = sorted(py_times)[len(py_times)//2]
        results["python"]["avg_time"] = sum(py_times) / len(py_times)
        results["python"]["min_time"] = min(py_times)
        results["python"]["max_time"] = max(py_times)
        
        # Fator de ajuste
        adjustment_factor = results["python"]["median_time"] / results["cpp"]["median_time"]
        results["adjustment_factor"] = adjustment_factor
        
        print(f"\n📈 RESULTADOS DA CALIBRAÇÃO:")
        print(f"   C++ Mediano: {results['cpp']['median_time']:.4f}s")
        print(f"   Python Mediano: {results['python']['median_time']:.4f}s")
        print(f"   Fator de Ajuste: {adjustment_factor:.2f}x")
        
        # Salvar resultados
        with open('calibration_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Resultados salvos em: calibration_results.json")
        return True
    else:
        print("❌ Falha na calibração - sem dados válidos")
        return False

def run_validation():
    """Executa validação com múltiplos casos"""
    print("\n🔬 EXECUTANDO VALIDAÇÃO - Múltiplos Casos")
    print("=" * 60)
    
    # Casos de teste baseados na análise CSES
    # Incluindo casos que causaram TLE e casos que passaram
    test_cases = [
        10,   # Caso pequeno - sempre passa
        50,   # Caso médio-pequeno
        100,  # Caso médio (calibração)
        200,  # Caso médio-grande
        300,  # Caso grande - pode causar diferenças
        400,  # Caso muito grande - próximo aos limites CSES
        450   # Caso crítico - próximo ao n=500 máximo
    ]
    
    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "test_cases": []
    }
    
    for n in test_cases:
        print(f"\n📊 Testando n = {n}")
        test_input = generate_test_case(n)
        
        case_result = {
            "n": n,
            "cpp": {"time": None, "output": None, "status": "unknown"},
            "python": {"time": None, "output": None, "status": "unknown"}
        }
        
        # C++
        cpp_output, cpp_time, cpp_error = run_solution('./solutions/solution_cpp', test_input, timeout=10)
        if cpp_error:
            case_result["cpp"]["status"] = f"error: {cpp_error}"
            print(f"   C++: ❌ {cpp_error}")
        else:
            case_result["cpp"]["time"] = cpp_time
            case_result["cpp"]["output"] = cpp_output
            case_result["cpp"]["status"] = "success"
            print(f"   C++: ✅ {cpp_time:.4f}s")
        
        # Python
        py_output, py_time, py_error = run_solution('solutions/solution.py', test_input, timeout=10)
        if py_error:
            case_result["python"]["status"] = f"error: {py_error}"
            print(f"   Python: ❌ {py_error}")
        else:
            case_result["python"]["time"] = py_time
            case_result["python"]["output"] = py_output
            case_result["python"]["status"] = "success"
            print(f"   Python: ✅ {py_time:.4f}s")
        
        # Verificar consistência
        if (case_result["cpp"]["output"] and case_result["python"]["output"] and 
            case_result["cpp"]["output"] != case_result["python"]["output"]):
            print(f"   ⚠️  Outputs diferentes!")
        
        # Calcular ratio se ambos executaram
        if (case_result["cpp"]["time"] and case_result["python"]["time"]):
            ratio = case_result["python"]["time"] / case_result["cpp"]["time"]
            case_result["performance_ratio"] = ratio
            print(f"   📊 Ratio Python/C++: {ratio:.2f}x")
        
        results["test_cases"].append(case_result)
    
    # Salvar resultados
    with open('validation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Resultados salvos em: validation_results.json")
    return True

def main():
    """Função principal"""
    print("🚀 BENCHMARK TWO SETS II - DP PROBLEM03 RECURSIVO")
    print("📋 Protocolo Metodológico Rigoroso - Fase 2")
    print("=" * 70)
    
    # Verificar estrutura
    if not os.path.exists('solutions/solution.cpp'):
        print("❌ Arquivo solutions/solution.cpp não encontrado")
        return False
    
    if not os.path.exists('solutions/solution.py'):
        print("❌ Arquivo solutions/solution.py não encontrado")
        return False
    
    # Compilar C++
    print("🔧 Compilando solução C++...")
    if not compile_cpp():
        return False
    print("✅ Compilação C++ concluída")
    
    # Executar calibração
    if not run_calibration():
        return False
    
    # Executar validação
    if not run_validation():
        return False
    
    print("\n🎉 BENCHMARK CONCLUÍDO COM SUCESSO!")
    print("📊 Verifique os arquivos de resultados:")
    print("   - calibration_results.json")
    print("   - validation_results.json")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
