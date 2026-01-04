import struct

numbers = [1920221984, 3736432267, 0x72, 1936028192, 3889681299, 0x6c, 27722122, 27722568, 0x73736572]

print("小端序解码:")
for num in numbers:
    try:
        if num > 0xFFFFFFFF:
            continue
        bytes_val = struct.pack('<I', num)
        text = bytes_val.decode('ascii')
        print(f"{num:12} -> '{text}'")
    except:
        pass

print("\n只关注关键值:")
key_nums = [0x72, 0x6c, 0x73736572]
for num in key_nums:
    if num <= 0xFF:
        print(f"0x{num:02X} -> '{chr(num)}'")
    else:
        bytes_val = struct.pack('<I', num)
        text = bytes_val.decode('ascii')
        print(f"0x{num:08X} -> '{text}'")