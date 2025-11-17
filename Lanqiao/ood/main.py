import os
import sys

month: str = input()
Q1 = [1, 2, 3]
Q2 = [4, 5, 6]
Q3 = [7, 8, 9]
Q4 = [10, 11, 12]
if month in map(str, Q1):
    print('Q1')
elif month in map(str, Q2):
    print('Q2')
elif month in map(str, Q3):
    print('Q3')
elif month in map(str, Q4):
    print('Q4')
else:
    print('??')
# 请在此输入您的代码