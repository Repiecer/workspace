n, m = map(int, input().split())

# 邻接矩阵，1 表示有边，0 表示无边
graph = [[1] * n for _ in range(n)]

# 自己到自己没边
for i in range(n):
    graph[i][i] = 0

# 删除边
for _ in range(m):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    graph[u][v] = 0
    graph[v][u] = 0

# DFS 找连通块
visited = [False] * n
components = []

def dfs(u, comp):
    visited[u] = True
    comp.append(u + 1)  # 转回 1-based
    for v in range(n):
        if graph[u][v] == 1 and not visited[v]:
            dfs(v, comp)

for i in range(n):
    if not visited[i]:
        comp = []
        dfs(i, comp)
        comp.sort()
        components.append(comp)

# 按最小节点升序输出
components.sort(key=lambda x: x[0])

print(len(components))
for comp in components:
    print(len(comp), *comp)