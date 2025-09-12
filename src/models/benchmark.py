from .base import db, TimestampMixin
from enum import Enum


class BenchmarkStatus(Enum):
    PENDING = "pending"
    RUNNING = "running" 
    STABLE = "stable"
    UNSTABLE = "unstable"
    FAILED = "failed"


class Benchmark(db.Model, TimestampMixin):
    
    __tablename__ = 'benchmarks'
    
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)
    
    largest_test_case_id = db.Column(db.Integer, db.ForeignKey('test_cases.id'), nullable=False)
    repetitions = db.Column(db.Integer, nullable=False, default=5)
    
    base_time_cpp = db.Column(db.Float, nullable=True)
    cpp_times = db.Column(db.Text, nullable=True)
    cpp_status = db.Column(db.Enum(BenchmarkStatus), nullable=False, default=BenchmarkStatus.PENDING)
    cpp_iqr = db.Column(db.Float, nullable=True)
    
    python_median_time = db.Column(db.Float, nullable=True)
    python_times = db.Column(db.Text, nullable=True)
    python_status = db.Column(db.Enum(BenchmarkStatus), nullable=False, default=BenchmarkStatus.PENDING)
    python_iqr = db.Column(db.Float, nullable=True)
    
    adjustment_factor_python = db.Column(db.Float, nullable=True)
    factor_cap = db.Column(db.Float, nullable=False, default=12.0)
    min_factor = db.Column(db.Float, nullable=False, default=1.0)
    
    status = db.Column(db.Enum(BenchmarkStatus), nullable=False, default=BenchmarkStatus.PENDING)
    is_reliable = db.Column(db.Boolean, nullable=False, default=False)
    error_message = db.Column(db.Text, nullable=True)
    
    docker_cpp_image = db.Column(db.String(100), nullable=True, default="adaptivejudge-cpp:latest")
    docker_python_image = db.Column(db.String(100), nullable=True, default="adaptivejudge-python:latest")
    largest_test_case = db.relationship('TestCase', foreign_keys=[largest_test_case_id])
    active_for_problems = db.relationship('ProblemBenchmarkActive', backref='benchmark', lazy=True)
    
    def __repr__(self):
        return f'<Benchmark {self.id}: Problem {self.problem_id} (Status: {self.status.value})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'problem_id': self.problem_id,
            'largest_test_case_id': self.largest_test_case_id,
            'repetitions': self.repetitions,
            'base_time_cpp': self.base_time_cpp,
            'cpp_status': self.cpp_status.value if self.cpp_status else None,
            'cpp_iqr': self.cpp_iqr,
            'python_median_time': self.python_median_time,
            'python_status': self.python_status.value if self.python_status else None,
            'python_iqr': self.python_iqr,
            'adjustment_factor_python': self.adjustment_factor_python,
            'factor_cap': self.factor_cap,
            'min_factor': self.min_factor,
            'status': self.status.value if self.status else None,
            'is_reliable': self.is_reliable,
            'error_message': self.error_message,
            'docker_cpp_image': self.docker_cpp_image,
            'docker_python_image': self.docker_python_image,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def get_time_limit_for_language(self, language: str) -> float:
        if not self.is_reliable or not self.base_time_cpp:
            return self.problem.time_limit_base
        
        if language.lower() == 'cpp' or language.lower() == 'c++':
            return self.base_time_cpp
        elif language.lower() == 'python':
            if self.adjustment_factor_python:
                return self.base_time_cpp * self.adjustment_factor_python
            else:
                return self.problem.time_limit_base
        else:
            return self.problem.time_limit_base
