# 函数main定义
# 主体代码逻辑
def main():
    a, b = input().split()
    a, b = int(a), int(b)
    cnt = 0
    for i in range(a, b+1):
        if is_prime(i):
            cnt += 1
    print(cnt)
def is_prime(x):
    if x <=1:
        return False
    for i in range(2, int(0.5*x)+1):
        if x%i==0:
            return False
    return True
# 函数is_prime定义
# 判断一个整数n是否是素数. 是返回True, 否则返回False
# 待补足


# 函数调用
main()