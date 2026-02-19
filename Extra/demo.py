import calendar
a = 100
def func(x):
    return int(x)**3
#print(sum(map(func, '153')))
while True:
    b = str(a)
    c = sum(map(func, b))
    #print(c)
    if c == a:
        print(a)
    a+=1
    if a == 9999:
        break

