def matrix_multiply(A, B):
    """O(n³) cubic time: standard matrix multiplication algorithm"""
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    
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

# Calculate C = A × B using optimal O(n³) approach
C = matrix_multiply(A, B)

# Calculate sum of all elements in result matrix
matrix_sum = sum(sum(row) for row in C)

# Output sum
print(matrix_sum)
