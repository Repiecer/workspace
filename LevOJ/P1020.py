ls: list = list(input().split())

for i in range(len(ls)):
    for j in range(i + 1, len(ls)):
        if len(ls[i]) > len(ls[j]):
            ls[i], ls[j] = ls[j], ls[i]
for i in ls:
    if len(i) == len(ls[-1]):
        print(i)
        break
print(ls[0])