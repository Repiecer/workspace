n, m, k = list(map(int, input().split()))

dp = [[0]*(k+1) for _ in range(n+1)]

dp[0] = [1]*k

for i in range(1, n+1):
    for j in range(1, k+1):
        for l in range(1, m+1):
            if j>= l:
                dp[i][j] += dp[i-1][j-l]
                
                
print(dp[n][k])

