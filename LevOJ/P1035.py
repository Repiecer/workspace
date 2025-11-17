ls = list(map(int, input().split()))
x = (2*ls[0])-(ls[1]/2)
y = ls[0]-x
if (x >= 0) and (y >= 0) and (y == int(y)):
    print(int(x), int(y))
else:
    print(-1, -1)