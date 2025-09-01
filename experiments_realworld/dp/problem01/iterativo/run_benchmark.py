#!/usr/bin/env python3
"""
CSES 1635 - Coin Combinations I (DP Iterativo) Benchmark Script
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

class CSES1635IterativeBenchmark:
    """Benchmark executor para CSES 1635 DP Iterativo seguindo protocolo científico."""
    
    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir or ".")
        self.solutions_dir = self.base_dir / "solutions"
        self.tests_dir = self.base_dir / ".." / "tests_cses"  # Pasta compartilhada
        self.results_dir = self.base_dir / "results" 
        self.results_dir.mkdir(exist_ok=True)
        
        # Docker configuration
        self.cpp_image = "gcc:latest"
        self.python_image = "python:3.11-slim"
        
        # Critical cases identificados pela validação CSES
        self.critical_cases = [4, 5, 8, 11, 12]  # Cases que causaram TLE Python
        self.control_cases = [1, 3, 6, 7, 9, 10, 13]  # Cases funcionais
        
    def check_docker_images(self):
        """Verificar disponibilidade das imagens Docker."""
        print("Configurando ambiente Docker...")
        
        for image in [self.cpp_image, self.python_image]:
            result = subprocess.run(
                ["docker", "image", "inspect", image], 
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print(f"✓ {image} disponível")
            else:
                print(f"⚠ Baixando {image}...")
                subprocess.run(["docker", "pull", image], check=True)

    def get_test_cases(self):
        """Listar test cases disponíveis."""
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
            "g++", "-std=c++17", "-O2", "-o", output_path.name, source_path.name
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
            execution_time = time.time() - start_time
            
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
            return {
                "status": "TLE",
                "time": time_limit,
                "output": "",
                "error": "Time limit exceeded"
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "time": 0,
                "output": "",
                "error": str(e)
            }

    def load_test_case(self, test_number):
        """Carregar input e output esperado de um test case."""
        input_file = self.tests_dir / f"{test_number}.in"
        output_file = self.tests_dir / f"{test_number}.out"
        
        if not input_file.exists() or not output_file.exists():
            return None, None
            
        test_input = input_file.read_text().strip()
        expected_output = output_file.read_text().strip()
        
        return test_input, expected_output

    def run_calibration(self, test_case, repetitions, time_limit):
        """Executar fase de calibração para calcular fator de ajuste."""
        print(f"\n=== CALIBRAÇÃO - Test Case {test_case} ===")
        
        # Preparar soluções
        cpp_source = self.solutions_dir / "solution.cpp"
        cpp_binary = self.solutions_dir / "solution_cpp"
        python_source = self.solutions_dir / "solution.py"
        
        # Compilar C++
        if not self.compile_cpp(cpp_source, cpp_binary):
            print("Falha na compilação C++")
            return None
        
        # Carregar test case
        test_input, expected_output = self.load_test_case(test_case)
        if test_input is None:
            print(f"Test case {test_case} não encontrado")
            return None
        
        # Executar C++
        print("Executando C++...")
        cpp_times = []
        cpp_success = 0
        
        for i in range(repetitions):
            result = self.execute_solution(cpp_binary, test_input, time_limit, "cpp")
            print(f"C++ #{i+1}: {result['status']} {result['time']:.3f}s")
            
            if result['status'] == 'ACCEPTED':
                cpp_times.append(result['time'])
                cpp_success += 1
        
        # Executar Python
        print("Executando Python...")
        python_times = []
        python_success = 0
        
        for i in range(repetitions):
            result = self.execute_solution(python_source, test_input, time_limit, "python")
            print(f"Python #{i+1}: {result['status']} {result['time']:.3f}s")
            
            if result['status'] == 'ACCEPTED':
                python_times.append(result['time'])
                python_success += 1
        
        # Calcular fator de ajuste
        if not cpp_times or not python_times:
            print("Impossível calcular fator de ajuste - falhas sistemáticas")
            return None
        
        cpp_median = statistics.median(cpp_times)
        python_median = statistics.median(python_times)
        adjustment_factor = python_median / cpp_median
        
        print(f"Fator de ajuste: {adjustment_factor:.2f}x")
        
        # Salvar resultados da calibração
        calibration_data = {
            "test_case": test_case,
            "repetitions": repetitions,
            "cpp": {
                "times": cpp_times,
                "success_count": cpp_success,
                "success_rate": cpp_success / repetitions,
                "median_time": cpp_median,
                "mean_time": statistics.mean(cpp_times)
            },
            "python": {
                "times": python_times,
                "success_count": python_success,
                "success_rate": python_success / repetitions,
                "median_time": python_median,
                "mean_time": statistics.mean(python_times)
            },
            "adjustment_factor": adjustment_factor
        }
        
        calibration_file = self.results_dir / f"calibration_case{test_case}.json"
        with open(calibration_file, 'w') as f:
            json.dump(calibration_data, f, indent=2)
        
        print(f"Calibração salva em: {calibration_file}")
        return adjustment_factor

    def run_validation(self, test_cases, repetitions, time_limit, adjustment_factor):
        """Executar fase de validação em múltiplos test cases."""
        print(f"\n=== VALIDAÇÃO - Fator {adjustment_factor:.2f}x ===")
        
        # Preparar soluções
        cpp_source = self.solutions_dir / "solution.cpp"
        cpp_binary = self.solutions_dir / "solution_cpp"
        python_source = self.solutions_dir / "solution.py"
        
        # Compilar C++
        if not self.compile_cpp(cpp_source, cpp_binary):
            print("Falha na compilação C++")
            return
        
        validation_results = {}
        
        for test_case in test_cases:
            print(f"\nTeste {test_case}:")
            
            test_input, expected_output = self.load_test_case(test_case)
            if test_input is None:
                continue
            
            test_results = []
            
            for rep in range(repetitions):
                print(f"  Repetição {rep+1}:")
                
                # C++ tradicional
                cpp_result = self.execute_solution(cpp_binary, test_input, time_limit, "cpp")
                cpp_status = "ACCEPTED" if cpp_result['status'] == 'ACCEPTED' else cpp_result['status']
                
                # Python tradicional
                python_result = self.execute_solution(python_source, test_input, time_limit, "python")
                python_status = "ACCEPTED" if python_result['status'] == 'ACCEPTED' else "TLE"
                
                # Python adaptativo
                adaptive_limit = time_limit * adjustment_factor
                python_adaptive = self.execute_solution(python_source, test_input, adaptive_limit, "python")
                python_adaptive_status = "ACCEPTED" if python_adaptive['status'] == 'ACCEPTED' else "TLE"
                
                print(f"    C++ tradicional: {cpp_status} ({cpp_result['time']:.3f}s)")
                print(f"    Python tradicional: {python_status} ({python_result['time']:.3f}s)")
                print(f"    Python adaptativo: {python_adaptive_status} ({python_adaptive['time']:.3f}s)")
                
                test_results.append({
                    "repetition": rep + 1,
                    "cpp_traditional": {
                        "status": cpp_result['status'],
                        "time": cpp_result['time']
                    },
                    "python_traditional": {
                        "status": python_result['status'], 
                        "time": python_result['time']
                    },
                    "python_adaptive": {
                        "status": python_adaptive['status'],
                        "time": python_adaptive['time'],
                        "time_limit": adaptive_limit
                    }
                })
            
            validation_results[test_case] = test_results
        
        # Salvar resultados da validação
        validation_data = {
            "adjustment_factor": adjustment_factor,
            "time_limit_traditional": time_limit,
            "repetitions": repetitions,
            "test_cases": validation_results
        }
        
        validation_file = self.results_dir / "validation_results.json"
        with open(validation_file, 'w') as f:
            json.dump(validation_data, f, indent=2)
        
        print(f"Validação salva em: {validation_file}")

def main():
    parser = argparse.ArgumentParser(description="CSES 1635 DP Iterativo Benchmark")
    parser.add_argument("--calibration-case", type=int, default=9, 
                       help="Test case para calibração")
    parser.add_argument("--validation-cases", nargs="+", type=int,
                       default=[1, 3, 4, 7, 8, 9, 11],
                       help="Test cases para validação")
    parser.add_argument("--calibration-reps", type=int, default=5,
                       help="Repetições para calibração")
    parser.add_argument("--validation-reps", type=int, default=3,
                       help="Repetições para validação")
    parser.add_argument("--time-limit", type=float, default=3.0,
                       help="Time limit em segundos")
    
    args = parser.parse_args()
    
    benchmark = CSES1635IterativeBenchmark()
    
    # Verificar ambiente
    benchmark.check_docker_images()
    test_cases = benchmark.get_test_cases()
    
    if not test_cases:
        print("Nenhum test case encontrado")
        return
    
    print("INICIANDO BENCHMARK CSES 1635 - DP ITERATIVO")
    
    # Fase 1: Calibração
    adjustment_factor = benchmark.run_calibration(
        args.calibration_case, 
        args.calibration_reps,
        args.time_limit
    )
    
    if adjustment_factor is None:
        print("Calibração falhou - não é possível calcular fator de ajuste")
        return
    
    # Fase 2: Validação
    benchmark.run_validation(
        args.validation_cases,
        args.validation_reps,
        args.time_limit,
        adjustment_factor
    )
    
    print("Benchmark concluído!")

if __name__ == "__main__":
    main()




