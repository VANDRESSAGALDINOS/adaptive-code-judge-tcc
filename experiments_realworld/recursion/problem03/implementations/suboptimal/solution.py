import sys
sys.setrecursionlimit(300000)

# SUBOPTIMAL: naive O(n^2) instead of the O(n) rerooting. For EACH node we run a
# separate recursive DFS that returns the maximum distance from that node to any
# other node. Same recursive DFS shape and the same answer as the optimal, but
# without the rerooting trick -> O(n^2) total (n independent DFS traversals).
# Genuine algorithmic inefficiency (worse complexity, not a fake slowdown).
# Selectivity check: a correct-but-too-slow submission that must be REJECTED even
# under the adaptive limit.

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    adj = [[] for _ in range(n + 1)]
    idx = 1
    for _ in range(n - 1):
        a = int(data[idx]); b = int(data[idx + 1]); idx += 2
        adj[a].append(b)
        adj[b].append(a)

    if n == 1:
        print(0)
        return

    # max distance reachable downward from u (away from parent)
    def dfs(u, parent, d):
        best = d
        for v in adj[u]:
            if v != parent:
                cand = dfs(v, u, d + 1)
                if cand > best:
                    best = cand
        return best

    out = []
    for s in range(1, n + 1):
        out.append(str(dfs(s, 0, 0)))

    sys.stdout.write(" ".join(out) + "\n")

if __name__ == "__main__":
    main()
