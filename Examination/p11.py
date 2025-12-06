m, n = list(map(int, input().split()))
k = int(input())
p = [i for i in range(m*n+1)]
def find(x):
    if x!=p[x]:
        p[x]=find(p[x])
    return p[x]
def union(x,y):
    x_root=find(x)
    y_root=find(y)
    if x_root!=y_root:
        p[y_root]=x_root
for _ in range(k):
    a, b = list(map(int, input().split()))
    union(a, b)

s = set()

for i in range(1, m*n+1):
    s.add(find(i))
print(len(s))
