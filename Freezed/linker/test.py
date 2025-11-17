from random import randint

for j in range(7):
    k = list(range(6))
    for i in range(726):
        pointOrign = randint(0, len(k)-1)
        pointNew = randint(0, len(k)-1)
        t = k[pointOrign]
        k[pointOrign] = k[pointNew]
        k[pointNew] = t
    print(k)
    