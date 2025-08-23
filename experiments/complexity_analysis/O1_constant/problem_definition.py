"""
O(1) Constant Time Complexity Problem Definition
Simple arithmetic operations with constant execution time
"""

def create_problem(problem_service):
    """Create O(1) constant time problem using MVP services"""
    
    # Create the problem
    problem = problem_service.create_problem(
        title="Arithmetic Operations (O(1))",
        description="""
        Perform basic arithmetic operations on two integers.
        
        This problem tests constant-time operations that should show minimal
        difference between C++ and Python performance.
        
        Input: Two integers a and b on a single line
        Output: Four lines containing:
        - Sum: a + b
        - Difference: a - b  
        - Product: a * b
        - Integer Division: a // b (if b != 0, otherwise 0)
        """,
        max_input_size=100,  # Very small input
        time_limit_base=0.1,  # 100ms base limit
        memory_limit=64,  # 64MB
        difficulty='easy',
        tags=['arithmetic', 'O(1)', 'constant-time']
    )
    
    # Test cases with varying input sizes but same complexity
    test_cases = [
        {
            'name': 'small_numbers',
            'input': '5 3',
            'output': '8\n2\n15\n1',
            'complexity_hint': 'O(1)',
            'input_size': 10
        },
        {
            'name': 'medium_numbers', 
            'input': '42 7',
            'output': '49\n35\n294\n6',
            'complexity_hint': 'O(1)',
            'input_size': 15
        },
        {
            'name': 'large_numbers',
            'input': '1000000 999999',
            'output': '1999999\n1\n999999000000\n1',
            'complexity_hint': 'O(1)',
            'input_size': 20
        },
        {
            'name': 'division_by_zero',
            'input': '10 0',
            'output': '10\n10\n0\n0',
            'complexity_hint': 'O(1)',
            'input_size': 10
        },
        {
            'name': 'negative_numbers',
            'input': '-15 -3',
            'output': '-18\n-12\n45\n5',
            'complexity_hint': 'O(1)',
            'input_size': 15
        }
    ]
    
    # Add test cases
    for i, tc in enumerate(test_cases):
        problem_service.add_test_case(
            problem_id=problem.id,
            name=tc['name'],
            input_data=tc['input'],
            expected_output=tc['output'],
            complexity_hint=tc['complexity_hint'],
            input_size=tc['input_size'],
            is_sample=(i == 0),  # First test case is sample
            is_hidden=(i != 0),  # Others are hidden
            weight=1.0
        )
    
    return problem
