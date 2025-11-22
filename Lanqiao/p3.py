import os
import sys

N = int(input())
A = list(map(int,input().split()))
mod = int(1e9)+7
cnt = 0
t = 0
for i in range(N-1):
    t ^= A[i]    
    cnt += t*2*pow(3,N-i-2,mod)
    cnt %= mod
cnt += t^A[-1]
print(cnt%mod)