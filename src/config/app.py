import os
from .database import DatabaseConfig


class AppConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '8000'))
    
    # Canonical execution parameters — MUST be identical across all pipelines
    # (service, complexity runner, real-world scripts). See artigo Sec. 3.2/3.8.
    DOCKER_CPP_IMAGE = os.getenv('DOCKER_CPP_IMAGE', 'adaptive-judge-cpp:latest')
    DOCKER_PYTHON_IMAGE = os.getenv('DOCKER_PYTHON_IMAGE', 'adaptive-judge-python:latest')
    DOCKER_TIMEOUT = int(os.getenv('DOCKER_TIMEOUT', '30'))
    DOCKER_MEMORY_LIMIT = os.getenv('DOCKER_MEMORY_LIMIT', '512m')
    DOCKER_CPUS = os.getenv('DOCKER_CPUS', '1.0')
    CPP_COMPILE_FLAGS = os.getenv('CPP_COMPILE_FLAGS', '-O2')

    DEFAULT_TIME_LIMIT = float(os.getenv('DEFAULT_TIME_LIMIT', '1.0'))
    DEFAULT_MEMORY_LIMIT = int(os.getenv('DEFAULT_MEMORY_LIMIT', '512'))
    MAX_SOURCE_CODE_SIZE = int(os.getenv('MAX_SOURCE_CODE_SIZE', '64000'))

    # beta (adjustment factor) is the raw median ratio, with NO clamp.
    # Clamping would hide the very phenomenon the work demonstrates (beta >> 2-3x).
    BENCHMARK_REPETITIONS = int(os.getenv('BENCHMARK_REPETITIONS', '5'))
    BENCHMARK_STABILITY_THRESHOLD = float(os.getenv('BENCHMARK_STABILITY_THRESHOLD', '0.1'))

    # Adaptive repetition (artigo Sec. 3.2): run in blocks, recompute IQR/median
    # each block, stop when IQR/median < per-language threshold or at the cap.
    BENCHMARK_MIN_REPETITIONS = int(os.getenv('BENCHMARK_MIN_REPETITIONS', '5'))
    BENCHMARK_BLOCK_SIZE = int(os.getenv('BENCHMARK_BLOCK_SIZE', '5'))
    BENCHMARK_MAX_REPETITIONS = int(os.getenv('BENCHMARK_MAX_REPETITIONS', '35'))
    BENCHMARK_IQR_THRESHOLD_CPP = float(os.getenv('BENCHMARK_IQR_THRESHOLD_CPP', '0.15'))
    BENCHMARK_IQR_THRESHOLD_PYTHON = float(os.getenv('BENCHMARK_IQR_THRESHOLD_PYTHON', '0.20'))

    # beta is a ratio of medians (no closed-form CI); its 95% CI is obtained by
    # bootstrap resampling of the measured times (artigo Sec. 3.2/3.5, Efron 1979).
    # Seed fixed for reproducibility (Sec. 3.8).
    BENCHMARK_BOOTSTRAP_RESAMPLES = int(os.getenv('BENCHMARK_BOOTSTRAP_RESAMPLES', '10000'))
    BENCHMARK_BOOTSTRAP_SEED = int(os.getenv('BENCHMARK_BOOTSTRAP_SEED', '42'))
    
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
