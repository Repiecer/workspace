ls: list = []
for _ in range(int(input())):
    ls.append(list(map(int, input().split())))
for _ in ls:
    print(_[0]+_[1])