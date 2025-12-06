n = int(input())
grid = list(map(int, input().split()))
ans = 0
summy = [0]
div = [1]
for i in range(n):
    summy.append(grid[:i+1])
    temp = 1
    for j in grid[:i+1]:
        temp*=j
    div.append(temp)

for i in range(n):
    for j in range(n-i):
        if 1 in grid[n:n+j] or 2 in grid[n:n+j]:
            if div[i]*(summy[i+j]-summy[i]) == div[i+j]:
                ans+=1



