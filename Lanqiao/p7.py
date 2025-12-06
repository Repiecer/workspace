t, m = list(map(int, input().split()))
ws = []
val = []
for _ in range(m):
    w, v = list(map(int, input().split()))
    ws.append(w)
    val.append(v)


dp = [[0]*(t+1) for _ in range(m+1)]

for i in range(1, m+1):
    for j in range(1, t+1):
        if j >= ws[i-1]:
            dp[i][j] = max(dp[i-1][j], dp[i-1][j-ws[i-1]]+val[i-1])
        else:
            dp[i][j] = dp[i-1][j]


print(dp[m][t])





