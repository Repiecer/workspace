ls: list = []
while True:
    solin = input()
    if not solin:
        break
    ls.append(list(map(int, solin.split())))
for i in ls:
    print(i[0]+i[1])