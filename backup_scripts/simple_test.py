#!/usr/bin/env python3
"""
Simple test to verify the application works with explicit SQLite path.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set explicit SQLite path
os.environ['SQLITE_PATH'] = '/Users/vandressa.galdino/adaptive-code-judge/data/adaptive_judge.db'

def main():
    print("Starting Adaptive Code Judge Test...")
    print(f"SQLite path: {os.environ.get('SQLITE_PATH')}")
    
    try:
        from src.main import create_app
        app = create_app()
        
        with app.app_context():
            from src.models import db, Problem, TestCase
            from src.services import ProblemService
            
            # Create tables
            print("Creating database tables...")
            db.create_all()
            print("✓ Database tables created")
            
            # Test basic operations
            service = ProblemService()
            problem_count = Problem.query.count()
            print(f"✓ Current problems: {problem_count}")
            
            # Create a simple test problem
            if problem_count == 0:
                print("Creating test problem...")
                problem = service.create_problem(
                    title="Hello World",
                    description="Print 'Hello, World!' to stdout",
                    difficulty="easy",
                    tags=["basic", "output"]
                )
                print(f"✓ Created problem: {problem.title}")
                
                # Add a test case
                test_case = service.add_test_case(
                    problem_id=problem.id,
                    name="basic_test",
                    input_data="",
                    expected_output="Hello, World!",
                    is_sample=True,
                    is_hidden=False
                )
                print(f"✓ Added test case: {test_case.name}")
            
            print("\n" + "="*50)
            print("✓ Basic system test PASSED!")
            print("\nThe application core is working correctly.")
            print("\nNext steps:")
            print("1. Install Docker to enable code execution")
            print("2. Build Docker images:")
            print("   cd docker")
            print("   docker build -t adaptivejudge-cpp:latest -f Dockerfile.cpp .")
            print("   docker build -t adaptivejudge-python:latest -f Dockerfile.python .")
            print("3. Start the full application:")
            print("   PYTHONPATH=/Users/vandressa.galdino/adaptive-code-judge python3 src/main.py")
            
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
