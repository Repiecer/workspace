# 原始 flag 字节
flag_bytes = [
    0x3D, 0x50, 0x35, 0x2F, 0x3D, 0x2C, 0x39, 0x5A,
    0x3C, 0x19, 0x2D, 0x1C, 0x30, 0x2A, 0x1B, 0x0D,
    0x00, 0x3B, 0x35, 0x0D, 0x0E, 0x51, 0x58, 0x0D,
    0x39, 0x3C, 0x21, 0x19, 0x0C, 0x3B, 0x53, 0x24
]

# 逆操作：先逆 SIGSEGV_handle (^0x66)，再逆 SIGINT_handle (-5)
result = []
for byte in flag_bytes:
    # 逆 SIGSEGV_handle: 异或 0x66
    byte ^= 0x66
    # 逆 SIGINT_handle: 减 5（处理下溢）
    byte = (byte - 5) & 0xFF
    result.append(byte)

# 转换为字符串
input_str = ''.join(chr(b) for b in result)
print("应该输入的字符串:", input_str)
print("十六进制:", ' '.join(f'{b:02X}' for b in result))
# 正向操作：先 SIGINT_handle (+5)，再 SIGSEGV_handle (^0x66)
result2 = []
for byte in flag_bytes:
    # SIGINT_handle: 加 5
    byte = (byte + 5) & 0xFF
    # SIGSEGV_handle: 异或 0x66
    byte ^= 0x66
    result2.append(byte)

input_str2 = ''.join(chr(b) for b in result2)
print("另一种可能:", input_str2)