ls: list = []
for _ in range(int(input())):
    ls.append(list(map(int, input().split())))
for i in ls:
    print(i[0]//i[1], i[0]%i[1])