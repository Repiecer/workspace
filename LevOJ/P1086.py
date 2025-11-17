
ls: list = []
while True:
    solin: str = input()
    if solin.split()==['0','0']:
        break
    ls.append(list(map(int, solin.split())))
for _ in ls:
    print(sum(_))