import sys
sys.setrecursionlimit(300000)

# SUBOPTIMAL: the SAME recursive DFS as the optimal, but WITHOUT small-to-large.
# It always merges the CHILD's set into the PARENT's set (never swapping the
# smaller into the larger). Same answer as the optimal, but the merge work is no
# longer bounded: on a chain (each node a distinct color) the accumulated set is
# carried up and re-copied at every level -> O(n^2) in the worst case, vs the
# optimal's O(n log n). Genuine algorithmic inefficiency (worse complexity, not a
# fake slowdown). Selectivity check: a correct-but-too-slow submission that must
# be REJECTED even under the adaptive limit.

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    color = [0] * (n + 1)
    for i in range(1, n + 1):
        color[i] = int(data[i])
    adj = [[] for _ in range(n + 1)]
    idx = n + 1
    for _ in range(n - 1):
        a = int(data[idx]); b = int(data[idx + 1]); idx += 2
        adj[a].append(b)
        adj[b].append(a)

    ans = [0] * (n + 1)

    def dfs(u, parent):
        s = {color[u]}
        for v in adj[u]:
            if v != parent:
                cs = dfs(v, u)
                # NAIVE merge: always child-into-parent, NO small-to-large.
                s.update(cs)
        ans[u] = len(s)
        return s

    dfs(1, 0)

    sys.stdout.write(" ".join(str(ans[i]) for i in range(1, n + 1)) + "\n")

if __name__ == "__main__":
    main()
