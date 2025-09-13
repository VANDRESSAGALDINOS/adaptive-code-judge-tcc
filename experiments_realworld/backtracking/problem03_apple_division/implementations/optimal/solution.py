import sys
sys.setrecursionlimit(10000)

def solve():
    n = int(input())
    weights = list(map(int, input().split()))
    total_sum = sum(weights)
    
    ans = [float('inf')]
    
    def backtrack(idx, sum1):
        if idx == n:
            sum2 = total_sum - sum1
            ans[0] = min(ans[0], abs(sum1 - sum2))
            return
        
        backtrack(idx + 1, sum1 + weights[idx])
        backtrack(idx + 1, sum1)
    
    backtrack(0, 0)
    print(ans[0])

if __name__ == "__main__":
    solve()
