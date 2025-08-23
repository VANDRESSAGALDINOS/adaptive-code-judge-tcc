"""
O(2ⁿ) Exponential Time Complexity Problem Definition
Subset Sum - Find if there exists a subset with given sum
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.services.problem_service import ProblemService

def create_problem(problem_service: ProblemService):
    """Create O(2ⁿ) Exponential Time problem: Subset Sum"""
    
    problem = problem_service.create_problem(
        title="Subset Sum (O(2ⁿ))",
        description="""
        Given a set of integers and a target sum, determine if there exists 
        a subset of the given set with sum equal to the target.
        
        This problem tests exponential-time operations where we need to 
        check all possible subsets (2ⁿ combinations).
        
        Input: 
        - First line: n (number of elements)
        - Second line: n integers (the set)
        - Third line: target sum
        
        Output: 
        - "YES" if subset exists, "NO" otherwise
        """,
        max_input_size=1000,  # Small input due to exponential growth
        time_limit_base=5.0,
        memory_limit=256,
        difficulty='expert',
        tags='subset-sum,O(2ⁿ),exponential,dynamic-programming,backtracking'
    )
    
    # Test cases designed to stress exponential vs factorial performance
    test_cases = [
        {
            'name': 'tiny_set',
            'input': '3\n1 2 3\n4',
            'output': 'YES',  # {1, 3} = 4
            'complexity_hint': 'O(2ⁿ)',
            'input_size': 50,
            'description': 'Tiny set (n=3)'
        },
        {
            'name': 'small_set',
            'input': '4\n2 4 6 8\n10',
            'output': 'YES',  # {2, 8} = 10 or {4, 6} = 10
            'complexity_hint': 'O(2ⁿ)',
            'input_size': 100,
            'description': 'Small set (n=4)'
        },
        {
            'name': 'medium_set_yes',
            'input': '6\n1 3 5 7 9 11\n16',
            'output': 'YES',  # {5, 11} = 16 or {1, 3, 5, 7} = 16
            'complexity_hint': 'O(2ⁿ)',
            'input_size': 200,
            'description': 'Medium set with solution (n=6)'
        },
        {
            'name': 'medium_set_no',
            'input': '6\n2 4 6 8 10 12\n25',
            'output': 'NO',  # No subset sums to 25
            'complexity_hint': 'O(2ⁿ)',
            'input_size': 200,
            'description': 'Medium set without solution (n=6)'
        },
        {
            'name': 'large_set',
            'input': '22\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22\n80',
            'output': 'YES',  # Multiple ways to get 80
            'complexity_hint': 'O(2ⁿ)',
            'input_size': 700,
            'description': 'Large set (n=22), O(3ⁿ) = 31B vs O(2ⁿ) = 4M operations - exponential difference!'
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
    
    print(f"✅ Created O(2ⁿ) problem: {problem.title}")
    print(f"   📊 Test cases: {len(test_cases)}")
    return problem

if __name__ == "__main__":
    # Test problem creation
    problem_service = ProblemService()
    problem = create_problem(problem_service)
    print("Problem created successfully!")
