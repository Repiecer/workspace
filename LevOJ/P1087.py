ls: list = []
while True:
    solin: str = input()
    if not int(solin.split()[0]):
        break
    ls.append(list(map(int, solin.split()))[1:])
for _ in ls:
    print(sum(_))