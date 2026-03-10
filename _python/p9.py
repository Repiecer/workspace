import sys
a, b = list(map(int, sys.stdin.readline().split()))

y = lambda m, n:3*n-m

if a==b:
    print(a+b)
elif a>b:
    print(y(a, b))
else:
    print(y(b, a))
