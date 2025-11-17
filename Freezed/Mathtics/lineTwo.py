from typing import Any
from matplotlib import pyplot as plt
from random import randint
import time

force = 5
step = 0.1
a = 1
b = 1
#x = [2, 3, 6, 8, 7, 12, 36, 55]
#y = [3, 4, 7, 9, 10 ,13, 38, 57]
x = [1]
y = [2]
for i in range(30):
    x.append(x[-1]+randint(1, 15))
    y.append(y[-1]+randint(1, 15))
start = time.time()

class ErrorFix:
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return None

# 结果根函数
def line(inpx, a_in, b_in):return a_in*inpx + b_in

# 损失函数
def lostVoid(a_in=a, b_in=b):
    if len(x) != len(y):
        return ErrorFix
    VNR = 0
    for i in range(len(x)):
        VNR += (y[i]-line(x[i], a_in, b_in))**2
    return VNR/(len(x)**force)


def lineStatuForA(TVoid, xLi):
    try:
        _call = 1
        statiu = (TVoid(xLi+_call)-TVoid(xLi))/_call
        while True:
            _call = _call/2
            newStatiu = (TVoid(xLi+_call)-TVoid(xLi))/_call
            
            if statiu == newStatiu:
                break
            else:
                statiu = newStatiu
        return statiu
    except ZeroDivisionError:
        return statiu
def lineStatuForB(TVoid, xLi):
    try:
        _call = 1
        statiu = (TVoid(a, xLi+_call)-TVoid(a, xLi))/_call
        while True:
            _call = _call/2
            newStatiu = (TVoid(a, xLi+_call)-TVoid(a, xLi))/_call
            
            if statiu == newStatiu:
                break
            else:
                statiu = newStatiu
        return statiu
    except ZeroDivisionError:
        return statiu

def lineTicSimu():
    global a
    global b
    while True:
        tempA = a - step*lineStatuForA(lostVoid, a)
        tempB = b - step*lineStatuForB(lostVoid, b)
        if (tempA == a) and (tempB == b):
            break
        else:
            a = tempA
            b = tempB
lineTicSimu()

print(lostVoid())
print(a, b)
end = time.time()
print("TIME:"+str(end-start))
plt.plot([x[0], x[-1]], [line(x[0], a, b), line(x[-1], a, b)])

plt.scatter(x, y)
plt.show()


