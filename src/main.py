#!/usr/bin/env python3

import os
import logging
from flask import Flask
from dotenv import load_dotenv

from config.app import get_config
from models import db
from api import problems_bp, submissions_bp, benchmarks_bp, health_bp


def create_app(config_name=None):
    load_dotenv()
    
    app = Flask(__name__)
    
    config_class = get_config(config_name)
    app.config.update(config_class.get_flask_config())
    
    config_class.init_directories()
    
    setup_logging(config_class)
    
    db.init_app(app)
    
    app.register_blueprint(health_bp)
    app.register_blueprint(problems_bp)
    app.register_blueprint(submissions_bp)
    app.register_blueprint(benchmarks_bp)
    
    with app.app_context():
        db.create_all()
        app.logger.info("Database tables created/verified")
    
    @app.route('/')
    def index():
        return {
            'service': 'adaptive-code-judge',
            'version': '1.0.0',
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
    
    log_level = getattr(logging, config_class.LOG_LEVEL.upper(), logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    if config_class.LOG_FILE:
        os.makedirs(os.path.dirname(config_class.LOG_FILE), exist_ok=True)
        file_handler = logging.FileHandler(config_class.LOG_FILE)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        
        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)
        root_logger.setLevel(log_level)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    flask_logger = logging.getLogger('werkzeug')
    flask_logger.setLevel(logging.WARNING)


def main():
    
    app = create_app()
    config_class = get_config()
    
    app.logger.info(f"Starting Adaptive Code Judge on {config_class.HOST}:{config_class.PORT}")
    app.logger.info(f"Debug mode: {config_class.DEBUG}")
    app.logger.info(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    app.run(
        host=config_class.HOST,
        port=config_class.PORT,
        debug=config_class.DEBUG,
        threaded=True
    )


if __name__ == '__main__':
    main()
