import sys

sys.setrecursionlimit(1e8)
n = int(input())
happ = list(map(int, sys.stdin.readline().split()))
dp = [[0, 0] for _ in range(n+1)]

E = [[] for _ in range(n+1)]
fathered = [False]*(n+1)
for i in range(1, n+1):
    u, v = list(map(int, sys.stdin.readline().split()))
    E[u].append(v)
    E[v].append(u)


def dfs(u, parent):
    dp[u][1] = happ[u]
    dp[u][0] = 0
    for v in E[u]:
        if v == parent:
            continue
        dfs(v, u)
        dp[u][1] += dp[v][0]
        dp[u][0] += max(dp[v][0], dp[v][1])
dfs(1, -1)
print(max(dp[1][0], dp[1][1]))



