def matrix_sum(matrix):
    """O(n²) quadratic time: visit each element exactly once"""
    total = 0
    n = len(matrix)
    
    for i in range(n):
        for j in range(n):
            total += matrix[i][j]
    
    return total

# Read input
n = int(input())
matrix = []
for i in range(n):
    row = list(map(int, input().split()))
    matrix.append(row)

# Calculate sum using optimal O(n²) approach
result = matrix_sum(matrix)
print(result)
