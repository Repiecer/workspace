ans: int = 0
def dfs(depth, m, n):
    global ans
    if depth == 7:
        if m == 0 and n == 0:
            ans += 1
        return
    for i in range(m+1):
        for j in range(n+1):
            if 2 <= i + j <= 5 and i <= m and j <= n:
                dfs(depth+1, m-i, n-j)
dfs(0, 9, 16)
print(ans)