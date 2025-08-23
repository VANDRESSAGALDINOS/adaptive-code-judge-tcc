def quartic_multiply(A, B):
    """Intentionally slow: O(n⁴) quartic time instead of O(n³) cubic"""
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    debug_counter = 0
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                # O(n⁴) extra nested loop with meaningful computation
                for l in range(n):
                    debug_counter += 1
                    # Side effect that prevents optimization
                    if debug_counter % 50000 == 0:
                        print(f"DEBUG: processed {debug_counter} operations")
                
                # Do the actual matrix multiplication work
                C[i][j] += A[i][k] * B[k][j]
    
    # Final debug info
    print(f"TOTAL_OPS: {debug_counter}")
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

# Use inefficient quartic multiplication
C = quartic_multiply(A, B)

# Calculate sum of all elements in result matrix
matrix_sum = sum(sum(row) for row in C)

# Output sum
print(matrix_sum)
