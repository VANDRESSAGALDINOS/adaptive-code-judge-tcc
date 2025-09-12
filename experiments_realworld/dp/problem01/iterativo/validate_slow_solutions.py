#!/usr/bin/env python3
"""
Validação de Soluções Lentas - CSES 1635 DP Iterativo
Verificar se soluções intencionalmente lentas são detectadas adequadamente
"""

import argparse
import json
import subprocess
import time
from pathlib import Path

class SlowSolutionValidator:
    """Validador para soluções intencionalmente lentas."""
    
    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir or ".")
        self.slow_dir = self.base_dir / "slow_validation" / "solutions_slow"
        self.tests_dir = self.base_dir / ".." / "tests_cses"
        self.results_dir = self.base_dir / "results"
        self.results_dir.mkdir(exist_ok=True)
        
        # Docker images
        self.cpp_image = "gcc:latest"
        self.python_image = "python:3.11-slim"

    def compile_cpp_slow(self):
        """Compilar solução C++ lenta."""
        source = self.slow_dir / "slow_solution.cpp"
        output = self.slow_dir / "slow_solution_cpp"
        
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{source.parent.absolute()}:/workspace",
            "-w", "/workspace",
            self.cpp_image,
            "g++", "-std=c++17", "-O2", "-o", output.name, source.name
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Erro na compilação C++ slow: {result.stderr}")
            return False
        return True

    def execute_slow_solution(self, solution_path, test_input, time_limit=5.0, language="cpp"):
        """Executar solução lenta."""
        
        if language == "cpp":
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

    def load_test_case(self, test_number):
        """Carregar test case."""
        input_file = self.tests_dir / f"{test_number}.in"
        output_file = self.tests_dir / f"{test_number}.out"
        
        if not input_file.exists() or not output_file.exists():
            return None, None
            
        test_input = input_file.read_text().strip()
        expected_output = output_file.read_text().strip()
        
        return test_input, expected_output

    def validate_slow_solutions(self, test_cases, time_limit):
        """Validar soluções lentas em test cases específicos."""
        print("=== VALIDAÇÃO DE SOLUÇÕES LENTAS ===")
        
        # Compilar C++ slow
        if not self.compile_cpp_slow():
            print("Falha na compilação C++ slow")
            return
        
        cpp_slow_binary = self.slow_dir / "slow_solution_cpp"
        python_slow_source = self.slow_dir / "slow_solution.py"
        
        validation_results = {}
        
        for test_case in test_cases:
            print(f"\nValidando Test Case {test_case}:")
            
            test_input, expected_output = self.load_test_case(test_case)
            if test_input is None:
                print(f"  Test case {test_case} não encontrado")
                continue
            
            # Executar C++ slow
            cpp_result = self.execute_slow_solution(cpp_slow_binary, test_input, time_limit, "cpp")
            cpp_status = "ACCEPTED" if cpp_result['status'] == 'ACCEPTED' else cpp_result['status']
            
            # Executar Python slow
            python_result = self.execute_slow_solution(python_slow_source, test_input, time_limit, "python")
            python_status = "ACCEPTED" if python_result['status'] == 'ACCEPTED' else python_result['status']
            
            print(f"  C++ Slow: {cpp_status} ({cpp_result['time']:.3f}s)")
            print(f"  Python Slow: {python_status} ({python_result['time']:.3f}s)")
            
            validation_results[test_case] = {
                "cpp_slow": {
                    "status": cpp_result['status'],
                    "time": cpp_result['time'],
                    "output": cpp_result['output'],
                    "error": cpp_result['error']
                },
                "python_slow": {
                    "status": python_result['status'],
                    "time": python_result['time'],
                    "output": python_result['output'],
                    "error": python_result['error']
                }
            }
        
        # Salvar resultados
        slow_validation_data = {
            "test_cases": test_cases,
            "time_limit": time_limit,
            "validation_results": validation_results
        }
        
        results_file = self.results_dir / "slow_solution_validation.json"
        with open(results_file, 'w') as f:
            json.dump(slow_validation_data, f, indent=2)
        
        print(f"\nResultados salvos em: {results_file}")
        
        # Resumo
        print("\n=== RESUMO DA VALIDAÇÃO ===")
        for test_case in test_cases:
            if test_case in validation_results:
                cpp_status = validation_results[test_case]['cpp_slow']['status']
                python_status = validation_results[test_case]['python_slow']['status']
                print(f"Test {test_case}: C++ {cpp_status}, Python {python_status}")

def main():
    parser = argparse.ArgumentParser(description="Validação de Soluções Lentas DP Iterativo")
    parser.add_argument("--test-cases", nargs="+", type=int, default=[4, 8],
                       help="Test cases para validação")
    parser.add_argument("--time-limit", type=float, default=2.0,
                       help="Time limit em segundos")
    
    args = parser.parse_args()
    
    validator = SlowSolutionValidator()
    validator.validate_slow_solutions(args.test_cases, args.time_limit)

if __name__ == "__main__":
    main()












