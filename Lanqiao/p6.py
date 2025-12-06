mal = []
n = int(input())
for _ in range(n):
    mal.append(list(map(int, input().split())))

masl = 0
def cal(x, y, a, b):
    temp = 0
    for le in mal[x:x+a]:
        for val in le[y:y+b]:
            temp+=val
    return temp

for i in range(n):
    for j in range(n):
        for k in range(n-i):
            for l in range(n-j):
                masl = max(masl, cal(i, j, k+1, l+1))
print(masl)



