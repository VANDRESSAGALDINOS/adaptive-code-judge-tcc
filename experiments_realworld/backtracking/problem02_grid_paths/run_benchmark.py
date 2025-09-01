#!/usr/bin/env python3

import subprocess
import time
import json
import os
from pathlib import Path

class GridPathsBenchmark:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.solutions_dir = self.base_dir / "solutions"
        self.results = {
            "calibration": {},
            "validation": {},
            "metadata": {
                "problem": "Grid Paths (CSES 1625)",
                "category": "Backtracking",
                "implementation": "Recursive",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    
    def compile_cpp(self):
        """Compila a solução C++"""
        cpp_file = self.solutions_dir / "solution.cpp"
        executable = self.solutions_dir / "solution_cpp"
        
        cmd = ["g++", "-O2", "-std=c++17", str(cpp_file), "-o", str(executable)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Erro na compilação C++: {result.stderr}")
        
        return executable
    
    def run_solution(self, executable, input_data, timeout=10):
        """Executa uma solução com input específico"""
        try:
            start_time = time.time()
            result = subprocess.run(
                [str(executable)],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            end_time = time.time()
            
            if result.returncode != 0:
                return None, f"Runtime error: {result.stderr}"
            
            return {
                "output": result.stdout.strip(),
                "time": end_time - start_time,
                "success": True
            }, None
            
        except subprocess.TimeoutExpired:
            return None, "Timeout"
        except Exception as e:
            return None, str(e)
    
    def run_python_solution(self, input_data, timeout=10):
        """Executa a solução Python"""
        python_file = self.solutions_dir / "solution.py"
        
        try:
            start_time = time.time()
            result = subprocess.run(
                ["python3", str(python_file)],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            end_time = time.time()
            
            if result.returncode != 0:
                return None, f"Runtime error: {result.stderr}"
            
            return {
                "output": result.stdout.strip(),
                "time": end_time - start_time,
                "success": True
            }, None
            
        except subprocess.TimeoutExpired:
            return None, "Timeout"
        except Exception as e:
            return None, str(e)
    
    def generate_test_cases(self):
        """Gera casos de teste para calibração"""
        # ATENÇÃO: Grid Paths é computacionalmente muito pesado
        # Vamos usar casos mais simples para calibração
        test_cases = [
            {
                "name": "simple_path_1",
                "input": "DDDDDDRRRRRRDDDDDDLLLLLLDDDDDDRRRRRRDDDDDDLLLLLL",
                "expected": "0",  # Path específico, deve dar 0 ou 1
                "description": "Caminho específico simples"
            },
            {
                "name": "simple_path_2", 
                "input": "DRDRDRDRDRDRDRDRDRDRDRDRDRDRDRDRDRDRDRDRDRDRDRDR",
                "expected": "0",  # Path específico
                "description": "Padrão alternado"
            },
            {
                "name": "few_wildcards",
                "input": "DDDDDDRRRRRRDDDDDLLLLLLDDDDDRRRRRRDDDDDLLLLL?",
                "expected": "unknown",  # Apenas 1 wildcard
                "description": "Apenas 1 wildcard no final"
            }
        ]
        
        return test_cases
    
    def run_calibration(self):
        """Executa calibração com casos simples"""
        print("🔧 Iniciando calibração Grid Paths...")
        
        # Compilar C++
        try:
            cpp_executable = self.compile_cpp()
            print("✅ C++ compilado com sucesso")
        except Exception as e:
            print(f"❌ Erro na compilação C++: {e}")
            return
        
        test_cases = self.generate_test_cases()
        
        for test_case in test_cases:
            print(f"\n📋 Testando: {test_case['name']}")
            
            # Testar C++
            cpp_result, cpp_error = self.run_solution(cpp_executable, test_case["input"], timeout=5)
            if cpp_error:
                print(f"❌ C++ falhou: {cpp_error}")
                continue
            
            # Testar Python
            py_result, py_error = self.run_python_solution(test_case["input"], timeout=10)
            if py_error:
                print(f"❌ Python falhou: {py_error}")
                continue
            
            # Verificar consistência
            if cpp_result["output"] == py_result["output"]:
                print(f"✅ Resultados consistentes: {cpp_result['output']}")
                print(f"⏱️  C++: {cpp_result['time']:.4f}s | Python: {py_result['time']:.4f}s")
                
                # Calcular fator de ajuste
                if cpp_result["time"] > 0:
                    adjustment_factor = py_result["time"] / cpp_result["time"]
                    print(f"📊 Fator de ajuste: {adjustment_factor:.2f}x")
                    
                    self.results["calibration"][test_case["name"]] = {
                        "cpp_time": cpp_result["time"],
                        "python_time": py_result["time"],
                        "adjustment_factor": adjustment_factor,
                        "output": cpp_result["output"]
                    }
            else:
                print(f"❌ Resultados inconsistentes!")
                print(f"   C++: {cpp_result['output']}")
                print(f"   Python: {py_result['output']}")
    
    def run_validation(self):
        """Executa validação com casos mais complexos"""
        print("\n🧪 Iniciando validação Grid Paths...")
        print("⚠️  AVISO: Este problema é computacionalmente muito pesado!")
        print("⚠️  Casos complexos podem demorar muito ou dar timeout!")
        
        # Casos de validação mais simples
        validation_cases = [
            {
                "name": "two_wildcards",
                "input": "DDDDDDRRRRRRDDDDDDLLLLLLDDDDDDRRRRRRDDDDDDLLLLL??",
                "timeout": 30,
                "description": "2 wildcards no final"
            }
        ]
        
        cpp_executable = self.solutions_dir / "solution_cpp"
        
        for test_case in validation_cases:
            print(f"\n📋 Validando: {test_case['name']}")
            
            # Testar C++
            cpp_result, cpp_error = self.run_solution(
                cpp_executable, 
                test_case["input"], 
                timeout=test_case["timeout"]
            )
            
            if cpp_error:
                print(f"❌ C++ falhou: {cpp_error}")
                continue
            
            # Testar Python (timeout maior)
            py_result, py_error = self.run_python_solution(
                test_case["input"], 
                timeout=test_case["timeout"] * 2
            )
            
            if py_error:
                print(f"❌ Python falhou: {py_error}")
                # Ainda salvar resultado C++
                self.results["validation"][test_case["name"]] = {
                    "cpp_time": cpp_result["time"],
                    "python_time": None,
                    "python_error": py_error,
                    "output": cpp_result["output"]
                }
                continue
            
            # Ambos funcionaram
            print(f"✅ Ambos executaram com sucesso")
            print(f"⏱️  C++: {cpp_result['time']:.4f}s | Python: {py_result['time']:.4f}s")
            
            if cpp_result["output"] == py_result["output"]:
                print(f"✅ Resultados consistentes: {cpp_result['output']}")
            else:
                print(f"❌ Resultados inconsistentes!")
                print(f"   C++: {cpp_result['output']}")
                print(f"   Python: {py_result['output']}")
            
            self.results["validation"][test_case["name"]] = {
                "cpp_time": cpp_result["time"],
                "python_time": py_result["time"],
                "cpp_output": cpp_result["output"],
                "python_output": py_result["output"],
                "consistent": cpp_result["output"] == py_result["output"]
            }
    
    def save_results(self):
        """Salva os resultados em arquivo JSON"""
        results_file = self.base_dir / "benchmark_results.json"
        
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Resultados salvos em: {results_file}")
    
    def run_full_benchmark(self):
        """Executa benchmark completo"""
        print("🚀 Iniciando benchmark Grid Paths (CSES 1625)")
        print("⚠️  ATENÇÃO: Este é um problema extremamente pesado computacionalmente!")
        
        self.run_calibration()
        self.run_validation()
        self.save_results()
        
        print("\n🎯 Benchmark concluído!")
        print("📊 Verifique benchmark_results.json para detalhes completos")

if __name__ == "__main__":
    benchmark = GridPathsBenchmark()
    benchmark.run_full_benchmark()
