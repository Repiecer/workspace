full: list = []
while True:
    try:
        ls = list(map(int, input().split()))
        ls.sort()
        if ls == []:
            break
        full.append(ls)
    except EOFError:
        break
for i in full:
    if i[0]**2 + i[1]**2 == i[2]**2:
        print("yes")
    else:
        print("no")