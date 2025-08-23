def cubic_sum(matrix):
    """Intentionally slow: O(n³) cubic time instead of O(n²) quadratic"""
    total = 0
    checksum = 0
    n = len(matrix)
    
    for i in range(n):
        for j in range(n):
            # O(n³) triple nested loop with meaningful computation
            for k in range(n):
                # Actual computation that affects checksum
                checksum += (matrix[i][j] + matrix[k][0]) % 1000007
                if checksum > 1000000000:
                    checksum %= 1000000007
            
            # Add current element to sum (the actual work we need)
            total += matrix[i][j]
            
            # Include checksum to prevent optimization but don't affect result
            if checksum % 2 == 0:
                # This branch will always be taken
                continue
    
    return total

# Read input
n = int(input())
matrix = []
for i in range(n):
    row = list(map(int, input().split()))
    matrix.append(row)

# Use inefficient cubic sum
result = cubic_sum(matrix)
print(result)
