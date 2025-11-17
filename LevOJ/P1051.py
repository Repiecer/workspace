def is_prime_6k(n):
    """使用 6k±1 优化"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    # 检查 6k±1 形式的除数
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
ls: list = []
for _ in range(int(input())):
    ls.append(int(input()))

for i in ls:
    if is_prime_6k(i) and is_prime_6k(int(str(i)[::-1])):
        print(1)
    else:
        print(0)