#!/usr/bin/env python3
"""
Adaptive Code Judge - Main Application Entry Point

A system for automatic algorithm evaluation for competitions, teaching, or scientific benchmarks.
Supports multiple languages (C++, Python), isolated execution via Docker, and adaptive time limits.
"""

import os
import logging
from flask import Flask
from dotenv import load_dotenv

from config.app import get_config
from models import db
from api import problems_bp, submissions_bp, benchmarks_bp, health_bp


def create_app(config_name=None):
    """Create and configure Flask application."""
    
    # Load environment variables
    load_dotenv()
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config(config_name)
    app.config.update(config_class.get_flask_config())
    
    # Initialize directories
    config_class.init_directories()
    
    # Setup logging
    setup_logging(config_class)
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(problems_bp)
    app.register_blueprint(submissions_bp)
    app.register_blueprint(benchmarks_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        app.logger.info("Database tables created/verified")
    
    # Add some basic routes
    @app.route('/')
    def index():
        return {
            'name': 'Adaptive Code Judge',
            'version': '1.0.0',
            'description': 'Automatic algorithm evaluation system',
            'endpoints': {
                'health': '/health',
                'problems': '/api/problems',
                'submissions': '/api/submissions',
                'benchmarks': '/api/benchmarks'
            }
        }
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Endpoint not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal server error: {error}")
        return {'error': 'Internal server error'}, 500
    
    app.logger.info("Adaptive Code Judge application created successfully")
    return app


def setup_logging(config_class):
    """Setup application logging."""
    
    log_level = getattr(logging, config_class.LOG_LEVEL.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup file handler if log file is specified
    if config_class.LOG_FILE:
        os.makedirs(os.path.dirname(config_class.LOG_FILE), exist_ok=True)
        file_handler = logging.FileHandler(config_class.LOG_FILE)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        
        # Add to root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)
        root_logger.setLevel(log_level)
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    # Add to Flask's logger
    flask_logger = logging.getLogger('werkzeug')
    flask_logger.setLevel(logging.WARNING)  # Reduce werkzeug verbosity


def main():
    """Main entry point for running the application."""
    
    app = create_app()
    config_class = get_config()
    
    app.logger.info(f"Starting Adaptive Code Judge on {config_class.HOST}:{config_class.PORT}")
    app.logger.info(f"Debug mode: {config_class.DEBUG}")
    app.logger.info(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Run the application
    app.run(
        host=config_class.HOST,
        port=config_class.PORT,
        debug=config_class.DEBUG,
        threaded=True
    )


if __name__ == '__main__':
    main()
