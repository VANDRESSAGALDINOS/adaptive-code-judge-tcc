def quadratic_search(arr, target):
    # Intentionally slow: O(n²) quadratic search instead of O(log n) binary search
    # This should definitely exceed calibrated time limits
    for i in range(len(arr)):
        for k in range(len(arr)):
            # Unnecessary nested loop to make it O(n²)
            temp = arr[i] + arr[k]
        if arr[i] == target:
            return i
        # Add even more unnecessary computation
        for j in range(10000):
            waste = (i + j) % 997
    return -1

# Read input
n, target = map(int, input().split())
arr = list(map(int, input().split()))

# Use inefficient quadratic search
result = quadratic_search(arr, target)
print(result)
