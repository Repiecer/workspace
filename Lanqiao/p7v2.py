t, m = list(map(int, input().split()))
ws = []
val = []
for _ in range(m):
    w, v = list(map(int, input().split()))
    ws.append(w)
    val.append(v)


dp = [0]*(t+1)

for i in range(m):
    for j in range(t, ws[i]-1, -1):
        dp[i] = max(dp[i], dp[i-ws[i]]+val[i])


print(dp[t])





