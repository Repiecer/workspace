num1: int = int(input())
num2: int = int(input())
ls1: list = list(map(int, input().split()))
ls2: list = list(map(int, input().split()))
ls3: list = ls1 + ls2
ls3.sort()
print(*ls3)