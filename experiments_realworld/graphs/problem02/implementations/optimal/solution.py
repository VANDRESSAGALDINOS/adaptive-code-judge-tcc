# CSES 1197: Cycle Finding
# Bellman-Ford Negative Cycle Detection - O(nm)

import sys

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    edges = []
    for i in range(m):
        a = int(next(it))
        b = int(next(it))
        w = int(next(it))
        edges.append((a, b, w))

    dist = [0] * (n + 1)          # Implicit super-source
    parent = [-1] * (n + 1)

    x = -1
    
    # Bellman-Ford: n iterations of edge relaxation
    for _ in range(n):
        x = -1
        for a, b, w in edges:
            nb = dist[a] + w
            if nb < dist[b]:
                dist[b] = nb
                parent[b] = a
                x = b

    if x == -1:   
        print("NO")
        return

    # Find node guaranteed to be in negative cycle
    y = x
    for _ in range(n):
        y = parent[y]

    # Reconstruct cycle and print closed form
    cycle = []
    v = y
    while True:
        cycle.append(v)
        v = parent[v]
        if v == y:
            cycle.append(v)  # Close the cycle
            break
    cycle.reverse()

    print("YES")
    print(*cycle)

if __name__ == "__main__":
    main()
