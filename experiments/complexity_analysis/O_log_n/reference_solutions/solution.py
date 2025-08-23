def binary_search(arr, target):
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # Not found

# Read input
n, target = map(int, input().split())
arr = list(map(int, input().split()))

# Perform binary search
result = binary_search(arr, target)
print(result)
