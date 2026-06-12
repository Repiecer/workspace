MOD = 10**9 + 7

def solve():
    N = 2025
    fib = [1, 1]
    while len(fib) <= (len(bin(N)) + 5):  # 预估够长
        fib.append((fib[-1] + fib[-2]) % MOD)
    
    def f_len(length):
        return fib[length + 1]  # f[length] = Fib(length+2) 时
    
    ans = 1
    for v in range(1, N + 1, 2):
        # v 是奇数
        k = 0
        while v * (2 ** k) <= N:
            k += 1
        # k 是节点数? 检查：
        # 节点：v, 2v, 4v, ..., 2^(k-1)v ≤ N
        # 所以长度为 k
        length = k
        ans = (ans * f_len(length)) % MOD
    
    print(ans)

solve()