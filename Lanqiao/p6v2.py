mal = []
n = int(input())
for _ in range(n):
    mal.append(list(map(int, input().split())))

masl = 0
saved = [[0]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        temp = 0
        for k in mal[:i+1]:
            temp+=sum(k[:j+1])
        saved[i][j]=temp
def cal(x, y, a, b):
    if x == 0 and y == 0:
        return saved[a][b]
    elif x != 0 and y == 0:
        return saved[x+a][b] - saved[x-1][b]
    elif x == 0 and y != 0:
        return saved[a][y+b] - saved[a][y-1]
    else:
        return saved[x+a][y+b] - saved[x-1][b] - saved[a][y-1] + saved[x-1][y-1]
    
for i in range(n):
    for j in range(n):
        for k in range(n-i):
            for l in range(n-j):
                masl = max(masl, cal(i, j, k, l))
print(masl)



