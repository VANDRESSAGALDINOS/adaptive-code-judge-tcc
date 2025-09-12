from .base import db, TimestampMixin


class TestCase(db.Model, TimestampMixin):
    
    __tablename__ = 'test_cases'
    
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    input_data = db.Column(db.Text, nullable=False)
    expected_output = db.Column(db.Text, nullable=False)
    complexity_hint = db.Column(db.String(50))
    input_size = db.Column(db.Integer)
    is_sample = db.Column(db.Boolean, nullable=False, default=False)
    is_hidden = db.Column(db.Boolean, nullable=False, default=True)
    weight = db.Column(db.Float, nullable=False, default=1.0)
    submission_results = db.relationship('SubmissionTestResult', backref='test_case', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<TestCase {self.id}: {self.name} (Problem {self.problem_id})>'
    
    def to_dict(self, include_data=False):
        result = {
            'id': self.id,
            'problem_id': self.problem_id,
            'name': self.name,
            'complexity_hint': self.complexity_hint,
            'input_size': self.input_size,
            'is_sample': self.is_sample,
            'is_hidden': self.is_hidden,
            'weight': self.weight,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_data or self.is_sample:
            result.update({
                'input_data': self.input_data,
                'expected_output': self.expected_output
            })
            
        return result
