encrypted = [80, 43, 212, 98, 229, 110, 27, 230, 54, 17, 109, 235, 145, 246, 133, 246, 196, 118, 111, 5, 95, 161, 12, 45]
known_keystream = [0x36, 0x47, 0xb5, 0x05, 0x9e]

# 方法1：尝试密钥流重复
print("方法1: 密钥流重复")
for repeat_len in [5, 4, 8]:
    extended_ks = (known_keystream * (len(encrypted) // repeat_len + 1))[:len(encrypted)]
    result = bytes([encrypted[i] ^ extended_ks[i] for i in range(len(encrypted))])
    print(f"重复长度 {repeat_len}: {result}")

# 方法2：尝试线性同余生成器
print("\n方法2: LCG生成器")
def lcg(seed, a, c, m):
    while True:
        seed = (a * seed + c) % m
        yield seed & 0xFF

# 测试不同的LCG参数
for a in [1664525, 1103515245, 22695477]:  # 常见LCG乘数
    for c in [1013904223, 12345, 1]:
        ks_gen = lcg(known_keystream[0], a, c, 256)
        test_keystream = [next(ks_gen) for _ in range(len(encrypted))]
        test_keystream[0] = known_keystream[0]  # 确保第一个匹配
        
        result = bytes([encrypted[i] ^ test_keystream[i] for i in range(len(encrypted))])
        if result.startswith(b'flag'):
            print(f"找到! a={a}, c={c}: {result}")