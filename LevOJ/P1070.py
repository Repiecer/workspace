ls: list = []
num :int = int(input())
xor: int = int(input())
for _ in range(num):
    ls.append(int(input()))
print('\n'.join(map(str, ls[xor:]+ls[:xor])))