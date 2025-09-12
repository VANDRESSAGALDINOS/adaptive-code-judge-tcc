from flask import Blueprint, request, jsonify, current_app
from services.benchmark_service import BenchmarkService

benchmarks_bp = Blueprint('benchmarks', __name__, url_prefix='/api/benchmarks')


@benchmarks_bp.route('', methods=['POST'])
def create_benchmark():
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        if not data.get('problem_id'):
            return jsonify({'error': 'Missing required field: problem_id'}), 400
        
        service = BenchmarkService()
        benchmark = service.create_benchmark(
            problem_id=data['problem_id'],
            repetitions=data.get('repetitions'),
            activated_by=data.get('activated_by')
        )
        
        return jsonify(benchmark.to_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error creating benchmark: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@benchmarks_bp.route('/<int:benchmark_id>', methods=['GET'])
def get_benchmark(benchmark_id):
    
    try:
        from ..models import Benchmark
        
        benchmark = Benchmark.query.get(benchmark_id)
        
        if not benchmark:
            return jsonify({'error': 'Benchmark not found'}), 404
        
        result = benchmark.to_dict()
        
        include_times = request.args.get('include_times', 'false').lower() == 'true'
        if include_times:
            import json
            try:
                result['cpp_times_data'] = json.loads(benchmark.cpp_times) if benchmark.cpp_times else []
                result['python_times_data'] = json.loads(benchmark.python_times) if benchmark.python_times else []
            except json.JSONDecodeError:
                result['cpp_times_data'] = []
                result['python_times_data'] = []
        
        if benchmark.largest_test_case:
            result['largest_test_case'] = benchmark.largest_test_case.to_dict()
        
        return jsonify(result)
        
    except Exception as e:
        current_app.logger.error(f"Error getting benchmark {benchmark_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@benchmarks_bp.route('/problem/<int:problem_id>', methods=['GET'])
def get_benchmarks_for_problem(problem_id):
    
    try:
        from ..models import Benchmark
        
        benchmarks = Benchmark.query.filter_by(problem_id=problem_id).order_by(
            Benchmark.created_at.desc()
        ).all()
        
        return jsonify({
            'benchmarks': [b.to_dict() for b in benchmarks],
            'count': len(benchmarks)
        })
        
    except Exception as e:
        current_app.logger.error(f"Error getting benchmarks for problem {problem_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@benchmarks_bp.route('/problem/<int:problem_id>/active', methods=['GET'])
def get_active_benchmark(problem_id):
    
    try:
        service = BenchmarkService()
        benchmark = service.get_active_benchmark(problem_id)
        
        if not benchmark:
            return jsonify({'error': 'No active benchmark found for this problem'}), 404
        
        result = benchmark.to_dict()
        
        from ..models import ProblemBenchmarkActive
        active_info = ProblemBenchmarkActive.get_active_benchmark(problem_id)
        if active_info:
            result['active_benchmark_info'] = active_info.to_dict()
        
        return jsonify(result)
        
    except Exception as e:
        current_app.logger.error(f"Error getting active benchmark for problem {problem_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@benchmarks_bp.route('/problem/<int:problem_id>/active', methods=['PUT'])
def set_active_benchmark(problem_id):
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if not data.get('benchmark_id'):
            return jsonify({'error': 'Missing required field: benchmark_id'}), 400
        
        service = BenchmarkService()
        active_benchmark = service.set_active_benchmark(
            problem_id=problem_id,
            benchmark_id=data['benchmark_id'],
            activated_by=data.get('activated_by'),
            notes=data.get('notes')
        )
        
        return jsonify(active_benchmark.to_dict())
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error setting active benchmark for problem {problem_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@benchmarks_bp.route('/problem/<int:problem_id>/time-limit', methods=['GET'])
def get_time_limit(problem_id):
    
    try:
        language = request.args.get('language', 'cpp')
        
        service = BenchmarkService()
        time_limit = service.get_time_limit_for_submission(problem_id, language)
        
        active_benchmark = service.get_active_benchmark(problem_id)
        
        result = {
            'problem_id': problem_id,
            'language': language,
            'time_limit': time_limit,
            'has_active_benchmark': active_benchmark is not None,
            'benchmark_reliable': active_benchmark.is_reliable if active_benchmark else False
        }
        
        if active_benchmark:
            result['benchmark_id'] = active_benchmark.id
            result['adjustment_factor'] = active_benchmark.adjustment_factor_python
        
        return jsonify(result)
        
    except Exception as e:
        current_app.logger.error(f"Error getting time limit for problem {problem_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@benchmarks_bp.route('/<int:benchmark_id>/activate', methods=['POST'])
def activate_benchmark(benchmark_id):
    
    try:
        data = request.get_json() or {}
        
        from ..models import Benchmark
        benchmark = Benchmark.query.get(benchmark_id)
        
        if not benchmark:
            return jsonify({'error': 'Benchmark not found'}), 404
        
        service = BenchmarkService()
        active_benchmark = service.set_active_benchmark(
            problem_id=benchmark.problem_id,
            benchmark_id=benchmark_id,
            activated_by=data.get('activated_by'),
            notes=data.get('notes')
        )
        
        return jsonify({
            'active_benchmark': active_benchmark.to_dict()
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error activating benchmark {benchmark_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500
