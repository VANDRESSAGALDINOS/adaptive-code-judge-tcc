#!/usr/bin/env python3
"""
Basic test script to verify the system components work without Docker.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from src.models import db, Problem, TestCase
        print("✓ Models imported successfully")
    except Exception as e:
        print(f"✗ Models import failed: {e}")
        return False
    
    try:
        from src.config.app import AppConfig
        print("✓ Config imported successfully")
    except Exception as e:
        print(f"✗ Config import failed: {e}")
        return False
    
    try:
        from src.services import ProblemService
        print("✓ Services imported successfully")
    except Exception as e:
        print(f"✗ Services import failed: {e}")
        return False
    
    return True

def test_database():
    """Test database creation."""
    print("\nTesting database...")
    
    try:
        from src.main import create_app
        app = create_app()
        
        with app.app_context():
            from src.models import db
            db.create_all()
            print("✓ Database tables created successfully")
            
            # Test basic operations
            from src.models import Problem
            problem_count = Problem.query.count()
            print(f"✓ Database query works, found {problem_count} problems")
            
        return True
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_api_creation():
    """Test API application creation."""
    print("\nTesting API creation...")
    
    try:
        from src.main import create_app
        app = create_app()
        
        with app.test_client() as client:
            # Test root endpoint
            response = client.get('/')
            if response.status_code == 200:
                print("✓ Root endpoint works")
            else:
                print(f"✗ Root endpoint failed: {response.status_code}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ API creation test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Adaptive Code Judge - Basic System Test")
    print("=" * 50)
    
    # Note about Docker
    print("Note: Docker tests will be skipped (Docker not available)")
    print()
    
    success = True
    
    success &= test_imports()
    success &= test_database()
    success &= test_api_creation()
    
    print("\n" + "=" * 50)
    if success:
        print("✓ All basic tests passed!")
        print("\nThe system core is working correctly.")
        print("\nTo fully test the system:")
        print("1. Install Docker")
        print("2. Build the Docker images")
        print("3. Run the full application")
    else:
        print("✗ Some tests failed!")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
