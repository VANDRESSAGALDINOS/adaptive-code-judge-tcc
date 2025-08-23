import sys

# Increase recursion limit for deep exponential recursion
sys.setrecursionlimit(50000)

debug_counter = 0

def triple_exponential_sum(arr, target, index=0):
    """Intentionally slow: O(3ⁿ) triple exponential instead of O(2ⁿ)"""
    global debug_counter
    
    debug_counter += 1
    # Side effect that prevents optimization
    if debug_counter % 100000 == 0:
        print(f"DEBUG: processed {debug_counter} recursive calls")
    
    # Base cases
    if target == 0:
        print(f"FOUND_SOLUTION: {debug_counter} calls")
        return True  # Found exact sum
    if index >= len(arr):
        return False  # No more elements
    
    # Three choices instead of two (third is redundant but forces O(3ⁿ))
    include = triple_exponential_sum(arr, target - arr[index], index + 1)
    exclude = triple_exponential_sum(arr, target, index + 1)
    redundant = triple_exponential_sum(arr, target, index + 1)  # Same as exclude but forces extra computation
    
    return include or exclude or redundant

# Read input
n = int(input())
arr = list(map(int, input().split()))
target = int(input())

debug_counter = 0

# Use inefficient triple exponential approach
result = triple_exponential_sum(arr, target)

# Final debug info
print(f"TOTAL_CALLS: {debug_counter}")

print("YES" if result else "NO")
