n = int(input())
matrix = []
for _ in range(n):
    matrix.append(list(map(int, input().split())))

prefix = [[0] * (n + 1) for _ in range(n + 1)]

for i in range(1, n + 1):
    for j in range(1, n + 1):
        prefix[i][j] = (prefix[i-1][j] + prefix[i][j-1] 
                       - prefix[i-1][j-1] + matrix[i-1][j-1])

max_sum = -10**9 

for x1 in range(1, n + 1):
    for y1 in range(1, n + 1):
        for x2 in range(x1, n + 1):
            for y2 in range(y1, n + 1):
                current = (prefix[x2][y2] - prefix[x1-1][y2] 
                          - prefix[x2][y1-1] + prefix[x1-1][y1-1])
                if current > max_sum:
                    max_sum = current

print(max_sum)