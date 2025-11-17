n, m, t = list(map(int, input().split()))
orders = []
ranks = [0]*n
for _ in range(m):
    orders.append(list(map(int, input().split())))
upon = []
for i in range(1, t+1):
    added = []
    for j in range(m):
        if orders[j][0] == i:
            added.append(orders[j][1])
            ranks[orders[j][1]-1] += 2
    for k in range(n):
        if k+1 not in added:
            ranks[k]-=1
    for l in range(n):
        if ranks[l] < 0:
            ranks[l] = 0
    for t in range(n):
        if ranks[t] > 5:
            if t+1 not in upon:
                upon.append(t+1)
        if ranks[t] <= 3:
            if t+1 in upon:
                upon.remove(t+1)

print(len(upon))

