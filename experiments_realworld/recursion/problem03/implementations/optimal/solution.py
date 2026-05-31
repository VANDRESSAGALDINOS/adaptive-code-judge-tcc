import sys
sys.setrecursionlimit(300000)

# RECURSIVE DFS rerooting (deep recursion). For each node, the MAXIMUM distance
# to any other node. Two recursive passes:
#   dfs_down: for each u, down1[u] = longest downward path, down2[u] = second
#             longest downward path (through a DIFFERENT child) -- needed for the
#             reroot.
#   dfs_up:   up[u] = longest path going through the parent; for a child c it is
#             1 + max(up[u], down-of-u-excluding-c). ans[u] = max(down1[u], up[u]).
# Genuine recursive tree rerooting; recursion depth up to n = 2*10^5 (chain).

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

    down1 = [0] * (n + 1)   # longest downward path from u
    down2 = [0] * (n + 1)   # second longest downward path (different child)
    arg1 = [0] * (n + 1)    # child giving down1 (to exclude it for that child)
    up = [0] * (n + 1)      # longest path going upward through the parent

    def dfs_down(u, parent):
        for v in adj[u]:
            if v != parent:
                dfs_down(v, u)
                cand = down1[v] + 1
                if cand > down1[u]:
                    down2[u] = down1[u]
                    down1[u] = cand
                    arg1[u] = v
                elif cand > down2[u]:
                    down2[u] = cand

    def dfs_up(u, parent):
        for v in adj[u]:
            if v != parent:
                # best downward of u excluding the branch through v
                best_excl = down2[u] if arg1[u] == v else down1[u]
                up[v] = max(up[u], best_excl) + 1
                dfs_up(v, u)

    dfs_down(1, 0)
    dfs_up(1, 0)

    out = []
    for i in range(1, n + 1):
        out.append(str(max(down1[i], up[i])))
    sys.stdout.write(" ".join(out) + "\n")

if __name__ == "__main__":
    main()
