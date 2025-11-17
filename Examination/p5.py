n, sub = list(map(int, input().split()))
weights: list = list(map(int, input().split()))

def dfs(depth):
    if depth == n:
        return
    dfs()
