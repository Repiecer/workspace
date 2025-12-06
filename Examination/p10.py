import sys
input=sys.stdin.readline
n=int(input())
p=[i for i in range(n+1)]
def find(x):
    if x!=p[x]:
        p[x]=find(p[x])
    return p[x]
def union(x,y):
    x_root=find(x)
    y_root=find(y)
    if x_root!=y_root:
        p[y_root]=x_root
k=[]
for i in range(n):
    k.append(int(input()))
    union(i+1,k[i])

s=set()
for i in range(1,n+1):
    s.add(find(i))
print(len(s))