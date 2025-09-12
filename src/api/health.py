from flask import Blueprint, jsonify
import docker
from models import db

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    health_status = {
        'status': 'healthy',
        'services': {}
    }
    try:
        db.session.execute('SELECT 1')
        health_status['services']['database'] = 'healthy'
    except Exception as e:
        health_status['services']['database'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    try:
        client = docker.from_env()
        client.ping()
        health_status['services']['docker'] = 'healthy'
    except Exception as e:
        health_status['services']['docker'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return jsonify(health_status), status_code


@health_bp.route('/health/detailed', methods=['GET'])
def detailed_health_check():
    
    from config.app import AppConfig
    
    health_info = {
        'status': 'healthy',
        'services': {},
        'configuration': {
            'docker_cpp_image': AppConfig.DOCKER_CPP_IMAGE,
            'docker_python_image': AppConfig.DOCKER_PYTHON_IMAGE,
            'default_time_limit': AppConfig.DEFAULT_TIME_LIMIT,
            'default_memory_limit': AppConfig.DEFAULT_MEMORY_LIMIT,
        },
        'docker_images': {}
    }
    try:
        from models import Problem, TestCase, Submission, Benchmark
        
        db.session.execute('SELECT 1')
        problem_count = Problem.query.count()
        test_case_count = TestCase.query.count()
        submission_count = Submission.query.count()
        benchmark_count = Benchmark.query.count()
        
        health_info['services']['database'] = {
            'status': 'healthy',
            'counts': {
                'problems': problem_count,
                'test_cases': test_case_count,
                'submissions': submission_count,
                'benchmarks': benchmark_count
            }
        }
    except Exception as e:
        health_info['services']['database'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
        health_info['status'] = 'unhealthy'
    try:
        client = docker.from_env()
        client.ping()
        required_images = [AppConfig.DOCKER_CPP_IMAGE, AppConfig.DOCKER_PYTHON_IMAGE]
        
        for image_name in required_images:
            try:
                image = client.images.get(image_name)
                health_info['docker_images'][image_name] = {
                    'status': 'available',
                    'id': image.short_id,
                    'created': image.attrs.get('Created', 'unknown')
                }
            except docker.errors.ImageNotFound:
                health_info['docker_images'][image_name] = {
                    'status': 'not_found',
                    'error': 'Image not built or not available'
                }
                health_info['status'] = 'unhealthy'
        
        health_info['services']['docker'] = {
            'status': 'healthy',
            'version': client.version()['Version']
        }
        
    except Exception as e:
        health_info['services']['docker'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
        health_info['status'] = 'unhealthy'
    
    status_code = 200 if health_info['status'] == 'healthy' else 503
    return jsonify(health_info), status_code
