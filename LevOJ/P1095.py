ls: list = []
for _ in range(int(input())):
    ls.append(list(map(int, input().split()))[:-1])
for i in ls:
    print(len(i), max(i), min(i), f'{sum(i)/len(i):.1f}',sep='\n')