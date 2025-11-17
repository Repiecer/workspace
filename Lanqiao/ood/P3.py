n = int(input())
cards: list = list(map(int, input().split()))
max_num = len(cards)
scores: list = []
for i in range(max_num):
    temp: int = 0
    exp = cards[:]
    ptr: int = 0
    while True:
        if ptr > len(exp) or len(exp) == 0:
            scores.append(temp)
            break
        if exp[(ptr+i)%len(exp)] == ptr + 1:
            temp += (ptr + 1)
            exp.pop((ptr+i)%len(exp))
        else:
            ptr += 1
print(max(scores) if len(scores)!=0 else 0)
