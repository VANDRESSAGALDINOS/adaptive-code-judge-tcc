import sys

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    
    n = int(next(it))
    q = int(next(it))
    
    next_planet = [0] * (n + 1)
    for i in range(1, n + 1):
        next_planet[i] = int(next(it))
    
    # SUBOPTIMAL: naive O(q*k) simulation instead of O(q*log k) binary lifting.
    # Walks the k teleporters one by one; for large k (up to 10^9) this is far
    # slower than the optimal, while computing the same answer.
    results = []
    for _ in range(q):
        x = int(next(it))
        k = int(next(it))
        for _step in range(k):
            x = next_planet[x]
        results.append(str(x))
    
    print('\n'.join(results))

if __name__ == "__main__":
    main()
