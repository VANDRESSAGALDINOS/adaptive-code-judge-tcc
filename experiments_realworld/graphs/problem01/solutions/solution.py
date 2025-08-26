# Python Reference Solution - CSES 1672: Shortest Routes II
# Algorithmically equivalent to C++ solution (see formal_proof.md)
# Floyd-Warshall All-Pairs Shortest Path - O(n³)
# Recommended to run on PyPy for performance margin

import sys

data = list(map(int, sys.stdin.buffer.read().split()))
it = iter(data)
n = next(it); m = next(it); q = next(it)

INF = 10**18
dist = [[INF]*n for _ in range(n)]
for i in range(n):
    dist[i][i] = 0

# edges: keep the smallest among multiple
for _ in range(m):
    a = next(it) - 1
    b = next(it) - 1
    c = next(it)
    if c < dist[a][b]:
        dist[a][b] = c
        dist[b][a] = c

# Floyd–Warshall with INF check to avoid overflow
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

# answer queries
out = []
for _ in range(q):
    a = next(it) - 1
    b = next(it) - 1
    ans = dist[a][b]
    out.append(str(-1 if ans >= INF else ans))
sys.stdout.write("\n".join(out))
