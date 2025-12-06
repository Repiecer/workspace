N, K = list(map(int, input().split()))

dp = [0]*(N+1)
dp[0] = 1

for i in range(1, N+1):
    for j in range(1, min(i, K)+1):
        dp[i] = (dp[i] + dp[i-j])%10003

print(dp[N])

