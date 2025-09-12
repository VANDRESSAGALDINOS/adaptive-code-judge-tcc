import os
from .database import DatabaseConfig


class AppConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '8000'))
    
    DOCKER_CPP_IMAGE = os.getenv('DOCKER_CPP_IMAGE', 'adaptivejudge-cpp:latest')
    DOCKER_PYTHON_IMAGE = os.getenv('DOCKER_PYTHON_IMAGE', 'adaptivejudge-python:latest')
    DOCKER_TIMEOUT = int(os.getenv('DOCKER_TIMEOUT', '30'))
    DOCKER_MEMORY_LIMIT = os.getenv('DOCKER_MEMORY_LIMIT', '128m')
    
    DEFAULT_TIME_LIMIT = float(os.getenv('DEFAULT_TIME_LIMIT', '1.0'))
    DEFAULT_MEMORY_LIMIT = int(os.getenv('DEFAULT_MEMORY_LIMIT', '128'))
    MAX_SOURCE_CODE_SIZE = int(os.getenv('MAX_SOURCE_CODE_SIZE', '64000'))
    
    BENCHMARK_REPETITIONS = int(os.getenv('BENCHMARK_REPETITIONS', '5'))
    BENCHMARK_FACTOR_CAP = float(os.getenv('BENCHMARK_FACTOR_CAP', '12.0'))
    BENCHMARK_MIN_FACTOR = float(os.getenv('BENCHMARK_MIN_FACTOR', '1.0'))
    BENCHMARK_STABILITY_THRESHOLD = float(os.getenv('BENCHMARK_STABILITY_THRESHOLD', '0.1'))
    
    TEMP_DIR = os.getenv('TEMP_DIR', '/tmp/adaptive-judge')
    REFERENCE_SOLUTIONS_DIR = os.getenv('REFERENCE_SOLUTIONS_DIR', 'data/reference_solutions')
    PROBLEMS_DATA_DIR = os.getenv('PROBLEMS_DATA_DIR', 'data/problems')
    
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/adaptive_judge.log')
    
    @classmethod
    def get_flask_config(cls):
        config = {
            'SECRET_KEY': cls.SECRET_KEY,
            'DEBUG': cls.DEBUG,
        }
        config.update(DatabaseConfig.get_config())
        
        return config
    
    @classmethod
    def init_directories(cls):
        directories = [
            cls.TEMP_DIR,
            cls.REFERENCE_SOLUTIONS_DIR,
            cls.PROBLEMS_DATA_DIR,
            os.path.dirname(cls.LOG_FILE) if cls.LOG_FILE else None
        ]
        
        for directory in directories:
            if directory:
                os.makedirs(directory, exist_ok=True)


class DevelopmentConfig(AppConfig):
    DEBUG = True


class ProductionConfig(AppConfig):
    DEBUG = False


class TestingConfig(AppConfig):
    TESTING = True
    DEBUG = True
    
    @classmethod
    def get_flask_config(cls):
        from .database import TestDatabaseConfig
        
        config = {
            'SECRET_KEY': 'test-secret-key',
            'DEBUG': cls.DEBUG,
            'TESTING': cls.TESTING,
        }
        config.update(TestDatabaseConfig.get_config())
        
        return config

config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    return config_map.get(config_name, DevelopmentConfig)
