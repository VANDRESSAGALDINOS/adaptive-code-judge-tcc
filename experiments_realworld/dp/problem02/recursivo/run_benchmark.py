#!/usr/bin/env python3
"""
CSES 1638 - Grid Paths I (DP Recursivo) Benchmark Script
Adaptado dos experimentos de grafos, seguindo metodologia estabelecida
"""

import argparse
import json
import os
import subprocess
import tempfile
import time
import statistics
from datetime import datetime
from pathlib import Path
import sys

class CSES1638GridPathsRecursiveBenchmark:
    """Benchmark executor para CSES 1638 Grid Paths I DP Recursivo seguindo protocolo científico."""
    
    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir or ".")
        self.solutions_dir = self.base_dir / "solutions"
        self.tests_dir = self.base_dir / ".." / "tests_cses"  # Pasta compartilhada
        self.results_dir = self.base_dir / "results" 
        self.results_dir.mkdir(exist_ok=True)
        
        # Docker configuration
        self.cpp_image = "gcc:latest"
        self.python_image = "python:3.11-slim"
        
        # Test case categorization para Grid Paths I
        # Será definido após submissões CSES
        self.critical_cases = []  # A ser preenchido
        self.control_cases = []   # A ser preenchido
        self.problematic_cases = []  # A ser preenchido
        
    def setup_docker_images(self):
        """Garantir que imagens Docker estão disponíveis."""
        print("Configurando ambiente Docker...")
        
        for image in [self.cpp_image, self.python_image]:
            try:
                result = subprocess.run(
                    ["docker", "image", "inspect", image],
                    capture_output=True, text=True, check=False
                )
                if result.returncode != 0:
                    print(f"Baixando {image}...")
                    subprocess.run(["docker", "pull", image], check=True)
                else:
                    print(f"✓ {image} disponível")
            except subprocess.CalledProcessError as e:
                print(f"Erro ao configurar {image}: {e}")
                return False
        return True

    def get_test_cases(self):
        """Obter lista de test cases disponíveis."""
        if not self.tests_dir.exists():
            print(f"Erro: Diretório de testes não encontrado: {self.tests_dir}")
            return []
        
        test_files = sorted([f for f in self.tests_dir.glob("*.in")])
        test_numbers = [int(f.stem) for f in test_files]
        print(f"Test cases encontrados: {test_numbers}")
        return test_numbers

    def compile_cpp(self, source_path, output_path):
        """Compilar solução C++ usando Docker."""
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{source_path.parent.absolute()}:/workspace",
            "-w", "/workspace",
            self.cpp_image,
            "g++", "-std=c++17", "-O1", "-o", output_path.name, source_path.name
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Erro na compilação C++: {result.stderr}")
            return False
        return True

    def execute_solution(self, solution_path, test_input, time_limit=5.0, language="cpp"):
        """Executar solução com input específico e medir tempo."""
        
        if language == "cpp":
            if not solution_path.exists():
                print(f"Erro: Executável não encontrado: {solution_path}")
                return {"status": "COMPILATION_ERROR", "time": 0, "output": "", "error": "Executable not found"}
            
            cmd = [
                "docker", "run", "--rm", "-i",
                "--memory=512m", "--cpus=1.0",
                "-v", f"{solution_path.parent.absolute()}:/workspace",
                "-w", "/workspace",
                self.cpp_image,
                f"./{solution_path.name}"
            ]
        
        elif language == "python":
            cmd = [
                "docker", "run", "--rm", "-i",
                "--memory=512m", "--cpus=1.0",
                "-v", f"{solution_path.parent.absolute()}:/workspace",
                "-w", "/workspace", 
                self.python_image,
                "python", solution_path.name
            ]
        
        try:
            start_time = time.time()
            result = subprocess.run(
                cmd, input=test_input, text=True, 
                capture_output=True, timeout=time_limit
            )
            end_time = time.time()
            execution_time = end_time - start_time
            
            if result.returncode == 0:
                return {
                    "status": "ACCEPTED",
                    "time": execution_time,
                    "output": result.stdout.strip(),
                    "error": result.stderr.strip()
                }
            else:
                return {
                    "status": "RUNTIME_ERROR", 
                    "time": execution_time,
                    "output": result.stdout.strip(),
                    "error": result.stderr.strip()
                }
                
        except subprocess.TimeoutExpired:
            return {"status": "TLE", "time": time_limit, "output": "", "error": "Time limit exceeded"}
        except Exception as e:
            return {"status": "SYSTEM_ERROR", "time": 0, "output": "", "error": str(e)}

    def validate_output(self, actual, expected):
        """Validar se output está correto."""
        return actual.strip() == expected.strip()

    def run_calibration(self, test_case, repetitions=15, time_limit=5.0):
        """Executar fase de calibração em um test case específico."""
        print(f"\n=== CALIBRAÇÃO - Test Case {test_case} ===")
        
        # Carregar test case
        input_file = self.tests_dir / f"{test_case}.in"
        output_file = self.tests_dir / f"{test_case}.out"
        
        if not input_file.exists() or not output_file.exists():
            print(f"Erro: Arquivos de teste não encontrados para caso {test_case}")
            return None
        
        test_input = input_file.read_text()
        expected_output = output_file.read_text().strip()
        
        # Compilar C++
        cpp_source = self.solutions_dir / "solution.cpp"
        cpp_exec = self.solutions_dir / "solution_cpp"
        
        if not self.compile_cpp(cpp_source, cpp_exec):
            print("Falha na compilação C++")
            return None
        
        # Python source
        python_source = self.solutions_dir / "solution.py"
        
        results = {"test_case": test_case, "repetitions": repetitions}
        
        # Executar C++ repetições
        print("Executando C++...")
        cpp_times = []
        cpp_success = 0
        
        for i in range(repetitions):
            result = self.execute_solution(cpp_exec, test_input, time_limit, "cpp")
            print(f"C++ #{i+1}: {result['status']} {result['time']:.3f}s")
            
            if result["status"] == "ACCEPTED" and self.validate_output(result["output"], expected_output):
                cpp_times.append(result["time"])
                cpp_success += 1
            elif result["status"] == "TLE":
                cpp_times.append(time_limit)
        
        # Executar Python repetições
        print("Executando Python...")
        python_times = []
        python_success = 0
        
        for i in range(repetitions):
            result = self.execute_solution(python_source, test_input, time_limit, "python")
            print(f"Python #{i+1}: {result['status']} {result['time']:.3f}s")
            
            if result["status"] == "ACCEPTED" and self.validate_output(result["output"], expected_output):
                python_times.append(result["time"])
                python_success += 1
            elif result["status"] == "TLE":
                python_times.append(time_limit)
            elif result["status"] == "RUNTIME_ERROR" and "RecursionError" in result["error"]:
                print(f"Python #{i+1}: RecursionError detectado")
                # Para RecursionError, não incluímos tempo na estatística
        
        # Calcular estatísticas
        results["cpp"] = {
            "times": cpp_times,
            "success_count": cpp_success,
            "success_rate": cpp_success / repetitions,
            "median_time": statistics.median(cpp_times) if cpp_times else 0,
            "mean_time": statistics.mean(cpp_times) if cpp_times else 0
        }
        
        results["python"] = {
            "times": python_times,
            "success_count": python_success, 
            "success_rate": python_success / repetitions,
            "median_time": statistics.median(python_times) if python_times else 0,
            "mean_time": statistics.mean(python_times) if python_times else 0
        }
        
        # Calcular fator de ajuste se ambos tiveram sucesso
        if cpp_times and python_times:
            adjustment_factor = statistics.median(python_times) / statistics.median(cpp_times)
            results["adjustment_factor"] = adjustment_factor
            print(f"Fator de ajuste: {adjustment_factor:.2f}x")
        else:
            results["adjustment_factor"] = None
            print("Impossível calcular fator de ajuste - falhas sistemáticas")
        
        return results

    def run_validation(self, test_cases, adjustment_factor, repetitions=3, base_time_limit=5.0):
        """Executar fase de validação com fator de ajuste."""
        print(f"\n=== VALIDAÇÃO - Fator {adjustment_factor:.2f}x ===")
        
        results = {
            "adjustment_factor": adjustment_factor,
            "base_time_limit": base_time_limit,
            "adaptive_time_limit": base_time_limit * adjustment_factor,
            "test_results": {}
        }
        
        # Compilar C++
        cpp_source = self.solutions_dir / "solution.cpp"
        cpp_exec = self.solutions_dir / "solution_cpp"
        
        if not self.compile_cpp(cpp_source, cpp_exec):
            print("Falha na compilação C++")
            return None
        
        python_source = self.solutions_dir / "solution.py"
        
        for test_case in test_cases:
            print(f"\nTeste {test_case}:")
            
            # Carregar test case
            input_file = self.tests_dir / f"{test_case}.in"
            output_file = self.tests_dir / f"{test_case}.out"
            
            if not input_file.exists() or not output_file.exists():
                print(f"Arquivos não encontrados para teste {test_case}")
                continue
            
            test_input = input_file.read_text()
            expected_output = output_file.read_text().strip()
            
            case_results = {"test_case": test_case, "repetitions": []}
            
            for rep in range(repetitions):
                print(f"  Repetição {rep+1}:")
                
                # C++ com limite tradicional
                cpp_result = self.execute_solution(cpp_exec, test_input, base_time_limit, "cpp")
                cpp_traditional = "ACCEPTED" if cpp_result["status"] == "ACCEPTED" and self.validate_output(cpp_result["output"], expected_output) else cpp_result["status"]
                
                # Python com limite tradicional
                python_result = self.execute_solution(python_source, test_input, base_time_limit, "python")
                python_traditional = "ACCEPTED" if python_result["status"] == "ACCEPTED" and self.validate_output(python_result["output"], expected_output) else python_result["status"]
                
                # Python com limite adaptativo
                python_adaptive_result = self.execute_solution(python_source, test_input, results["adaptive_time_limit"], "python")
                python_adaptive = "ACCEPTED" if python_adaptive_result["status"] == "ACCEPTED" and self.validate_output(python_adaptive_result["output"], expected_output) else python_adaptive_result["status"]
                
                rep_result = {
                    "cpp_traditional": {"status": cpp_traditional, "time": cpp_result["time"]},
                    "python_traditional": {"status": python_traditional, "time": python_result["time"]},
                    "python_adaptive": {"status": python_adaptive, "time": python_adaptive_result["time"]}
                }
                
                case_results["repetitions"].append(rep_result)
                print(f"    C++ tradicional: {cpp_traditional} ({cpp_result['time']:.3f}s)")
                print(f"    Python tradicional: {python_traditional} ({python_result['time']:.3f}s)")
                print(f"    Python adaptativo: {python_adaptive} ({python_adaptive_result['time']:.3f}s)")
            
            results["test_results"][test_case] = case_results
        
        return results

def main():
    parser = argparse.ArgumentParser(description="CSES 1635 DP Recursivo Benchmark")
    parser.add_argument("--calibration-case", type=int, default=8, help="Test case para calibração")
    parser.add_argument("--validation-cases", nargs="+", type=int, default=[4, 8, 11], help="Test cases para validação")
    parser.add_argument("--calibration-reps", type=int, default=15, help="Repetições na calibração")
    parser.add_argument("--validation-reps", type=int, default=3, help="Repetições na validação")
    parser.add_argument("--time-limit", type=float, default=5.0, help="Limite de tempo base (segundos)")
    
    args = parser.parse_args()
    
    benchmark = CSES1638GridPathsRecursiveBenchmark()
    
    if not benchmark.setup_docker_images():
        print("Falha na configuração do Docker")
        return 1
    
    # Verificar test cases disponíveis
    available_tests = benchmark.get_test_cases()
    if not available_tests:
        print("Nenhum test case encontrado")
        return 1
    
    # Fase de calibração
    print("INICIANDO BENCHMARK CSES 1635 - DP RECURSIVO")
    calibration_result = benchmark.run_calibration(
        args.calibration_case, args.calibration_reps, args.time_limit
    )
    
    if not calibration_result or calibration_result["adjustment_factor"] is None:
        print("Calibração falhou - não é possível calcular fator de ajuste")
        return 1
    
    # Salvar resultado da calibração
    calibration_file = benchmark.results_dir / f"calibration_case{args.calibration_case}.json"
    with open(calibration_file, 'w') as f:
        json.dump(calibration_result, f, indent=2)
    print(f"Calibração salva em: {calibration_file}")
    
    # Fase de validação
    validation_result = benchmark.run_validation(
        args.validation_cases, calibration_result["adjustment_factor"],
        args.validation_reps, args.time_limit
    )
    
    if validation_result:
        validation_file = benchmark.results_dir / "validation_results.json"
        with open(validation_file, 'w') as f:
            json.dump(validation_result, f, indent=2)
        print(f"Validação salva em: {validation_file}")
    
    print("\nBenchmark concluído!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
