import sys
sys.setrecursionlimit(300000)

# RECURSIVE DFS rerooting (deep recursion). For each node, the sum of distances
# to all other nodes, via two recursive passes:
#   DFS1 (post-order): subtree size cnt[u] and res[1] = sum of depths from root.
#   DFS2 (pre-order):  reroot, res[v] = res[u] + (n - cnt[v]) - cnt[v].
# More per-node arithmetic than a plain diameter DFS. The tree may degenerate
# into a chain -> recursion depth up to n = 2*10^5. Python pays the per-call
# interpreter overhead AND a smaller stack limit than C++; the verdict here is
# either TLE (time) or RUNTIME ERROR (stack). This run confirms which appears.

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

    cnt = [1] * (n + 1)   # subtree sizes
    res = [0] * (n + 1)   # answer per node

    # DFS1: post-order — subtree sizes and sum of depths from root (into res[1]).
    def dfs1(u, parent, depth):
        res[1] += depth
        for v in adj[u]:
            if v != parent:
                dfs1(v, u, depth + 1)
                cnt[u] += cnt[v]

    # DFS2: pre-order — reroot from u to each child v.
    def dfs2(u, parent):
        for v in adj[u]:
            if v != parent:
                res[v] = res[u] + (n - cnt[v]) - cnt[v]
                dfs2(v, u)

    dfs1(1, 0, 0)
    dfs2(1, 0)

    sys.stdout.write(" ".join(str(res[i]) for i in range(1, n + 1)) + "\n")

if __name__ == "__main__":
    main()
