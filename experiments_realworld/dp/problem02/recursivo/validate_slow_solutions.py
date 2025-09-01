#!/usr/bin/env python3
"""
Validação de Soluções Lentas - CSES 1635 DP Recursivo
Verifica se soluções intencionalmente lentas falham como esperado
"""

import subprocess
import time
import json
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
            "g++", "-std=c++17", "-O1", "-o", output.name, source.name
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
            end_time = time.time()
            execution_time = end_time - start_time
            
            return {
                "status": "ACCEPTED" if result.returncode == 0 else "RUNTIME_ERROR",
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

    def validate_slow_solutions(self, test_cases=[8, 12], time_limit=5.0):
        """Validar que soluções lentas falham nos test cases especificados."""
        print("=== VALIDAÇÃO DE SOLUÇÕES LENTAS ===")
        
        results = {
            "test_cases": test_cases,
            "time_limit": time_limit,
            "validation_results": {}
        }
        
        # Compilar C++ slow
        if not self.compile_cpp_slow():
            print("Falha na compilação C++ slow")
            return None
        
        cpp_slow = self.slow_dir / "slow_solution_cpp"
        python_slow = self.slow_dir / "slow_solution.py"
        
        for test_case in test_cases:
            print(f"\nValidando Test Case {test_case}:")
            
            # Carregar test case
            input_file = self.tests_dir / f"{test_case}.in"
            output_file = self.tests_dir / f"{test_case}.out"
            
            if not input_file.exists():
                print(f"Test case {test_case} não encontrado")
                continue
            
            test_input = input_file.read_text()
            expected_output = output_file.read_text().strip() if output_file.exists() else ""
            
            # Testar C++ slow
            cpp_result = self.execute_slow_solution(cpp_slow, test_input, time_limit, "cpp")
            print(f"  C++ Slow: {cpp_result['status']} ({cpp_result['time']:.3f}s)")
            
            # Testar Python slow
            python_result = self.execute_slow_solution(python_slow, test_input, time_limit, "python")
            print(f"  Python Slow: {python_result['status']} ({python_result['time']:.3f}s)")
            
            results["validation_results"][test_case] = {
                "cpp_slow": cpp_result,
                "python_slow": python_result
            }
        
        return results

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Validação de Soluções Lentas CSES 1635")
    parser.add_argument("--test-cases", nargs="+", type=int, default=[8, 12],
                        help="Test cases para validação")
    parser.add_argument("--time-limit", type=float, default=5.0,
                        help="Limite de tempo (segundos)")
    
    args = parser.parse_args()
    
    validator = SlowSolutionValidator()
    results = validator.validate_slow_solutions(args.test_cases, args.time_limit)
    
    if results:
        # Salvar resultados
        output_file = validator.results_dir / "slow_solution_validation.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResultados salvos em: {output_file}")
        
        # Resumo
        print("\n=== RESUMO DA VALIDAÇÃO ===")
        for test_case in results["validation_results"]:
            cpp_status = results["validation_results"][test_case]["cpp_slow"]["status"]
            python_status = results["validation_results"][test_case]["python_slow"]["status"]
            print(f"Test {test_case}: C++ {cpp_status}, Python {python_status}")
    
    return 0

if __name__ == "__main__":
    exit(main())
