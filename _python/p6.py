import sys
n = int(input())
sys.setrecursionlimit(100000)

arr = [0]+list(map(int, sys.stdin.readline().split()))

E = [[] for _ in range(n+1)]
fathered = [False]*(n+1)

for _ in range(n-1):
    u, v = list(map(int, sys.stdin.readline().split()))
    E[u].append(v)
    E[v].append(u)
    fathered[u] = True

root = 0
for i in range(1, n+1):
    if not fathered[i]:
        root = i
        break

dp = [[0, 0] for _ in range(n+1)]

def dfs(u, parent):
    dp[u][1] = arr[u]
    dp[u][0] = 0

    for v in E[u]:
        if v == parent:
            continue
        dfs(v, u)
        dp[u][1] += dp[v][0]
        dp[u][0] += max(dp[v][1], dp[v][0])

dfs(root, -1)
print(max(dp[root][1], dp[root][0]))

