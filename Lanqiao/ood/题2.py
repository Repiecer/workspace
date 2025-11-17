num: int = input()
ls: list = list(map(int, input().split()))
summary: int = 0
for i in ls:
    if i-1 not in ls:
        summary+=i
print(summary)