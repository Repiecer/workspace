from math import gcd
from functools import reduce
results: list = []
for _ in range(int(input())):
    results.append(reduce(gcd, map(int, input().split())))
print('\n'.join(map(str, results)))