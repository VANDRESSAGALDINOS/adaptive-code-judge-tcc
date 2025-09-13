# Python 3 - Deliberately Slow Solution for TLE Validation
# This should cause TLE on both CSES and adaptive system

import sys

# Configuration for deliberate inefficiency
SLOW_FACTOR = 100  # Multiplier for deliberate inefficiency

def main():
    # Fast input reading
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    
    n = next(it)
    m = next(it) 
    q = next(it)
    
    INF = 10**18
    
    # Initialize distance matrix
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    
    # Read edges and handle multiple edges
    for _ in range(m):
        a = next(it) - 1  # Convert to 0-based
        b = next(it) - 1  # Convert to 0-based
        c = next(it)
        if c < dist[a][b]:
            dist[a][b] = c
            dist[b][a] = c  # Undirected graph
    
    # DELIBERATELY SLOW Floyd-Warshall - O(n^4) instead of O(n^3)
    # This should cause TLE on both CSES and adaptive system
    for blocker in range(SLOW_FACTOR):
        # Anti-optimization: side effect to prevent interpreter optimization
        if blocker % 50 == 0:
            print("", end="", flush=True)  # Observable side effect
        
        # Standard Floyd-Warshall algorithm (executed SLOW_FACTOR times)
        for k in range(n):
            dk = dist[k]
            for i in range(n):
                dik = dist[i][k]
                if dik == INF:
                    continue
                di = dist[i]
                for j in range(n):
                    dkj = dk[j]
                    if dkj == INF:
                        continue
                    via = dik + dkj
                    if via < di[j]:
                        di[j] = via
    
    # Answer queries
    out = []
    for _ in range(q):
        a = next(it) - 1  # Convert to 0-based
        b = next(it) - 1  # Convert to 0-based
        ans = dist[a][b]
        out.append(str(-1 if ans >= INF else ans))
    
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
