import os
import sys
import heapq as he

n,k = map(int,input().split())
ball = tuple(map(int,input().split()))
k += 1
if n <= k + 1:
    print(ball[0]+ball[-1])
    sys.exit()
black = [(ball[0],0)]
he.heapify(black)
for i in range(1,n-1):
    while True:
        t = he.heappop(black)
        if t[1] + k >= i:
            break
    he.heappush(black,(ball[i]+t[0],i))
    he.heappush(black,t)
while True:
    t = he.heappop(black)
    if t[1] + k >= n-1:
        break
print(t[0]+ball[-1])