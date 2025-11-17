length: int = int(input())
ls: list = list(map(int, input().split()))
if len(ls) != length:
    raise ValueError("List length does not match the specified length.")
print(ls[(length - 1) // 2])