n = input()
x_point = list(map(int, input().split()))
y_point = list(map(int, input().split()))
visited = []
steps = [(0, 1), (1, 0), (-1, 0), (0, -1)]
routine = sum(x_point)
def dfs(depth, x, y):
    visited.append((x, y))
    if depth >= routine:
        return
    for step in steps:
        position = (x+step[0], y+step[1])
        if 0<=position[0]<=n-1 and 0<=position[1]<=n-1:
            if position not in visited:
                dfs(depth+1, *position)

