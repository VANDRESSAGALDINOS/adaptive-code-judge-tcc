import logging
from typing import List, Optional, Dict, Any

from models import db, Problem, TestCase, Submission, SubmissionTestResult
from models.submission import SubmissionStatus, SubmissionResult as SubmissionResultEnum, Language
from models.submission_result import ErrorType
from executor import DockerExecutor, ExecutionStatus
from config.app import AppConfig
from services.benchmark_service import BenchmarkService


logger = logging.getLogger(__name__)


class SubmissionService:
    """Service for managing code submissions and evaluation."""
    
    def __init__(self, config: AppConfig = None):
        """Initialize submission service."""
        self.config = config or AppConfig()
        self.executor = DockerExecutor(config)
        self.benchmark_service = BenchmarkService(config)
    
    def create_submission(
        self, 
        problem_id: int, 
        language: str, 
        source_code: str, 
        user_id: str = None
    ) -> Submission:
        """Create a new submission."""
        
        # Validate problem exists
        problem = Problem.query.get(problem_id)
        if not problem:
            raise ValueError(f"Problem {problem_id} not found")
        
        if not problem.is_active:
            raise ValueError(f"Problem {problem_id} is not active")
        
        # Validate language
        try:
            lang_enum = Language(language.lower())
        except ValueError:
            raise ValueError(f"Unsupported language: {language}")
        
        # Validate source code size
        if len(source_code.encode('utf-8')) > self.config.MAX_SOURCE_CODE_SIZE:
            raise ValueError(f"Source code too large (max {self.config.MAX_SOURCE_CODE_SIZE} bytes)")
        
        # Get active benchmark for time limits
        active_benchmark = self.benchmark_service.get_active_benchmark(problem_id)
        
        # Create submission record
        submission = Submission(
            problem_id=problem_id,
            user_id=user_id,
            language=lang_enum,
            source_code=source_code,
            benchmark_id=active_benchmark.id if active_benchmark else None,
            status=SubmissionStatus.PENDING
        )
        
        db.session.add(submission)
        db.session.commit()
        
        logger.info(f"Created submission {submission.id} for problem {problem_id} in {language}")
        
        # Execute submission
        try:
            self._execute_submission(submission)
        except Exception as e:
            logger.error(f"Submission execution failed: {e}")
            submission.status = SubmissionStatus.FAILED
            submission.result = SubmissionResultEnum.INTERNAL_ERROR
            submission.runtime_error = str(e)
            db.session.commit()
        
        return submission
    
    def _execute_submission(self, submission: Submission):
        """Execute submission against all test cases."""
        submission.status = SubmissionStatus.RUNNING
        db.session.commit()
        
        # Get test cases
        test_cases = TestCase.query.filter_by(problem_id=submission.problem_id).all()
        if not test_cases:
            raise ValueError(f"No test cases found for problem {submission.problem_id}")
        
        # Get time limit for this language
        time_limit = self.benchmark_service.get_time_limit_for_submission(
            submission.problem_id, submission.language.value
        )
        submission.time_limit_used = time_limit
        
        logger.info(f"Executing submission {submission.id} with time limit {time_limit}s")
        
        # Execute against each test case
        all_results = []
        total_execution_time = 0.0
        early_termination = False
        
        for test_case in test_cases:
            if early_termination:
                # Create failed result for remaining test cases
                result = SubmissionTestResult(
                    submission_id=submission.id,
                    test_case_id=test_case.id,
                    passed=False,
                    error_type=ErrorType.INTERNAL_ERROR,
                    error_message="Execution terminated early due to compilation error"
                )
                all_results.append(result)
                continue
            
            result = self._execute_test_case(submission, test_case, time_limit)
            all_results.append(result)
            
            if result.execution_time:
                total_execution_time += result.execution_time
            
            # Early termination on compilation error
            if result.error_type == ErrorType.INTERNAL_ERROR and "compilation" in (result.error_message or "").lower():
                early_termination = True
                submission.compilation_error = result.error_message
        
        # Save all results
        for result in all_results:
            db.session.add(result)
        
        # Update submission with overall results
        submission.execution_time_total = total_execution_time
        submission.total_test_cases = len(all_results)
        submission.passed_test_cases = sum(1 for r in all_results if r.passed)
        submission.update_score()
        
        # Determine overall result
        submission.result = self._determine_overall_result(all_results)
        submission.status = SubmissionStatus.COMPLETED
        
        db.session.commit()
        
        logger.info(f"Submission {submission.id} completed: {submission.result.value} "
                   f"({submission.passed_test_cases}/{submission.total_test_cases} passed, "
                   f"score: {submission.score:.2f})")
    
    def _execute_test_case(
        self, submission: Submission, test_case: TestCase, time_limit: float
    ) -> SubmissionTestResult:
        """Execute submission against a single test case."""
        
        result = SubmissionTestResult(
            submission_id=submission.id,
            test_case_id=test_case.id
        )
        
        try:
            # Execute code
            if submission.language == Language.CPP:
                execution_result = self.executor.execute_cpp(
                    submission.source_code,
                    test_case.input_data,
                    time_limit=time_limit,
                    memory_limit=submission.problem.memory_limit
                )
            elif submission.language == Language.PYTHON:
                execution_result = self.executor.execute_python(
                    submission.source_code,
                    test_case.input_data,
                    time_limit=time_limit,
                    memory_limit=submission.problem.memory_limit
                )
            else:
                raise ValueError(f"Unsupported language: {submission.language}")
            
            # Update result with execution data
            result.execution_time = execution_result.execution_time
            result.memory_used = execution_result.memory_used
            result.container_id = execution_result.container_id
            result.stdout = execution_result.stdout
            result.stderr = execution_result.stderr
            result.exit_code = execution_result.exit_code
            
            # Check for execution errors
            if execution_result.status == ExecutionStatus.COMPILATION_ERROR:
                result.error_type = ErrorType.INTERNAL_ERROR
                result.error_message = "Compilation failed"
                result.passed = False
                return result
            
            if execution_result.status == ExecutionStatus.TIME_LIMIT_EXCEEDED:
                result.error_type = ErrorType.TIME_LIMIT_EXCEEDED
                result.error_message = f"Time limit exceeded ({time_limit}s)"
                result.passed = False
                return result
            
            if execution_result.status == ExecutionStatus.MEMORY_LIMIT_EXCEEDED:
                result.error_type = ErrorType.MEMORY_LIMIT_EXCEEDED
                result.error_message = "Memory limit exceeded"
                result.passed = False
                return result
            
            if execution_result.status == ExecutionStatus.RUNTIME_ERROR:
                # Determine specific error type
                if any(keyword in execution_result.stderr.lower() for keyword in ['stack overflow', 'segmentation fault']):
                    result.error_type = ErrorType.STACK_OVERFLOW
                    result.error_message = "Stack overflow detected"
                else:
                    result.error_type = ErrorType.RUNTIME_ERROR
                    result.error_message = f"Runtime error (exit code: {execution_result.exit_code})"
                result.passed = False
                return result
            
            if not execution_result.success:
                result.error_type = ErrorType.INTERNAL_ERROR
                result.error_message = execution_result.error_message or "Unknown execution error"
                result.passed = False
                return result
            
            # Compare output
            expected_output = test_case.expected_output.strip()
            actual_output = execution_result.stdout.strip()
            result.actual_output = actual_output
            
            if expected_output == actual_output:
                result.passed = True
                result.error_type = ErrorType.NONE
            else:
                result.passed = False
                result.error_type = ErrorType.WRONG_ANSWER
                result.error_message = "Output does not match expected result"
                result.output_diff = self._generate_diff(expected_output, actual_output)
            
        except Exception as e:
            logger.error(f"Error executing test case {test_case.id}: {e}")
            result.error_type = ErrorType.INTERNAL_ERROR
            result.error_message = str(e)
            result.passed = False
        
        return result
    
    def _generate_diff(self, expected: str, actual: str) -> str:
        """Generate a simple diff between expected and actual output."""
        import difflib
        
        expected_lines = expected.splitlines(keepends=True)
        actual_lines = actual.splitlines(keepends=True)
        
        diff = list(difflib.unified_diff(
            expected_lines, actual_lines,
            fromfile='expected', tofile='actual',
            lineterm=''
        ))
        
        return ''.join(diff[:50])  # Limit diff size
    
    def _determine_overall_result(self, results: List[SubmissionTestResult]) -> SubmissionResultEnum:
        """Determine overall submission result based on test case results."""
        
        if not results:
            return SubmissionResultEnum.INTERNAL_ERROR
        
        # Check for compilation errors
        if any(r.error_type == ErrorType.INTERNAL_ERROR and "compilation" in (r.error_message or "").lower() 
               for r in results):
            return SubmissionResultEnum.COMPILATION_ERROR
        
        # Check if all passed
        if all(r.passed for r in results):
            return SubmissionResultEnum.ACCEPTED
        
        # Check for specific error types (prioritized)
        error_priority = [
            (ErrorType.TIME_LIMIT_EXCEEDED, SubmissionResultEnum.TIME_LIMIT_EXCEEDED),
            (ErrorType.MEMORY_LIMIT_EXCEEDED, SubmissionResultEnum.MEMORY_LIMIT_EXCEEDED),
            (ErrorType.STACK_OVERFLOW, SubmissionResultEnum.STACK_OVERFLOW),
            (ErrorType.RUNTIME_ERROR, SubmissionResultEnum.RUNTIME_ERROR),
            (ErrorType.WRONG_ANSWER, SubmissionResultEnum.WRONG_ANSWER),
            (ErrorType.PRESENTATION_ERROR, SubmissionResultEnum.PRESENTATION_ERROR),
            (ErrorType.INTERNAL_ERROR, SubmissionResultEnum.INTERNAL_ERROR),
        ]
        
        for error_type, result_type in error_priority:
            if any(r.error_type == error_type for r in results):
                return result_type
        
        return SubmissionResultEnum.WRONG_ANSWER
    
    def get_submission(self, submission_id: int, include_code: bool = False) -> Optional[Submission]:
        """Get submission by ID."""
        return Submission.query.get(submission_id)
    
    def get_submissions_for_problem(
        self, problem_id: int, user_id: str = None, limit: int = 100
    ) -> List[Submission]:
        """Get submissions for a problem."""
        query = Submission.query.filter_by(problem_id=problem_id)
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        return query.order_by(Submission.created_at.desc()).limit(limit).all()
    
    def get_submission_results(self, submission_id: int) -> List[SubmissionTestResult]:
        """Get test results for a submission."""
        return SubmissionTestResult.query.filter_by(submission_id=submission_id).all()
