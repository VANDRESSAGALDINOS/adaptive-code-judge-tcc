"""
O(n) Linear Time Complexity Problem Definition
Array Sum - Calculate sum of array elements
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.services.problem_service import ProblemService

def create_problem(problem_service: ProblemService):
    """Create O(n) Linear Time problem: Array Sum"""
    
    problem = problem_service.create_problem(
        title="Array Sum (O(n))",
        description="""
        Calculate the sum of all elements in an array.
        
        This problem tests linear-time operations where each element 
        must be visited exactly once to compute the total sum.
        
        Input: 
        - First line: n (number of elements)
        - Second line: n integers
        
        Output: 
        - Sum of all elements
        """,
        max_input_size=500000,  # Large input for clear differentiation
        time_limit_base=1.0,
        memory_limit=256,
        difficulty='easy',
        tags='array-sum,O(n),linear,iteration'
    )
    
    # Test cases designed to stress linear vs quadratic performance
    test_cases = [
        {
            'name': 'small_array',
            'input': '5\n1 2 3 4 5',
            'output': '15',
            'complexity_hint': 'O(n)',
            'input_size': 50,
            'description': 'Small array (n=5)'
        },
        {
            'name': 'medium_array',
            'input': '10\n10 20 30 40 50 60 70 80 90 100',
            'output': '550', 
            'complexity_hint': 'O(n)',
            'input_size': 100,
            'description': 'Medium array (n=10)'
        },
        {
            'name': 'large_array',
            'input': f'1000\n{" ".join(map(str, range(1, 1001)))}',
            'output': str(sum(range(1, 1001))),  # 500500
            'complexity_hint': 'O(n)',
            'input_size': 10000,
            'description': 'Large array (n=1000)'
        },
        {
            'name': 'negative_numbers',
            'input': f'100\n{" ".join(map(str, range(-50, 50)))}',
            'output': str(sum(range(-50, 50))),  # -50
            'complexity_hint': 'O(n)',
            'input_size': 1000,
            'description': 'Array with negative numbers (n=100)'
        },
        {
            'name': 'massive_array',
            'input': f'1000000\n{" ".join(map(str, range(1, 1000001)))}',
            'output': str(sum(range(1, 1000001))),  # 500000500000
            'complexity_hint': 'O(n)',
            'input_size': 8000000,  # ~8MB input
            'description': 'Massive array (n=1M), algorithmic difference should dominate Docker overhead'
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
    
    print(f"✅ Created O(n) problem: {problem.title}")
    print(f"   📊 Test cases: {len(test_cases)}")
    return problem

if __name__ == "__main__":
    # Test problem creation
    problem_service = ProblemService()
    problem = create_problem(problem_service)
    print("Problem created successfully!")
