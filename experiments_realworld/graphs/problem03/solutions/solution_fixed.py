import sys

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    
    n = int(next(it))
    q = int(next(it))
    
    next_planet = [0] * (n + 1)
    for i in range(1, n + 1):
        next_planet[i] = int(next(it))
    
    # Binary lifting: up[i][j] = destination after 2^j steps from planet i
    LOG = 30  # log2(10^9) ≈ 30
    up = [[0] * LOG for _ in range(n + 1)]
    
    # Initialize: up[i][0] = next_planet[i] (after 2^0 = 1 step)
    for i in range(1, n + 1):
        up[i][0] = next_planet[i]
    
    # Fill binary lifting table: up[i][j] = up[up[i][j-1]][j-1]
    for j in range(1, LOG):
        for i in range(1, n + 1):
            up[i][j] = up[up[i][j-1]][j-1]
    
    # Process queries
    results = []
    for _ in range(q):
        x = int(next(it))
        k = int(next(it))
        
        # Binary lifting: decompose k into powers of 2
        for j in range(LOG):
            if k & (1 << j):
                x = up[x][j]
        
        results.append(str(x))
    
    print('\n'.join(results))

if __name__ == "__main__":
    main()













