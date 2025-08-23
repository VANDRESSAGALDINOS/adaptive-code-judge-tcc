"""
O(n²) Quadratic Time Complexity Problem Definition
Matrix Sum - Calculate sum of all elements in a matrix
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.services.problem_service import ProblemService

def create_problem(problem_service: ProblemService):
    """Create O(n²) Quadratic Time problem: Matrix Sum"""
    
    problem = problem_service.create_problem(
        title="Matrix Sum (O(n²))",
        description="""
        Calculate the sum of all elements in a square matrix.
        
        This problem tests quadratic-time operations where each element 
        in an n×n matrix must be visited exactly once to compute the total sum.
        
        Input: 
        - First line: n (matrix dimension)
        - Next n lines: n integers each (matrix elements)
        
        Output: 
        - Sum of all matrix elements
        """,
        max_input_size=100000,  # Large matrix for clear differentiation
        time_limit_base=2.0,
        memory_limit=512,
        difficulty='medium',
        tags='matrix-sum,O(n²),quadratic,2d-array'
    )
    
    # Test cases designed to stress quadratic vs cubic performance
    test_cases = [
        {
            'name': 'small_matrix',
            'input': '3\n1 2 3\n4 5 6\n7 8 9',
            'output': '45',
            'complexity_hint': 'O(n²)',
            'input_size': 50,
            'description': 'Small 3×3 matrix'
        },
        {
            'name': 'medium_matrix',
            'input': '5\n' + '\n'.join([' '.join(map(str, range(i*5+1, (i+1)*5+1))) for i in range(5)]),
            'output': str(sum(range(1, 26))),  # 325
            'complexity_hint': 'O(n²)',
            'input_size': 200,
            'description': 'Medium 5×5 matrix'
        },
        {
            'name': 'identity_matrix',
            'input': '10\n' + '\n'.join([' '.join(['1' if i==j else '0' for j in range(10)]) for i in range(10)]),
            'output': '10',
            'complexity_hint': 'O(n²)',
            'input_size': 1000,
            'description': '10×10 identity matrix'
        },
        {
            'name': 'large_matrix',
            'input': '50\n' + '\n'.join([' '.join(map(str, range(i*50+1, (i+1)*50+1))) for i in range(50)]),
            'output': str(sum(range(1, 2501))),  # 3127500
            'complexity_hint': 'O(n²)',
            'input_size': 10000,
            'description': 'Large 50×50 matrix'
        },
        {
            'name': 'massive_matrix',
            'input': '1000\n' + '\n'.join([' '.join(map(str, [(i + j) % 10 + 1 for j in range(1000)])) for i in range(1000)]),
            'output': '5500000',  # Sum of 1000x1000 matrix with pattern (i+j)%10+1
            'complexity_hint': 'O(n²)',
            'input_size': 4000000,  # ~4MB input, 1M elements
            'description': 'Massive 1000×1000 matrix, algorithmic difference should dominate Docker overhead'
        }
    ]
    
    # Add test cases
    for i, tc in enumerate(test_cases):
        problem_service.add_test_case(
            problem_id=problem.id,
            name=tc['name'],
            input_data=tc['input'],
            expected_output=tc['output'],
            is_sample=i < 2  # First 2 are sample cases
        )
    
    print(f"✅ Created O(n²) problem: {problem.title}")
    print(f"   📊 Test cases: {len(test_cases)}")
    return problem

if __name__ == "__main__":
    # Test problem creation
    problem_service = ProblemService()
    problem = create_problem(problem_service)
    print("Problem created successfully!")
