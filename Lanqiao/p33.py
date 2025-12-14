import os
import sys
n, m, k = list(map(input().split()))
mal = []
for _ in range(k):
    mal.append(list(map(input().split())))
for i in range(n):
    for j in range(m):
        if [i+1, j+1] in [k[:2] for k in mal]:
            print(mal[i][j])
