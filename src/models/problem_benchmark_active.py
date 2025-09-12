from .base import db, TimestampMixin


class ProblemBenchmarkActive(db.Model, TimestampMixin):
    
    __tablename__ = 'problem_benchmark_active'
    
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False, unique=True)
    benchmark_id = db.Column(db.Integer, db.ForeignKey('benchmarks.id'), nullable=False)
    
    activated_by = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<ProblemBenchmarkActive: Problem {self.problem_id} -> Benchmark {self.benchmark_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'problem_id': self.problem_id,
            'benchmark_id': self.benchmark_id,
            'activated_by': self.activated_by,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @staticmethod
    def set_active_benchmark(problem_id: int, benchmark_id: int, activated_by: str = None, notes: str = None):
        from .base import db
        
        existing = ProblemBenchmarkActive.query.filter_by(problem_id=problem_id).first()
        if existing:
            db.session.delete(existing)
        
        active_benchmark = ProblemBenchmarkActive(
            problem_id=problem_id,
            benchmark_id=benchmark_id,
            activated_by=activated_by,
            notes=notes
        )
        
        db.session.add(active_benchmark)
        db.session.commit()
        
        return active_benchmark
    
    @staticmethod
    def get_active_benchmark(problem_id: int):
        return ProblemBenchmarkActive.query.filter_by(problem_id=problem_id).first()
