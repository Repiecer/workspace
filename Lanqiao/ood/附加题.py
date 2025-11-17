ls: list = []
def is_group(strlist: list):
    temp: list = []
    for i in strlist:
        if temp.append(i[1]):
            temp.append(i[1])
    minu: int = min(temp)
    group_cost: int = minu*first[1]
    orgin_cost: int = 0
    for i in range(len(strlist)):
        orgin_cost+=strlist[i][0]*minu
    if orgin_cost>group_cost:
        for i in range(len(strlist)):
            if strlist[i][1]:
                strlist[i][1]-=minu
        return orgin_cost>group_cost, strlist, group_cost
    else:
        return False, strlist, group_cost

first: list = list(map(int, input().split()))
for _ in range(first[0]):
    ls.append(list(map(int, input().split())))
sum_cost: int = 0

while True:
    trick = is_group(ls)
    if not trick[0]:
        break
    sum_cost+=trick[2]
    ls = trick[1]

for j in ls:
    sum_cost+=j[0]*j[1]

print(sum_cost)