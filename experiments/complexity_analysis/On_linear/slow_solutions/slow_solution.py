def inefficient_sum(arr):
    """Algorithmically equivalent but inefficient: O(n²) using nested summation"""
    # Each element is added len(arr) times, then divided by n
    total = 0
    n = len(arr)
    
    for i in range(n):
        element_contribution = 0
        # Add current element n times (inefficient)
        for j in range(n):
            element_contribution += arr[i]
        # Divide by n to get back original value
        total += element_contribution // n
    
    return total

# Read input
n = int(input())
arr = list(map(int, input().split()))

# Calculate sum using inefficient approach
result = inefficient_sum(arr)
print(result)
