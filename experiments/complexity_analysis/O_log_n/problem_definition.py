"""
O(log n) Logarithmic Time Complexity Problem Definition
Binary search implementation with logarithmic complexity
"""

def create_problem(problem_service):
    """Create O(log n) logarithmic time problem using MVP services"""
    
    # Create the problem
    problem = problem_service.create_problem(
        title="Binary Search (O(log n))",
        description="""
        Find the position of a target element in a sorted array using binary search.
        
        This problem tests logarithmic-time operations that may show some
        difference between C++ and Python due to recursion and function call overhead.
        
        Input: 
        - First line: n (array size) and target (value to find)
        - Second line: n sorted integers
        
        Output: 
        - Index of target element (0-based), or -1 if not found
        """,
        max_input_size=10000,  # Moderate input
        time_limit_base=0.5,  # 500ms base limit
        memory_limit=128,  # 128MB
        difficulty='medium',
        tags=['binary-search', 'O(log n)', 'logarithmic', 'divide-conquer']
    )
    
    # Test cases with increasing array sizes
    test_cases = [
        {
            'name': 'small_array',
            'input': '5 3\n1 2 3 4 5',
            'output': '2',
            'complexity_hint': 'O(log n)',
            'input_size': 50,
            'description': 'Small array (n=5)'
        },
        {
            'name': 'medium_array',
            'input': '10 7\n1 3 5 7 9 11 13 15 17 19',
            'output': '3', 
            'complexity_hint': 'O(log n)',
            'input_size': 100,
            'description': 'Medium array (n=10)'
        },
        {
            'name': 'large_array_found',
            'input': f'100 50\n{" ".join(map(str, range(1, 101, 1)))}',
            'output': '49',
            'complexity_hint': 'O(log n)',
            'input_size': 1000,
            'description': 'Large array (n=100), element found'
        },
        {
            'name': 'large_array_not_found',
            'input': f'100 150\n{" ".join(map(str, range(1, 101, 1)))}',
            'output': '-1',
            'complexity_hint': 'O(log n)',
            'input_size': 1000,
            'description': 'Large array (n=100), element not found'
        },
        {
            'name': 'very_large_array',
            'input': f'5000 2500\n{" ".join(map(str, range(1, 5001, 1)))}',
            'output': '2499',
            'complexity_hint': 'O(log n)',
            'input_size': 50000,
            'description': 'Very large array (n=5000), should stress O(n²) vs O(log n) difference'
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
