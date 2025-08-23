from flask import Blueprint, request, jsonify, current_app
from services.problem_service import ProblemService
from models import Problem

problems_bp = Blueprint('problems', __name__, url_prefix='/api/problems')


@problems_bp.route('', methods=['GET'])
def get_problems():
    """Get list of problems with optional filtering."""
    
    try:
        service = ProblemService()
        
        # Parse query parameters
        active_only = request.args.get('active', 'true').lower() == 'true'
        difficulty = request.args.get('difficulty')
        tags = request.args.getlist('tags')
        limit = min(int(request.args.get('limit', 100)), 1000)  # Cap at 1000
        
        problems = service.get_problems(
            active_only=active_only,
            difficulty=difficulty,
            tags=tags,
            limit=limit
        )
        
        return jsonify({
            'problems': [p.to_dict() for p in problems],
            'count': len(problems)
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting problems: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@problems_bp.route('/<int:problem_id>', methods=['GET'])
def get_problem(problem_id):
    """Get a specific problem by ID."""
    
    try:
        service = ProblemService()
        problem = service.get_problem(problem_id)
        
        if not problem:
            return jsonify({'error': 'Problem not found'}), 404
        
        # Include sample test cases
        include_samples = request.args.get('include_samples', 'true').lower() == 'true'
        result = problem.to_dict()
        
        if include_samples:
            sample_test_cases = service.get_test_cases(problem_id, sample_only=True)
            result['sample_test_cases'] = [tc.to_dict(include_data=True) for tc in sample_test_cases]
        
        return jsonify(result)
        
    except Exception as e:
        current_app.logger.error(f"Error getting problem {problem_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@problems_bp.route('', methods=['POST'])
def create_problem():
    """Create a new problem."""
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['title', 'description']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        service = ProblemService()
        problem = service.create_problem(
            title=data['title'],
            description=data['description'],
            max_input_size=data.get('max_input_size'),
            time_limit_base=data.get('time_limit_base'),
            memory_limit=data.get('memory_limit'),
            difficulty=data.get('difficulty', 'medium'),
            tags=data.get('tags', [])
        )
        
        return jsonify(problem.to_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error creating problem: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@problems_bp.route('/<int:problem_id>/test-cases', methods=['GET'])
def get_test_cases(problem_id):
    """Get test cases for a problem."""
    
    try:
        service = ProblemService()
        
        # Check if problem exists
        problem = service.get_problem(problem_id)
        if not problem:
            return jsonify({'error': 'Problem not found'}), 404
        
        # Parse query parameters
        include_hidden = request.args.get('include_hidden', 'false').lower() == 'true'
        sample_only = request.args.get('sample_only', 'false').lower() == 'true'
        
        test_cases = service.get_test_cases(
            problem_id=problem_id,
            include_hidden=include_hidden,
            sample_only=sample_only
        )
        
        return jsonify({
            'test_cases': [tc.to_dict(include_data=not tc.is_hidden or include_hidden) for tc in test_cases],
            'count': len(test_cases)
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting test cases for problem {problem_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@problems_bp.route('/<int:problem_id>/test-cases', methods=['POST'])
def add_test_case(problem_id):
    """Add a test case to a problem."""
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['name', 'input_data', 'expected_output']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        service = ProblemService()
        test_case = service.add_test_case(
            problem_id=problem_id,
            name=data['name'],
            input_data=data['input_data'],
            expected_output=data['expected_output'],
            complexity_hint=data.get('complexity_hint'),
            input_size=data.get('input_size'),
            is_sample=data.get('is_sample', False),
            is_hidden=data.get('is_hidden', True),
            weight=data.get('weight', 1.0)
        )
        
        return jsonify(test_case.to_dict(include_data=True)), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error adding test case to problem {problem_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@problems_bp.route('/<int:problem_id>/statistics', methods=['GET'])
def get_problem_statistics(problem_id):
    """Get statistics for a problem."""
    
    try:
        service = ProblemService()
        
        # Check if problem exists
        problem = service.get_problem(problem_id)
        if not problem:
            return jsonify({'error': 'Problem not found'}), 404
        
        statistics = service.get_problem_statistics(problem_id)
        return jsonify(statistics)
        
    except Exception as e:
        current_app.logger.error(f"Error getting statistics for problem {problem_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@problems_bp.route('/<int:problem_id>', methods=['PUT'])
def update_problem(problem_id):
    """Update a problem."""
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        service = ProblemService()
        problem = service.update_problem(problem_id, **data)
        
        if not problem:
            return jsonify({'error': 'Problem not found'}), 404
        
        return jsonify(problem.to_dict())
        
    except Exception as e:
        current_app.logger.error(f"Error updating problem {problem_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@problems_bp.route('/<int:problem_id>', methods=['DELETE'])
def delete_problem(problem_id):
    """Delete (deactivate) a problem."""
    
    try:
        service = ProblemService()
        success = service.delete_problem(problem_id)
        
        if not success:
            return jsonify({'error': 'Problem not found'}), 404
        
        return jsonify({'message': 'Problem deactivated successfully'})
        
    except Exception as e:
        current_app.logger.error(f"Error deleting problem {problem_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@problems_bp.route('/test-cases/<int:test_case_id>', methods=['DELETE'])
def delete_test_case(test_case_id):
    """Delete a test case."""
    
    try:
        service = ProblemService()
        success = service.delete_test_case(test_case_id)
        
        if not success:
            return jsonify({'error': 'Test case not found'}), 404
        
        return jsonify({'message': 'Test case deleted successfully'})
        
    except Exception as e:
        current_app.logger.error(f"Error deleting test case {test_case_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500
