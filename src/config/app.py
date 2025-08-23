import os
from .database import DatabaseConfig


class AppConfig:
    """Application configuration settings."""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '8000'))
    
    # Docker settings
    DOCKER_CPP_IMAGE = os.getenv('DOCKER_CPP_IMAGE', 'adaptivejudge-cpp:latest')
    DOCKER_PYTHON_IMAGE = os.getenv('DOCKER_PYTHON_IMAGE', 'adaptivejudge-python:latest')
    DOCKER_TIMEOUT = int(os.getenv('DOCKER_TIMEOUT', '30'))  # seconds
    DOCKER_MEMORY_LIMIT = os.getenv('DOCKER_MEMORY_LIMIT', '128m')
    
    # Execution settings
    DEFAULT_TIME_LIMIT = float(os.getenv('DEFAULT_TIME_LIMIT', '1.0'))  # seconds
    DEFAULT_MEMORY_LIMIT = int(os.getenv('DEFAULT_MEMORY_LIMIT', '128'))  # MB
    MAX_SOURCE_CODE_SIZE = int(os.getenv('MAX_SOURCE_CODE_SIZE', '64000'))  # bytes
    
    # Benchmark settings
    BENCHMARK_REPETITIONS = int(os.getenv('BENCHMARK_REPETITIONS', '5'))
    BENCHMARK_FACTOR_CAP = float(os.getenv('BENCHMARK_FACTOR_CAP', '12.0'))
    BENCHMARK_MIN_FACTOR = float(os.getenv('BENCHMARK_MIN_FACTOR', '1.0'))
    BENCHMARK_STABILITY_THRESHOLD = float(os.getenv('BENCHMARK_STABILITY_THRESHOLD', '0.1'))  # IQR threshold
    
    # File paths
    TEMP_DIR = os.getenv('TEMP_DIR', '/tmp/adaptive-judge')
    REFERENCE_SOLUTIONS_DIR = os.getenv('REFERENCE_SOLUTIONS_DIR', 'data/reference_solutions')
    PROBLEMS_DATA_DIR = os.getenv('PROBLEMS_DATA_DIR', 'data/problems')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/adaptive_judge.log')
    
    @classmethod
    def get_flask_config(cls):
        """Get Flask application configuration."""
        config = {
            'SECRET_KEY': cls.SECRET_KEY,
            'DEBUG': cls.DEBUG,
        }
        
        # Add database configuration
        config.update(DatabaseConfig.get_config())
        
        return config
    
    @classmethod
    def init_directories(cls):
        """Initialize required directories."""
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
    """Development configuration."""
    DEBUG = True


class ProductionConfig(AppConfig):
    """Production configuration."""
    DEBUG = False


class TestingConfig(AppConfig):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    
    @classmethod
    def get_flask_config(cls):
        """Get Flask test configuration."""
        from .database import TestDatabaseConfig
        
        config = {
            'SECRET_KEY': 'test-secret-key',
            'DEBUG': cls.DEBUG,
            'TESTING': cls.TESTING,
        }
        
        # Add test database configuration
        config.update(TestDatabaseConfig.get_config())
        
        return config


# Configuration factory
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """Get configuration class based on environment."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    return config_map.get(config_name, DevelopmentConfig)
