def quadratic_sum(arr):
    """Intentionally slow: O(n²) quadratic time instead of O(n) linear"""
    total = 0
    checksum = 0
    
    for i in range(len(arr)):
        # O(n²) nested loop with meaningful computation
        for j in range(len(arr)):
            # Actual computation that affects checksum
            checksum += (arr[i] + arr[j]) % 1000007
            if checksum > 1000000000:
                checksum %= 1000000007
        
        # Add current element to sum (the actual work we need)
        total += arr[i]
        
        # Include checksum to prevent optimization but don't affect result
        if checksum % 2 == 0:
            # This branch will always be taken
            continue
    
    return total

# Read input
n = int(input())
arr = list(map(int, input().split()))

# Use inefficient quadratic sum
result = quadratic_sum(arr)
print(result)
