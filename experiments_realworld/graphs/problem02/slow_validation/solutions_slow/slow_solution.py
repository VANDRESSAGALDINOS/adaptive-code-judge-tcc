# Python Slow Solution - CSES 1197: Cycle Finding
# Deliberately inefficient version for TLE validation
# Based on provided TLE code with artificial slowdown

import sys

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    # Flat list of edges for multiple traversals
    edges = [None] * m
    for i in range(m):
        a = int(next(it))
        b = int(next(it)) 
        w = int(next(it))
        edges[i] = (a, b, w)

    dist = [0] * (n + 1)      # Implicit super-source
    parent = [-1] * (n + 1)

    x = -1

    # Slowdown factor: each real iteration followed by EXTRA_PASSES useless sweeps
    EXTRA_PASSES = 150  # Increased for stronger TLE

    # Waste variable prevents Python from optimizing away work
    waste = 0

    # Complete Bellman-Ford WITHOUT early-stop
    for _ in range(n):
        x = -1

        # 1) Real relaxation pass
        for a, b, w in edges:
            nb = dist[a] + w
            if nb < dist[b]:
                dist[b] = nb
                parent[b] = a
                x = b

        # 2) Extra work to consume time (doesn't alter useful state)
        for _rep in range(EXTRA_PASSES):
            acc = 0
            for a, b, w in edges:
                # Integer arithmetic plus memory accesses to prevent dead-code
                acc ^= (a * 1315423911) ^ (b * 2654435761) ^ (w & 0xFFFF)
                acc ^= (dist[a] & 0xFF) ^ (dist[b] & 0x7F)
                # Touch parent to force memory accesses
                pa = parent[a] if parent[a] != -1 else 0
                pb = parent[b] if parent[b] != -1 else 0
                acc ^= (pa + 3 * pb) & 0xFFFF
            waste ^= acc  # Accumulate to prevent elimination

    # Final decision
    if x == -1:
        # Optional: small cooldown to ensure TLE on very large NO instances
        for _ in range(EXTRA_PASSES):
            for a, b, w in edges:
                waste ^= (a + b + (w & 255))
        print("NO")
        return

    # If update occurred in nth iteration, negative cycle exists
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
            cycle.append(v)  # Close cycle
            break
    cycle.reverse()

    print("YES")
    print(*cycle)

if __name__ == "__main__":
    main()

# Reference: https://cses.fi/paste/20ed388184c517b5db2332/
