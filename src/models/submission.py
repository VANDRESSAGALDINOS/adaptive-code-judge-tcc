from .base import db, TimestampMixin
from enum import Enum


class SubmissionStatus(Enum):
    """Status of submission execution."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class SubmissionResult(Enum):
    """Overall result of submission evaluation."""
    ACCEPTED = "accepted"
    WRONG_ANSWER = "wrong_answer"
    TIME_LIMIT_EXCEEDED = "time_limit_exceeded"
    RUNTIME_ERROR = "runtime_error"
    COMPILATION_ERROR = "compilation_error"
    MEMORY_LIMIT_EXCEEDED = "memory_limit_exceeded"
    STACK_OVERFLOW = "stack_overflow"
    PRESENTATION_ERROR = "presentation_error"
    INTERNAL_ERROR = "internal_error"


class Language(Enum):
    """Supported programming languages."""
    CPP = "cpp"
    PYTHON = "python"


class Submission(db.Model, TimestampMixin):
    """Submission model representing user code submissions."""
    
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)
    
    # Submission metadata
    user_id = db.Column(db.String(100), nullable=True)  # External user identifier
    language = db.Column(db.Enum(Language), nullable=False)
    source_code = db.Column(db.Text, nullable=False)
    
    # Execution results
    status = db.Column(db.Enum(SubmissionStatus), nullable=False, default=SubmissionStatus.PENDING)
    result = db.Column(db.Enum(SubmissionResult), nullable=True)
    execution_time_total = db.Column(db.Float, nullable=True)  # Total execution time in seconds
    memory_used = db.Column(db.Integer, nullable=True)  # Memory used in KB
    
    # Scoring
    score = db.Column(db.Float, nullable=True)  # Score between 0.0 and 1.0
    passed_test_cases = db.Column(db.Integer, nullable=False, default=0)
    total_test_cases = db.Column(db.Integer, nullable=False, default=0)
    
    # Benchmark reference
    benchmark_id = db.Column(db.Integer, db.ForeignKey('benchmarks.id'), nullable=True)
    time_limit_used = db.Column(db.Float, nullable=True)  # Time limit that was applied
    
    # Error information
    compilation_error = db.Column(db.Text, nullable=True)
    runtime_error = db.Column(db.Text, nullable=True)
    
    # Docker execution info
    docker_image = db.Column(db.String(100), nullable=True)
    container_id = db.Column(db.String(100), nullable=True)
    
    # Relationships
    test_results = db.relationship('SubmissionTestResult', backref='submission', lazy=True, cascade='all, delete-orphan')
    benchmark = db.relationship('Benchmark', backref='submissions')
    
    def __repr__(self):
        return f'<Submission {self.id}: Problem {self.problem_id} ({self.language.value if self.language else "unknown"})>'
    
    def to_dict(self, include_code=False):
        result = {
            'id': self.id,
            'problem_id': self.problem_id,
            'user_id': self.user_id,
            'language': self.language.value if self.language else None,
            'status': self.status.value if self.status else None,
            'result': self.result.value if self.result else None,
            'execution_time_total': self.execution_time_total,
            'memory_used': self.memory_used,
            'score': self.score,
            'passed_test_cases': self.passed_test_cases,
            'total_test_cases': self.total_test_cases,
            'benchmark_id': self.benchmark_id,
            'time_limit_used': self.time_limit_used,
            'compilation_error': self.compilation_error,
            'runtime_error': self.runtime_error,
            'docker_image': self.docker_image,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_code:
            result['source_code'] = self.source_code
            
        return result
    
    def calculate_score(self):
        """Calculate score based on passed test cases and their weights."""
        if self.total_test_cases == 0:
            return 0.0
        
        if not self.test_results:
            return 0.0
        
        total_weight = sum(tr.test_case.weight for tr in self.test_results)
        passed_weight = sum(tr.test_case.weight for tr in self.test_results if tr.passed)
        
        if total_weight == 0:
            return 0.0
        
        return passed_weight / total_weight
    
    def update_score(self):
        """Update the score field based on current test results."""
        self.score = self.calculate_score()
        self.passed_test_cases = sum(1 for tr in self.test_results if tr.passed)
        self.total_test_cases = len(self.test_results)
