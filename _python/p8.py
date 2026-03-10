from collections import Counter
n = input()
string = input()
counts = Counter(string)
ans = 0
for i in counts.values():
    if i%2 != 0:
        ans+=1
print(max(ans, 1))
