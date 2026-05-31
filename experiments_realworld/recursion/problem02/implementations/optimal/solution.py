import sys
sys.setrecursionlimit(300000)

# RECURSIVE DFS + small-to-large merging. For each node, the number of distinct
# colors in its subtree. The DFS returns a set of the colors in the subtree;
# a parent merges each child's set into its own, always iterating the SMALLER set
# into the LARGER one (small-to-large) -> O(n log n) total. This is heavier
# per-node than a plain O(n) tree DFS (set operations on top of the recursion),
# stressing both the recursive call overhead and the set work in Python.
# Recursion depth up to n = 2*10^5 (chain). setrecursionlimit raised accordingly.

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

    # returns the set of distinct colors in the subtree rooted at u
    def dfs(u, parent):
        s = {color[u]}
        for v in adj[u]:
            if v != parent:
                cs = dfs(v, u)
                # small-to-large: merge the smaller set into the larger
                if len(cs) > len(s):
                    s, cs = cs, s
                s.update(cs)
        ans[u] = len(s)
        return s

    dfs(1, 0)

    sys.stdout.write(" ".join(str(ans[i]) for i in range(1, n + 1)) + "\n")

if __name__ == "__main__":
    main()
