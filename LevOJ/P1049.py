ls: list = list(map(float, input().split()))
print("%.6f"%(ls[1] + ls[0] % 3 * int(ls[1] + ls[2]) % 2 / 4))
