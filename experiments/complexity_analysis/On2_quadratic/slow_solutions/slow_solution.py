def inefficient_matrix_sum(matrix):
    """Algorithmically equivalent but inefficient: O(n³) using redundant computations"""
    # Each element is accessed n times and averaged, maintaining mathematical equivalence
    total = 0
    n = len(matrix)
    
    for i in range(n):
        for j in range(n):
            element_contribution = 0
            # Access current element n times (inefficient)
            for k in range(n):
                element_contribution += matrix[i][j]
            # Divide by n to get back original value
            total += element_contribution // n
    
    return total

# Read input
n = int(input())
matrix = []
for i in range(n):
    row = list(map(int, input().split()))
    matrix.append(row)

# Calculate sum using inefficient approach
result = inefficient_matrix_sum(matrix)
print(result)
