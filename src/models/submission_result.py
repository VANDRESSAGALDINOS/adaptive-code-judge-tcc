from .base import db, TimestampMixin
from enum import Enum


class ErrorType(Enum):
    NONE = "none"
    WRONG_ANSWER = "wrong_answer"
    TIME_LIMIT_EXCEEDED = "time_limit_exceeded"
    RUNTIME_ERROR = "runtime_error"
    MEMORY_LIMIT_EXCEEDED = "memory_limit_exceeded"
    STACK_OVERFLOW = "stack_overflow"
    PRESENTATION_ERROR = "presentation_error"
    INTERNAL_ERROR = "internal_error"


class SubmissionTestResult(db.Model, TimestampMixin):
    
    __tablename__ = 'submission_results'
    
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    test_case_id = db.Column(db.Integer, db.ForeignKey('test_cases.id'), nullable=False)
    
    passed = db.Column(db.Boolean, nullable=False, default=False)
    execution_time = db.Column(db.Float, nullable=True)
    memory_used = db.Column(db.Integer, nullable=True)
    
    actual_output = db.Column(db.Text, nullable=True)
    output_diff = db.Column(db.Text, nullable=True)
    
    error_type = db.Column(db.Enum(ErrorType), nullable=False, default=ErrorType.NONE)
    error_message = db.Column(db.Text, nullable=True)
    exit_code = db.Column(db.Integer, nullable=True)
    
    container_id = db.Column(db.String(100), nullable=True)
    stdout = db.Column(db.Text, nullable=True)
    stderr = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<SubmissionTestResult {self.id}: Submission {self.submission_id}, TestCase {self.test_case_id} ({"PASS" if self.passed else "FAIL"})>'
    
    def to_dict(self, include_output=False):
        result = {
            'id': self.id,
            'submission_id': self.submission_id,
            'test_case_id': self.test_case_id,
            'passed': self.passed,
            'execution_time': self.execution_time,
            'memory_used': self.memory_used,
            'error_type': self.error_type.value if self.error_type else None,
            'error_message': self.error_message,
            'exit_code': self.exit_code,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_output:
            result.update({
                'actual_output': self.actual_output,
                'output_diff': self.output_diff,
                'stdout': self.stdout,
                'stderr': self.stderr
            })
            
        return result
    
    def determine_error_type(self, exit_code: int, stderr: str, execution_time: float, time_limit: float, memory_used: int = None, memory_limit: int = None) -> ErrorType:
        if execution_time > time_limit:
            return ErrorType.TIME_LIMIT_EXCEEDED
        
        if memory_used and memory_limit and memory_used > memory_limit * 1024:
            return ErrorType.MEMORY_LIMIT_EXCEEDED
        
        if stderr and any(keyword in stderr.lower() for keyword in ['stack overflow', 'segmentation fault', 'stack smashing']):
            return ErrorType.STACK_OVERFLOW
        
        if exit_code != 0:
            return ErrorType.RUNTIME_ERROR
        
        if not self.passed:
            return ErrorType.WRONG_ANSWER
        
        return ErrorType.NONE
