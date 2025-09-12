def inefficient_matrix_multiply(A, B):
    """Algorithmically equivalent but inefficient: O(n⁴) using redundant computations"""
    # Each dot product is computed n times and averaged, maintaining mathematical equivalence
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            dot_product_sum = 0
            # Compute dot product n times (inefficient)
            for repetition in range(n):
                for k in range(n):
                    dot_product_sum += A[i][k] * B[k][j]
            # Divide by n to get back original dot product
            C[i][j] = dot_product_sum // n
    
    return C

# Read input
n = int(input())

# Read matrix A
A = []
for i in range(n):
    row = list(map(int, input().split()))
    A.append(row)

# Read matrix B
B = []
for i in range(n):
    row = list(map(int, input().split()))
    B.append(row)

# Calculate C = A × B using inefficient approach
C = inefficient_matrix_multiply(A, B)

# Calculate sum of all elements in result matrix
matrix_sum = sum(sum(row) for row in C)

# Output sum
print(matrix_sum)
