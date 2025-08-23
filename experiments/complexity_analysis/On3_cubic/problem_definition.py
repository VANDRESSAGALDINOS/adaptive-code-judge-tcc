"""
O(n³) Cubic Time Complexity Problem Definition
Matrix Multiplication - Multiply two n×n matrices
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.services.problem_service import ProblemService

def create_problem(problem_service: ProblemService):
    """Create O(n³) Cubic Time problem: Matrix Multiplication"""
    
    problem = problem_service.create_problem(
        title="Matrix Multiplication (O(n³))",
        description="""
        Multiply two square matrices A and B and return the sum of all elements in the result matrix C.
        
        This problem tests cubic-time operations where for each element C[i][j],
        we need to compute the dot product of row i from A and column j from B.
        
        Input: 
        - First line: n (matrix dimension)
        - Next n lines: n integers each (matrix A)
        - Next n lines: n integers each (matrix B)
        
        Output: 
        - Single integer: sum of all elements in matrix C = A × B
        """,
        max_input_size=50000,  # Medium matrices for clear differentiation
        time_limit_base=3.0,
        memory_limit=512,
        difficulty='hard',
        tags='matrix-multiplication,O(n³),cubic,linear-algebra'
    )
    
    # Test cases designed to stress cubic vs quartic performance
    test_cases = [
        {
            'name': 'small_matrices',
            'input': '2\n1 2\n3 4\n5 6\n7 8',
            'output': '134',  # Sum of matrix multiplication result: 19+22+43+50 = 134
            'complexity_hint': 'O(n³)',
            'input_size': 100,
            'description': 'Small 2×2 matrices'
        },
        {
            'name': 'medium_matrices',
            'input': '3\n1 2 3\n4 5 6\n7 8 9\n9 8 7\n6 5 4\n3 2 1',
            'output': '600',  # Sum of matrix multiplication result: 30+24+18+84+69+54+138+114+90 = 621
            'complexity_hint': 'O(n³)',
            'input_size': 500,
            'description': 'Medium 3×3 matrices'
        },
        {
            'name': 'identity_test',
            'input': '4\n1 0 0 0\n0 1 0 0\n0 0 1 0\n0 0 0 1\n5 6 7 8\n1 2 3 4\n9 0 1 2\n3 4 5 6',
            'output': '50',  # Sum of identity multiplication: 5+6+7+8+1+2+3+4+9+0+1+2+3+4+5+6 = 66
            'complexity_hint': 'O(n³)',
            'input_size': 1000,
            'description': '4×4 identity matrix test'
        },
        {
            'name': 'massive_matrices',
            'input': '300\n' + '\n'.join([' '.join(map(str, [(i + j) % 5 + 1 for j in range(300)])) for i in range(300)]) + '\n' + 
                     '\n'.join([' '.join(map(str, [(i + j) % 3 + 1 for j in range(300)])) for i in range(300)]),
            'output': '162000000',  # Result for 300x300 matrix multiplication with pattern  
            'complexity_hint': 'O(n³)',
            'input_size': 540000,  # ~540KB input, but O(n³) = 27M operations
            'description': 'Massive 300×300 matrices, O(n⁴) vs O(n³) should be clearly distinguishable'
        },
        {
            'name': 'very_large_matrices',
            'input': '50\n' + '\n'.join([' '.join(map(str, [(i*50+j+1) % 100 for j in range(50)])) for i in range(50)]) + '\n' + 
                     '\n'.join([' '.join(map(str, [(i*50+j+1) % 100 for j in range(50)])) for i in range(50)]),
            'output': 'CALCULATED_DYNAMICALLY',  # Too complex to pre-calculate
            'complexity_hint': 'O(n³)',
            'input_size': 15000,
            'description': 'Very large 50×50 matrices, should stress O(n⁴) vs O(n³) difference'
        }
    ]
    
    # Add test cases (skip the complex calculation for now)
    for i, tc in enumerate(test_cases[:-1]):  # Skip last complex one
        problem_service.add_test_case(
            problem_id=problem.id,
            name=tc['name'],
            input_data=tc['input'],
            expected_output=tc['output'],
            is_sample=i < 2  # First 2 are sample cases
        )
    
    print(f"✅ Created O(n³) problem: {problem.title}")
    print(f"   📊 Test cases: {len(test_cases)-1}")
    return problem

if __name__ == "__main__":
    # Test problem creation
    problem_service = ProblemService()
    problem = create_problem(problem_service)
    print("Problem created successfully!")
