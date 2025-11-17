ls: list = []
temp1: list = []
for _ in range(int(input())):
    ls.append(list(map(int, input().split())))
for i in range(len(ls)):
    temp1.append(ls[i][i])
for i in range(len(ls)):
    temp1.append(ls[i][len(ls)-1-i])
print(max(temp1), min(temp1))
