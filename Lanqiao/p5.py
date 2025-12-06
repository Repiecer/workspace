nl = []
for _ in range(int(input())):
    nl.append(int(input()))
    
cl = []

pos = 0
neg = 0

for i in range(1, len(nl)):
    n = nl[i]-nl[i-1]
    if n > 0:
        pos+=n
    else:
        neg-=n

print(max(pos, neg))
print(abs(neg-pos)+1)
        



