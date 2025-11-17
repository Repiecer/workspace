def gcd_manual(a, b):
    """手动实现最大公约数"""
    while b != 0:
        a, b = b, a % b
    return a

def lcm_manual(a, b):
    """手动实现最小公倍数"""
    return abs(a * b) // gcd_manual(a, b)


a, b = map(int, input().split())
print(gcd_manual(a, b), lcm_manual(a, b), sep='\n')
