# 读取所有输入数据
data = []
while True:
    try:
        line = input().strip()
        if line:
            data.extend(map(int, line.split()))
    except EOFError:
        break

# 第一个数字是n
n = data[0]
matrix_data = data[1:]

# 检查数据量是否足够
if len(matrix_data) < n * n:
    print("错误：输入数据不足")
    exit()

# 构建n×n矩阵
matrix = []
for i in range(n):
    row = matrix_data[i*n:(i+1)*n]
    matrix.append(row)

# 使用Kadane算法找最大子矩阵和
max_sum = -10**9

for start_row in range(n):
    col_sum = [0] * n
    for end_row in range(start_row, n):
        for j in range(n):
            col_sum[j] += matrix[end_row][j]
        
        # Kadane算法找最大子数组和
        current_max = col_sum[0]
        current_sum = col_sum[0]
        for j in range(1, n):
            current_sum = max(col_sum[j], current_sum + col_sum[j])
            current_max = max(current_max, current_sum)
        
        max_sum = max(max_sum, current_max)

print(max_sum)