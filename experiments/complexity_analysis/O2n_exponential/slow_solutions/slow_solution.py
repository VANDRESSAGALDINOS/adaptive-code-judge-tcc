import sys

# Increase recursion limit for deep exponential recursion
sys.setrecursionlimit(50000)

def inefficient_subset_sum(arr, target, index=0):
    """Algorithmically equivalent but inefficient: O(3ⁿ) using redundant recursive calls"""
    # Each decision point explores three paths: include, exclude, and duplicate exclude
    
    # Base cases
    if target == 0:
        return True  # Found exact sum
    if index >= len(arr):
        return False  # No more elements
    
    # Three recursive calls: include, exclude, and redundant exclude
    # The redundant call computes the same result as exclude but forces O(3ⁿ) complexity
    include = inefficient_subset_sum(arr, target - arr[index], index + 1)
    exclude = inefficient_subset_sum(arr, target, index + 1)
    redundant_exclude = inefficient_subset_sum(arr, target, index + 1)  # Identical to exclude
    
    # Mathematical equivalence: (A or B or B) = (A or B)
    return include or exclude or redundant_exclude

# Read input
n = int(input())
arr = list(map(int, input().split()))
target = int(input())

# Find subset using inefficient approach
result = inefficient_subset_sum(arr, target)

print("YES" if result else "NO")
