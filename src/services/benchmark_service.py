import json
import logging
import statistics
from typing import List, Tuple, Optional, Dict, Any

from models import db, Problem, TestCase, Benchmark, ProblemBenchmarkActive
from models.benchmark import BenchmarkStatus
from executor import DockerExecutor, ExecutionStatus
from config.app import AppConfig


logger = logging.getLogger(__name__)


class BenchmarkService:
    
    def __init__(self, config: AppConfig = None):
        self.config = config or AppConfig()
        self.executor = DockerExecutor(config)
    
    def create_benchmark(self, problem_id: int, repetitions: int = None, activated_by: str = None) -> Benchmark:
        if repetitions is None:
            repetitions = self.config.BENCHMARK_REPETITIONS
        
        problem = Problem.query.get(problem_id)
        if not problem:
            raise ValueError(f"Problem {problem_id} not found")
        
        largest_test_case = self._find_largest_test_case(problem_id)
        if not largest_test_case:
            raise ValueError(f"No test cases found for problem {problem_id}")
        
        benchmark = Benchmark(
            problem_id=problem_id,
            largest_test_case_id=largest_test_case.id,
            repetitions=repetitions,
            factor_cap=self.config.BENCHMARK_FACTOR_CAP,
            min_factor=self.config.BENCHMARK_MIN_FACTOR,
            status=BenchmarkStatus.PENDING
        )
        
        db.session.add(benchmark)
        db.session.commit()
        
        logger.info(f"Created benchmark {benchmark.id} for problem {problem_id}")
        
        try:
            self._execute_benchmark(benchmark, largest_test_case)
            
            if benchmark.is_reliable:
                ProblemBenchmarkActive.set_active_benchmark(
                    problem_id=problem_id,
                    benchmark_id=benchmark.id,
                    activated_by=activated_by,
                    notes="Auto-activated after successful benchmark creation"
                )
                logger.info(f"Set benchmark {benchmark.id} as active for problem {problem_id}")
        
        except Exception as e:
            logger.error(f"Benchmark execution failed: {e}")
            benchmark.status = BenchmarkStatus.FAILED
            benchmark.error_message = str(e)
            db.session.commit()
        
        return benchmark
    
    def _find_largest_test_case(self, problem_id: int) -> Optional[TestCase]:
        test_cases = TestCase.query.filter_by(problem_id=problem_id).all()
        
        if not test_cases:
            return None
        
        largest = max(test_cases, key=lambda tc: (
            tc.input_size or len(tc.input_data),
            len(tc.input_data)
        ))
        
        logger.info(f"Selected largest test case {largest.id} ({largest.name}) for benchmarking")
        return largest
    
    def _execute_benchmark(self, benchmark: Benchmark, test_case: TestCase):
        benchmark.status = BenchmarkStatus.RUNNING
        db.session.commit()
        
        cpp_solution = self._load_reference_solution(benchmark.problem_id, 'cpp')
        python_solution = self._load_reference_solution(benchmark.problem_id, 'python')
        
        if not cpp_solution:
            raise ValueError(f"No C++ reference solution found for problem {benchmark.problem_id}")
        if not python_solution:
            raise ValueError(f"No Python reference solution found for problem {benchmark.problem_id}")
        
        if not self._validate_solution(cpp_solution, test_case, 'cpp'):
            raise ValueError("C++ reference solution produces incorrect output")
        if not self._validate_solution(python_solution, test_case, 'python'):
            raise ValueError("Python reference solution produces incorrect output")
        
        cpp_times = self._measure_execution_times(
            cpp_solution, test_case, benchmark.repetitions, 'cpp'
        )
        python_times = self._measure_execution_times(
            python_solution, test_case, benchmark.repetitions, 'python'
        )
        
        self._calculate_benchmark_statistics(benchmark, cpp_times, python_times)
        
        logger.info(f"Benchmark {benchmark.id} completed successfully")
    
    def _load_reference_solution(self, problem_id: int, language: str) -> Optional[str]:
        import os
        
        filename = f"problem_{problem_id}.{language}" if language == 'cpp' else f"problem_{problem_id}.py"
        filepath = os.path.join(self.config.REFERENCE_SOLUTIONS_DIR, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Reference solution not found: {filepath}")
            return None
        except Exception as e:
            logger.error(f"Error loading reference solution {filepath}: {e}")
            return None
    
    def _validate_solution(self, solution_code: str, test_case: TestCase, language: str) -> bool:
        try:
            if language == 'cpp':
                result = self.executor.execute_cpp(
                    solution_code, test_case.input_data, 
                    time_limit=30.0
                )
            elif language == 'python':
                result = self.executor.execute_python(
                    solution_code, test_case.input_data,
                    time_limit=30.0
                )
            else:
                return False
            
            if not result.success:
                logger.error(f"Reference solution execution failed: {result.error_message}")
                return False
            
            expected = test_case.expected_output.strip()
            actual = result.stdout.strip()
            
            if expected != actual:
                logger.error(f"Output mismatch. Expected: {expected[:100]}..., Got: {actual[:100]}...")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Solution validation error: {e}")
            return False
    
    def _measure_execution_times(
        self, solution_code: str, test_case: TestCase, repetitions: int, language: str
    ) -> List[float]:
        times = []
        
        for i in range(repetitions):
            try:
                if language == 'cpp':
                    result = self.executor.execute_cpp(
                        solution_code, test_case.input_data,
                        time_limit=60.0
                    )
                elif language == 'python':
                    result = self.executor.execute_python(
                        solution_code, test_case.input_data,
                        time_limit=60.0
                    )
                else:
                    raise ValueError(f"Unsupported language: {language}")
                
                if result.success:
                    times.append(result.execution_time)
                    logger.debug(f"{language} run {i+1}: {result.execution_time:.4f}s")
                else:
                    logger.warning(f"{language} run {i+1} failed: {result.error_message}")
                    
            except Exception as e:
                logger.error(f"Error in {language} run {i+1}: {e}")
        
        if len(times) < repetitions // 2:
            raise RuntimeError(f"Too many failed runs for {language} (got {len(times)}/{repetitions})")
        
        return times
    
    def _calculate_benchmark_statistics(
        self, benchmark: Benchmark, cpp_times: List[float], python_times: List[float]
    ):
        
        if cpp_times:
            benchmark.base_time_cpp = statistics.median(cpp_times)
            benchmark.cpp_times = json.dumps(cpp_times)
            benchmark.cpp_iqr = self._calculate_iqr(cpp_times)
            benchmark.cpp_status = self._determine_stability_status(benchmark.cpp_iqr, benchmark.base_time_cpp)
        else:
            benchmark.cpp_status = BenchmarkStatus.FAILED
        
        if python_times:
            benchmark.python_median_time = statistics.median(python_times)
            benchmark.python_times = json.dumps(python_times)
            benchmark.python_iqr = self._calculate_iqr(python_times)
            benchmark.python_status = self._determine_stability_status(
                benchmark.python_iqr, benchmark.python_median_time
            )
        else:
            benchmark.python_status = BenchmarkStatus.FAILED
        
        if benchmark.base_time_cpp and benchmark.python_median_time:
            raw_factor = benchmark.python_median_time / benchmark.base_time_cpp
            
            benchmark.adjustment_factor_python = max(
                benchmark.min_factor,
                min(benchmark.factor_cap, raw_factor)
            )
            
            logger.info(f"Calculated adjustment factor: {raw_factor:.2f} -> {benchmark.adjustment_factor_python:.2f}")
        
        if (benchmark.cpp_status == BenchmarkStatus.STABLE and 
            benchmark.python_status == BenchmarkStatus.STABLE and
            benchmark.adjustment_factor_python):
            benchmark.status = BenchmarkStatus.STABLE
            benchmark.is_reliable = True
        elif (benchmark.cpp_status in [BenchmarkStatus.STABLE, BenchmarkStatus.UNSTABLE] and
              benchmark.python_status in [BenchmarkStatus.STABLE, BenchmarkStatus.UNSTABLE] and
              benchmark.adjustment_factor_python):
            benchmark.status = BenchmarkStatus.UNSTABLE
            benchmark.is_reliable = False
        else:
            benchmark.status = BenchmarkStatus.FAILED
            benchmark.is_reliable = False
        
        db.session.commit()
    
    def _calculate_iqr(self, times: List[float]) -> float:
        if len(times) < 2:
            return 0.0
        
        q75, q25 = statistics.quantiles(times, n=4)[1], statistics.quantiles(times, n=4)[0]
        return q75 - q25
    
    def _determine_stability_status(self, iqr: float, median: float) -> BenchmarkStatus:
        if median == 0:
            return BenchmarkStatus.FAILED
        
        relative_iqr = iqr / median
        
        if relative_iqr <= self.config.BENCHMARK_STABILITY_THRESHOLD:
            return BenchmarkStatus.STABLE
        else:
            return BenchmarkStatus.UNSTABLE
    
    def get_active_benchmark(self, problem_id: int) -> Optional[Benchmark]:
        active = ProblemBenchmarkActive.get_active_benchmark(problem_id)
        return active.benchmark if active else None
    
    def set_active_benchmark(
        self, problem_id: int, benchmark_id: int, activated_by: str = None, notes: str = None
    ) -> ProblemBenchmarkActive:
        benchmark = Benchmark.query.filter_by(id=benchmark_id, problem_id=problem_id).first()
        if not benchmark:
            raise ValueError(f"Benchmark {benchmark_id} not found for problem {problem_id}")
        
        return ProblemBenchmarkActive.set_active_benchmark(
            problem_id=problem_id,
            benchmark_id=benchmark_id,
            activated_by=activated_by,
            notes=notes
        )
    
    def get_time_limit_for_submission(self, problem_id: int, language: str) -> float:
        active_benchmark = self.get_active_benchmark(problem_id)
        
        if active_benchmark and active_benchmark.is_reliable:
            return active_benchmark.get_time_limit_for_language(language)
        else:
            problem = Problem.query.get(problem_id)
            return problem.time_limit_base if problem else self.config.DEFAULT_TIME_LIMIT
