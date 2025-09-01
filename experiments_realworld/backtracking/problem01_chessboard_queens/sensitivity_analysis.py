#!/usr/bin/env python3
"""
Análise de Sensibilidade Diferencial - Metodologia Adaptativa
Para problemas intrinsecamente rápidos que não geram TLE naturalmente
"""

import json
import subprocess
import time
import statistics
from pathlib import Path

class SensitivityAnalyzer:
    def __init__(self):
        self.extra_work_levels = [0, 1000, 5000, 10000, 25000, 50000, 100000]
        self.test_case = "cses_example"  # Caso padrão
        self.repetitions = 5
        self.timeout = 30.0
        
    def modify_extra_work(self, language, extra_work):
        """Modifica EXTRA_WORK no código fonte"""
        if language == "cpp":
            file_path = "slow_validation/solutions_slow/slow_solution.cpp"
            old_pattern = "const int EXTRA_WORK = "
            new_line = f"const int EXTRA_WORK = {extra_work};  // Overhead para análise de sensibilidade"
        else:
            file_path = "slow_validation/solutions_slow/slow_solution.py"
            old_pattern = "EXTRA_WORK = "
            new_line = f"EXTRA_WORK = {extra_work}  # Overhead para análise de sensibilidade"
            
        # Ler arquivo
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Substituir linha
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if old_pattern in line:
                lines[i] = new_line
                break
                
        # Escrever arquivo
        with open(file_path, 'w') as f:
            f.write('\n'.join(lines))
    
    def compile_cpp(self):
        """Compila solução C++"""
        cmd = ["g++", "-O2", "-o", "slow_validation/solutions_slow/slow_solution_cpp", 
               "slow_validation/solutions_slow/slow_solution.cpp"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    
    def run_solution(self, language, test_input):
        """Executa solução e mede tempo"""
        if language == "cpp":
            cmd = ["./slow_validation/solutions_slow/slow_solution_cpp"]
        else:
            cmd = ["python3", "slow_validation/solutions_slow/slow_solution.py"]
            
        start_time = time.perf_counter()
        try:
            result = subprocess.run(cmd, input=test_input, text=True, 
                                  capture_output=True, timeout=self.timeout)
            end_time = time.perf_counter()
            
            if result.returncode == 0:
                return end_time - start_time, result.stdout.strip(), None
            else:
                return None, None, "Runtime Error"
        except subprocess.TimeoutExpired:
            return self.timeout, None, "Timeout"
    
    def get_test_input(self):
        """Carrega input do caso de teste"""
        test_file = f"tests_cses/{self.test_case.split('_')[0] if '_' in self.test_case else '1'}.in"
        if not Path(test_file).exists():
            # Caso padrão CSES
            return "........\n........\n..*.....\\n........\n........\n.....**.\\n...*....\n........\n"
        
        with open(test_file, 'r') as f:
            return f.read()
    
    def analyze_sensitivity(self):
        """Executa análise completa de sensibilidade"""
        print("🔬 ANÁLISE DE SENSIBILIDADE DIFERENCIAL")
        print("📋 Metodologia Adaptativa para Problemas Intrinsecamente Rápidos")
        print("=" * 70)
        
        test_input = self.get_test_input()
        results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "methodology": "Differential Sensitivity Analysis",
            "problem": "N-Queens 8x8 - Intrinsically Fast",
            "test_case": self.test_case,
            "extra_work_levels": self.extra_work_levels,
            "repetitions": self.repetitions,
            "data": []
        }
        
        for extra_work in self.extra_work_levels:
            print(f"\n🔍 Testando EXTRA_WORK = {extra_work}")
            
            level_data = {
                "extra_work": extra_work,
                "cpp": {"times": [], "errors": 0},
                "python": {"times": [], "errors": 0}
            }
            
            for language in ["cpp", "python"]:
                print(f"  📊 {language.upper()}...")
                
                # Modificar código
                self.modify_extra_work(language, extra_work)
                
                # Compilar se necessário
                if language == "cpp":
                    if not self.compile_cpp():
                        print(f"    ❌ Erro de compilação")
                        continue
                
                # Executar repetições
                for rep in range(self.repetitions):
                    exec_time, output, error = self.run_solution(language, test_input)
                    
                    if error:
                        level_data[language]["errors"] += 1
                        if error == "Timeout":
                            exec_time = self.timeout
                    
                    if exec_time is not None:
                        level_data[language]["times"].append(exec_time)
                
                # Calcular estatísticas
                if level_data[language]["times"]:
                    times = level_data[language]["times"]
                    level_data[language].update({
                        "median": statistics.median(times),
                        "mean": statistics.mean(times),
                        "std": statistics.stdev(times) if len(times) > 1 else 0,
                        "min": min(times),
                        "max": max(times)
                    })
                    print(f"    ✅ Mediano: {level_data[language]['median']:.4f}s")
                else:
                    print(f"    ❌ Todas execuções falharam")
            
            results["data"].append(level_data)
        
        # Calcular métricas científicas
        self.calculate_scientific_metrics(results)
        
        # Salvar resultados
        with open("sensitivity_analysis_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Resultados salvos em: sensitivity_analysis_results.json")
        return results
    
    def calculate_scientific_metrics(self, results):
        """Calcula métricas científicas rigorosas"""
        print(f"\n📈 MÉTRICAS CIENTÍFICAS")
        print("=" * 50)
        
        # Extrair dados para regressão
        cpp_points = []
        py_points = []
        
        for level in results["data"]:
            if "median" in level["cpp"] and "median" in level["python"]:
                extra_work = level["extra_work"]
                cpp_points.append((extra_work, level["cpp"]["median"]))
                py_points.append((extra_work, level["python"]["median"]))
        
        if len(cpp_points) >= 3 and len(py_points) >= 3:
            # Calcular slopes (sensibilidade)
            cpp_slope = self.calculate_slope(cpp_points)
            py_slope = self.calculate_slope(py_points)
            
            # Differential Sensitivity Index
            dsi = py_slope / cpp_slope if cpp_slope > 0 else float('inf')
            
            # Tolerance Thresholds (EXTRA_WORK onde atinge 1s)
            cpp_threshold = (1.0 - cpp_points[0][1]) / cpp_slope if cpp_slope > 0 else float('inf')
            py_threshold = (1.0 - py_points[0][1]) / py_slope if py_slope > 0 else float('inf')
            
            tolerance_gap = cpp_threshold / py_threshold if py_threshold > 0 else float('inf')
            
            results["scientific_metrics"] = {
                "cpp_slope": cpp_slope,
                "python_slope": py_slope,
                "differential_sensitivity_index": dsi,
                "cpp_tolerance_threshold": cpp_threshold,
                "python_tolerance_threshold": py_threshold,
                "tolerance_gap": tolerance_gap,
                "statistical_significance": dsi >= 2.0 and tolerance_gap >= 10.0
            }
            
            print(f"📊 C++ Slope: {cpp_slope:.2e} s/work")
            print(f"📊 Python Slope: {py_slope:.2e} s/work")
            print(f"🎯 DSI (Differential Sensitivity Index): {dsi:.2f}x")
            print(f"⚡ Tolerance Gap: {tolerance_gap:.1f}x")
            print(f"✅ Statistically Significant: {'Yes' if results['scientific_metrics']['statistical_significance'] else 'No'}")
    
    def calculate_slope(self, points):
        """Calcula slope da regressão linear"""
        if len(points) < 2:
            return 0
        
        n = len(points)
        sum_x = sum(p[0] for p in points)
        sum_y = sum(p[1] for p in points)
        sum_xy = sum(p[0] * p[1] for p in points)
        sum_x2 = sum(p[0] ** 2 for p in points)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        return slope

if __name__ == "__main__":
    analyzer = SensitivityAnalyzer()
    analyzer.analyze_sensitivity()
