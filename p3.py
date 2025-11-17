
a, b, c, d = list(map(int, input().split()))
def func(x):
    return a*x^3+b*x^2+c*x+d
situ = []
t = -100
odd = func(t)
while t < 101:
    new = func(t+1)
    if odd*new <= 0:
        situ.append([t, t+1])
    odd = new
    t+=1

print(situ)
