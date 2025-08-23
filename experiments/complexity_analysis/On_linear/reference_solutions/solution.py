def array_sum(arr):
    """O(n) linear time: visit each element exactly once"""
    total = 0
    for num in arr:
        total += num
    return total

# Read input
n = int(input())
arr = list(map(int, input().split()))

# Calculate sum using optimal O(n) approach
result = array_sum(arr)
print(result)
