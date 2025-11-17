ls: list = []
for _ in range(7):
    ls.append(sum(map(int, input().split())))
print(ls.index(max(ls))+1)