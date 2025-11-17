arr: list = []
for _ in range(int(input())):
    arr.append(list(map(int, input().split())))
position: tuple = tuple(map(int, input().split()))
result = -1
for i, j in enumerate(arr[::-1]):
    if j[0] <= position[0] < j[0]+j[2] and j[1] <= position[1] < j[1]+j[3]:
        result = len(arr) - i
print(result)
