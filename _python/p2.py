sum_n = int(10e7+1)

n, k = list(map(int, input().split()))
arr = list(map(int, input().split()))
def dfs(loc, atl):
    global sum_n
    if loc >= n:
        return
    atl += arr[loc]
    if loc == n-1:
        sum_n = min(sum_n, atl)
    for i in range(k+1):
        dfs(loc+i+1, atl)

dfs(0, 0)
print(sum_n)
