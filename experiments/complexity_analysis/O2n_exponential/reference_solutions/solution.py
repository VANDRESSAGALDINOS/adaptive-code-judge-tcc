import sys

# Increase recursion limit for deep exponential recursion
sys.setrecursionlimit(50000)

def subset_sum(arr, target, index=0):
    """O(2ⁿ) exponential time: check all possible subsets recursively"""
    
    # Base cases
    if target == 0:
        return True  # Found exact sum
    if index >= len(arr):
        return False  # No more elements
    
    # Two choices: include current element or exclude it
    include = subset_sum(arr, target - arr[index], index + 1)
    exclude = subset_sum(arr, target, index + 1)
    
    return include or exclude

# Read input
n = int(input())
arr = list(map(int, input().split()))
target = int(input())

# Find subset using optimal O(2ⁿ) recursive approach
result = subset_sum(arr, target)

print("YES" if result else "NO")
