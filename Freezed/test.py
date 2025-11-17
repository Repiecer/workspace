import os
import sys
import math
number = input()
ls1 = list(map(int, input().split()))
ls2 = list(map(int, input().split()))
occasion = 1
def func(lt1 :list, lt2 :list):
  difficult_temp = 0
  diffit = list()
  for i in lt1:
    for j in lt2:
      difficult_temp+=abs(i-j)
    diffit.append(difficult_temp)
    difficult_temp = 0
  if occasion % 2 != 0:
    return diffit.index(max(diffit))
  else:
    return diffit.index(min(diffit))

while True:
  if occasion % 2 != 0:
    del ls1[func(ls1, ls2)]
    occasion +=1
  else:
    del ls2[func(ls2, ls1)]
    if len(ls2) == 1:
      break
    occasion +=1
print(abs(ls1[0]-ls2[0]))
# 请在此输入您的代码