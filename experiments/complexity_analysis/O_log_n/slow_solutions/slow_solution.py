def linear_search(arr, target):
    # Algorithmically equivalent but inefficient: O(n) linear search
    # Both algorithms solve the search problem, but with different complexities
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1  # Not found

# Read input
n, target = map(int, input().split())
arr = list(map(int, input().split()))

# Perform linear search
result = linear_search(arr, target)
print(result)
