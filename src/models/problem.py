from .base import db, TimestampMixin


class Problem(db.Model, TimestampMixin):
    
    __tablename__ = 'problems'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    max_input_size = db.Column(db.Integer, nullable=False, default=1000000)
    time_limit_base = db.Column(db.Float, nullable=False, default=1.0)
    memory_limit = db.Column(db.Integer, nullable=False, default=128)
    difficulty = db.Column(db.String(50), nullable=False, default='medium')
    tags = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    test_cases = db.relationship('TestCase', backref='problem', lazy=True, cascade='all, delete-orphan')
    benchmarks = db.relationship('Benchmark', backref='problem', lazy=True, cascade='all, delete-orphan')
    submissions = db.relationship('Submission', backref='problem', lazy=True, cascade='all, delete-orphan')
    active_benchmark = db.relationship('ProblemBenchmarkActive', backref='problem', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Problem {self.id}: {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'max_input_size': self.max_input_size,
            'time_limit_base': self.time_limit_base,
            'memory_limit': self.memory_limit,
            'difficulty': self.difficulty,
            'tags': self.tags.split(',') if self.tags else [],
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
