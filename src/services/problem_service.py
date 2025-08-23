import logging
from typing import List, Optional, Dict, Any

from models import db, Problem, TestCase
from config.app import AppConfig


logger = logging.getLogger(__name__)


class ProblemService:
    """Service for managing problems and test cases."""
    
    def __init__(self, config: AppConfig = None):
        """Initialize problem service."""
        self.config = config or AppConfig()
    
    def create_problem(
        self,
        title: str,
        description: str,
        max_input_size: int = None,
        time_limit_base: float = None,
        memory_limit: int = None,
        difficulty: str = 'medium',
        tags: List[str] = None
    ) -> Problem:
        """Create a new problem."""
        
        if max_input_size is None:
            max_input_size = 1000000
        if time_limit_base is None:
            time_limit_base = self.config.DEFAULT_TIME_LIMIT
        if memory_limit is None:
            memory_limit = self.config.DEFAULT_MEMORY_LIMIT
        
        problem = Problem(
            title=title,
            description=description,
            max_input_size=max_input_size,
            time_limit_base=time_limit_base,
            memory_limit=memory_limit,
            difficulty=difficulty,
            tags=','.join(tags) if tags else None
        )
        
        db.session.add(problem)
        db.session.commit()
        
        logger.info(f"Created problem {problem.id}: {title}")
        return problem
    
    def add_test_case(
        self,
        problem_id: int,
        name: str,
        input_data: str,
        expected_output: str,
        complexity_hint: str = None,
        input_size: int = None,
        is_sample: bool = False,
        is_hidden: bool = True,
        weight: float = 1.0
    ) -> TestCase:
        """Add a test case to a problem."""
        
        # Validate problem exists
        problem = Problem.query.get(problem_id)
        if not problem:
            raise ValueError(f"Problem {problem_id} not found")
        
        # Calculate input size if not provided
        if input_size is None:
            input_size = len(input_data.encode('utf-8'))
        
        test_case = TestCase(
            problem_id=problem_id,
            name=name,
            input_data=input_data,
            expected_output=expected_output,
            complexity_hint=complexity_hint,
            input_size=input_size,
            is_sample=is_sample,
            is_hidden=is_hidden,
            weight=weight
        )
        
        db.session.add(test_case)
        db.session.commit()
        
        logger.info(f"Added test case {test_case.id} ({name}) to problem {problem_id}")
        return test_case
    
    def get_problem(self, problem_id: int) -> Optional[Problem]:
        """Get problem by ID."""
        return Problem.query.get(problem_id)
    
    def get_problems(
        self, 
        active_only: bool = True, 
        difficulty: str = None, 
        tags: List[str] = None,
        limit: int = 100
    ) -> List[Problem]:
        """Get problems with optional filtering."""
        
        query = Problem.query
        
        if active_only:
            query = query.filter_by(is_active=True)
        
        if difficulty:
            query = query.filter_by(difficulty=difficulty)
        
        if tags:
            # Filter by tags (simple contains check)
            for tag in tags:
                query = query.filter(Problem.tags.contains(tag))
        
        return query.order_by(Problem.created_at.desc()).limit(limit).all()
    
    def get_test_cases(
        self, 
        problem_id: int, 
        include_hidden: bool = False,
        sample_only: bool = False
    ) -> List[TestCase]:
        """Get test cases for a problem."""
        
        query = TestCase.query.filter_by(problem_id=problem_id)
        
        if sample_only:
            query = query.filter_by(is_sample=True)
        elif not include_hidden:
            query = query.filter_by(is_hidden=False)
        
        return query.order_by(TestCase.created_at.asc()).all()
    
    def update_problem(self, problem_id: int, **kwargs) -> Optional[Problem]:
        """Update problem fields."""
        
        problem = Problem.query.get(problem_id)
        if not problem:
            return None
        
        # Update allowed fields
        allowed_fields = [
            'title', 'description', 'max_input_size', 'time_limit_base',
            'memory_limit', 'difficulty', 'tags', 'is_active'
        ]
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                if field == 'tags' and isinstance(value, list):
                    value = ','.join(value)
                setattr(problem, field, value)
        
        db.session.commit()
        
        logger.info(f"Updated problem {problem_id}")
        return problem
    
    def delete_problem(self, problem_id: int) -> bool:
        """Delete a problem and all related data."""
        
        problem = Problem.query.get(problem_id)
        if not problem:
            return False
        
        # Soft delete by marking as inactive
        problem.is_active = False
        db.session.commit()
        
        logger.info(f"Deactivated problem {problem_id}")
        return True
    
    def delete_test_case(self, test_case_id: int) -> bool:
        """Delete a test case."""
        
        test_case = TestCase.query.get(test_case_id)
        if not test_case:
            return False
        
        db.session.delete(test_case)
        db.session.commit()
        
        logger.info(f"Deleted test case {test_case_id}")
        return True
    
    def get_problem_statistics(self, problem_id: int) -> Dict[str, Any]:
        """Get statistics for a problem."""
        
        problem = Problem.query.get(problem_id)
        if not problem:
            return {}
        
        # Count test cases
        total_test_cases = TestCase.query.filter_by(problem_id=problem_id).count()
        sample_test_cases = TestCase.query.filter_by(problem_id=problem_id, is_sample=True).count()
        
        # Count submissions
        from models import Submission
        total_submissions = Submission.query.filter_by(problem_id=problem_id).count()
        
        # Count accepted submissions
        from models.submission import SubmissionResult
        accepted_submissions = Submission.query.filter_by(
            problem_id=problem_id, 
            result=SubmissionResult.ACCEPTED
        ).count()
        
        acceptance_rate = (accepted_submissions / total_submissions * 100) if total_submissions > 0 else 0
        
        return {
            'problem_id': problem_id,
            'total_test_cases': total_test_cases,
            'sample_test_cases': sample_test_cases,
            'hidden_test_cases': total_test_cases - sample_test_cases,
            'total_submissions': total_submissions,
            'accepted_submissions': accepted_submissions,
            'acceptance_rate': round(acceptance_rate, 2)
        }
