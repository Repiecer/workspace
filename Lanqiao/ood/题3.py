ls = list(map(int, input().split()))

a: int = round((ls[2]-ls[2]%ls[0])/ls[0])
b: int = round((ls[3]-ls[3]%ls[1])/ls[1])
c: int = min(a, b)
print(c, end='')
