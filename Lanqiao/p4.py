n, m = list(map(int, input().split()))
pl = list(map(int, input().split()))
cl = []
for _ in range(n-1):
    cl.append(list(map(int, input().split())))

rl = [0]*(n-1)
for i in range(m-1):
    for j in range(min(pl[i], pl[i+1]), max(pl[i], pl[i+1])):
        rl[j-1]+=1
ss = 0
for k in range(n-1):
    if rl[k]==0:
        continue
    pc = cl[k][0]*rl[k]
    cc = cl[k][2]+cl[k][1]*rl[k]
    if pc <= cc:
        ss+=pc
    else:
        ss+=cc
print(ss)
        
