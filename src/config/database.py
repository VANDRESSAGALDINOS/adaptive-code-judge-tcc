import os
from urllib.parse import quote_plus


class DatabaseConfig:
    """Database configuration settings."""
    
    @staticmethod
    def get_database_uri():
        """Get database URI from environment variables or use SQLite default."""
        # PostgreSQL configuration (production)
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'adaptive_judge')
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', '')
        
        # If PostgreSQL credentials are provided, use PostgreSQL
        if db_password or db_user != 'postgres':
            # URL encode password to handle special characters
            encoded_password = quote_plus(db_password) if db_password else ''
            return f'postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}'
        
        # SQLite fallback (development/testing)
        sqlite_path = os.getenv('SQLITE_PATH', 'data/adaptive_judge.db')
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
        
        return f'sqlite:///{sqlite_path}'
    
    @staticmethod
    def get_config():
        """Get SQLAlchemy configuration."""
        return {
            'SQLALCHEMY_DATABASE_URI': DatabaseConfig.get_database_uri(),
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'SQLALCHEMY_ENGINE_OPTIONS': {
                'pool_recycle': 3600,  # Recycle connections after 1 hour
                'pool_pre_ping': True,  # Validate connections before use
            }
        }


class TestDatabaseConfig(DatabaseConfig):
    """Test database configuration."""
    
    @staticmethod
    def get_database_uri():
        """Get test database URI."""
        return 'sqlite:///:memory:'  # In-memory SQLite for testing
    
    @staticmethod
    def get_config():
        """Get test SQLAlchemy configuration."""
        return {
            'SQLALCHEMY_DATABASE_URI': TestDatabaseConfig.get_database_uri(),
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'TESTING': True
        }
