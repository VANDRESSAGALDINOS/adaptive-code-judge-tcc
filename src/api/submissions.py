from flask import Blueprint, request, jsonify, current_app
from services.submission_service import SubmissionService

submissions_bp = Blueprint('submissions', __name__, url_prefix='/api/submissions')


@submissions_bp.route('', methods=['POST'])
def create_submission():
    """Create a new submission."""
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['problem_id', 'language', 'source_code']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        service = SubmissionService()
        submission = service.create_submission(
            problem_id=data['problem_id'],
            language=data['language'],
            source_code=data['source_code'],
            user_id=data.get('user_id')
        )
        
        return jsonify(submission.to_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error creating submission: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@submissions_bp.route('/<int:submission_id>', methods=['GET'])
def get_submission(submission_id):
    """Get a specific submission by ID."""
    
    try:
        service = SubmissionService()
        submission = service.get_submission(submission_id)
        
        if not submission:
            return jsonify({'error': 'Submission not found'}), 404
        
        # Check if source code should be included
        include_code = request.args.get('include_code', 'false').lower() == 'true'
        
        result = submission.to_dict(include_code=include_code)
        
        # Include test results if requested
        include_results = request.args.get('include_results', 'true').lower() == 'true'
        if include_results:
            test_results = service.get_submission_results(submission_id)
            
            # Check if output should be included (only for non-hidden test cases or with permission)
            include_output = request.args.get('include_output', 'false').lower() == 'true'
            
            result['test_results'] = []
            for tr in test_results:
                tr_dict = tr.to_dict(include_output=include_output)
                
                # Include test case info (but not the data unless it's a sample)
                tr_dict['test_case'] = tr.test_case.to_dict(include_data=tr.test_case.is_sample)
                
                result['test_results'].append(tr_dict)
        
        return jsonify(result)
        
    except Exception as e:
        current_app.logger.error(f"Error getting submission {submission_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@submissions_bp.route('', methods=['GET'])
def get_submissions():
    """Get submissions with optional filtering."""
    
    try:
        service = SubmissionService()
        
        # Parse query parameters
        problem_id = request.args.get('problem_id', type=int)
        user_id = request.args.get('user_id')
        limit = min(int(request.args.get('limit', 100)), 1000)  # Cap at 1000
        
        if not problem_id:
            return jsonify({'error': 'problem_id parameter is required'}), 400
        
        submissions = service.get_submissions_for_problem(
            problem_id=problem_id,
            user_id=user_id,
            limit=limit
        )
        
        return jsonify({
            'submissions': [s.to_dict() for s in submissions],
            'count': len(submissions)
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting submissions: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@submissions_bp.route('/<int:submission_id>/results', methods=['GET'])
def get_submission_results(submission_id):
    """Get detailed test results for a submission."""
    
    try:
        service = SubmissionService()
        
        # Check if submission exists
        submission = service.get_submission(submission_id)
        if not submission:
            return jsonify({'error': 'Submission not found'}), 404
        
        test_results = service.get_submission_results(submission_id)
        
        # Check if output should be included
        include_output = request.args.get('include_output', 'false').lower() == 'true'
        
        results = []
        for tr in test_results:
            tr_dict = tr.to_dict(include_output=include_output)
            
            # Include test case info
            tr_dict['test_case'] = tr.test_case.to_dict(include_data=tr.test_case.is_sample)
            
            results.append(tr_dict)
        
        return jsonify({
            'submission_id': submission_id,
            'test_results': results,
            'summary': {
                'total_tests': len(results),
                'passed_tests': sum(1 for r in results if r['passed']),
                'score': submission.score
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting results for submission {submission_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@submissions_bp.route('/judge', methods=['POST'])
def judge_submission():
    """Quick judge endpoint for immediate evaluation."""
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['problem_id', 'language', 'source_code']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        service = SubmissionService()
        submission = service.create_submission(
            problem_id=data['problem_id'],
            language=data['language'],
            source_code=data['source_code'],
            user_id=data.get('user_id', 'anonymous')
        )
        
        # Return submission with results
        test_results = service.get_submission_results(submission.id)
        
        result = submission.to_dict()
        result['test_results'] = []
        
        for tr in test_results:
            tr_dict = tr.to_dict(include_output=tr.test_case.is_sample)
            tr_dict['test_case'] = tr.test_case.to_dict(include_data=tr.test_case.is_sample)
            result['test_results'].append(tr_dict)
        
        return jsonify(result), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error judging submission: {e}")
        return jsonify({'error': 'Internal server error'}), 500
