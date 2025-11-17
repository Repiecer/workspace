
results: list = []
def gcd_manual(a, b):
    """手动实现最大公约数"""
    while b != 0:
        a, b = b, a % b
    return a


def lcm_manual(a, b):
    """手动实现最小公倍数"""
    return abs(a * b) // gcd_manual(a, b)

for _ in range(int(input())):
    results.append(lcm_manual(*map(int, input().split())))
print(*results, sep='\n')

