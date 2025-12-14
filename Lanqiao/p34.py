n, m = list(map(int, input().split()))

ls = [i for i in range(n)]
def find(x):
    while ls[x] != x:
        x = ls[x]
    return x
def union(x, y):
    x_root = find(x)
    y_root = find(y)
    if ls[x_root] != ls[y_root]:
        ls[x_root] = y_root


    