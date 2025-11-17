import sys

n = int(input())
r, c = [*map(int, input().split())], [*map(int, input().split())]

path = []
vis = [[False] * n for _ in range(n)]


def check():
    return all(x == 0 for x in r) and all(x == 0 for x in c)

def dfs(i, j):
    if r[j] - 1 < 0 or c[i] - 1 < 0:
        return 
    vis[i][j] = True
    r[j] -= 1
    c[i] -= 1
    path.append(str(i * n + j))
    if i == n - 1 and j == n - 1 and check():
        print(' '.join(path))
        sys.exit(0)
    for dx, dy in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
        nx, ny = dx + i, dy + j
        if 0 <= nx < n and 0 <= ny < n and not vis[nx][ny]:
            dfs(nx, ny)
    path.pop()
    r[j] += 1
    c[i] += 1
    vis[i][j] = False

dfs(0, 0)