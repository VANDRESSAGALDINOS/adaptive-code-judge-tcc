import os
from urllib.parse import quote_plus


class DatabaseConfig:
    
    @staticmethod
    def get_database_uri():
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'adaptive_judge')
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', '')
        
        if db_password or db_user != 'postgres':
            encoded_password = quote_plus(db_password) if db_password else ''
            return f'postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}'
        
        sqlite_path = os.getenv('SQLITE_PATH', 'data/adaptive_judge.db')
        os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
        
        return f'sqlite:///{sqlite_path}'
    
    @staticmethod
    def get_config():
        return {
            'SQLALCHEMY_DATABASE_URI': DatabaseConfig.get_database_uri(),
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'SQLALCHEMY_ENGINE_OPTIONS': {
                'pool_recycle': 3600,
                'pool_pre_ping': True
            }
        }


class TestDatabaseConfig(DatabaseConfig):
    
    @staticmethod
    def get_database_uri():
        return 'sqlite:///:memory:'
    
    @staticmethod
    def get_config():
        return {
            'SQLALCHEMY_DATABASE_URI': TestDatabaseConfig.get_database_uri(),
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'TESTING': True
        }
