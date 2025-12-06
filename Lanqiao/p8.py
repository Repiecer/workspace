a, b = input(), input()
def toint(p):
    q = []
    if len(p)%3 != 0:
        q.append(p[:len(p)%3])
        p = p[len(p)%3:]
    for _ in range(len(p)//3):
        q.append(p[:3])
        p = p[3:]
    return list(map(int, q))
al = toint(a)
bl = toint(b)
m, n = len(al), len(bl)
if len(al) >= len(bl):

    al = [0]+al
    bl = [0]*(m-n+1) + bl

else:
    bl = [0]+bl
    al = [0]*(n-m+1) + al
print(len(al), len(bl))
for i in range(len(al)):
    bl[i]+=al[i]

bl = list(map(str, bl))[::-1]

for j in range(len(bl)-1):
    if len(bl[j]) > 3:
        bl[j+1] = str(int(bl[j+1])+int(bl[j][:len(bl[j])%3]))


print(''.join(bl[::-1]).lstrip('0') or '0')


