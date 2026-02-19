import calendar

a = 1
b = 1000
c = 20
ans = 0

for i in range(a, b+1):
    if calendar.isleap(i):
        ans+=1
    if ans == c:
        print(i)
        break
