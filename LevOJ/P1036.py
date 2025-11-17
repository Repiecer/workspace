array: list = []
for _ in range(int(input())):
    array.append(list(map(int, input().split())))
for i in range(len(array)):
    for j in range(i + 1, len(array)):
        array[i][j], array[j][i] = array[j][i], array[i][j]
print('\n'.join([' '.join(map(str, item)) for item in array]))