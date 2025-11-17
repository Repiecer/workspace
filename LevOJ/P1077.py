fibonacci: list = [1, 1]
len_n: int = int(input())
sum_n: int = 0
for _ in range(len_n):
    fibonacci.append(fibonacci[-1] + fibonacci[-2])
for i in range(len_n):
    sum_n += ((-1) ** i)*(fibonacci[i+2]/fibonacci[i+1])
print(f"{sum_n:.10f}")