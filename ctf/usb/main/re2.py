from scapy.all import *

def analyze_hid_patterns(pcap_file):
    packets = rdpcap(pcap_file)
    
    print("分析HID数据模式...")
    print("=" * 50)
    
    # 收集所有HID数据包
    hid_sequences = []
    
    for i, pkt in enumerate(packets):
        raw = bytes(pkt)
        if len(raw) in [32, 34]:
            usb_data = raw[28:]
            hex_str = usb_data.hex()
            
            # 排除描述符请求
            if not hex_str.startswith('8006') and hex_str != '0000000000000000':
                hid_sequences.append((i, hex_str))
    
    print("HID数据序列:")
    for pkt_num, data in hid_sequences:
        print(f"包 {pkt_num:3d}: {data}")
    
    return hid_sequences

def decode_hid_data(sequences):
    """尝试多种解码方法"""
    print("\n尝试解码HID数据...")
    print("=" * 50)
    
    # 方法1: 直接解析为键盘数据
    print("方法1 - 键盘键码解析:")
    keymap = {
        0x33: "3",  # 根据 050133000100 中的 0x33
        0x01: "1",  # 根据模式推测
        0xff: "-",  # 特殊分隔符
        0xfe: "_"   # 特殊分隔符
    }
    
    result1 = ""
    for pkt_num, data in sequences:
        bytes_data = bytes.fromhex(data)
        print(f"包 {pkt_num}: {data} -> 字节: {list(f'0x{b:02x}' for b in bytes_data)}")
        
        if data == "050133000100":
            # 050133000100 格式分析
            # 0x05 = 报告ID, 0x01 = 修饰键?, 0x33 = 键码'3'
            result1 += "3"
            print("  -> 字符 '3'")
        elif data == "00ff0100":
            result1 += "-"
            print("  -> 分隔符 '-'")
        elif data == "00ffff00":
            result1 += "_"
            print("  -> 分隔符 '_'")
        elif data == "0000fe00":
            result1 += "."
            print("  -> 分隔符 '.'")
    
    print(f"解码结果1: {result1}")
    
    # 方法2: 尝试ASCII解码
    print("\n方法2 - ASCII解码尝试:")
    result2 = ""
    for pkt_num, data in sequences:
        if data == "050133000100":
            # 提取可能的ASCII值
            bytes_data = bytes.fromhex(data)
            # 尝试不同的字节组合
            if bytes_data[2] == 0x33:  # ASCII '3' = 0x33
                result2 += "3"
            if bytes_data[4] == 0x01:  # 可能表示数字1
                result2 += "1"
    
    print(f"解码结果2: {result2}")
    
    # 方法3: 尝试flag模式
    print("\n方法3 - 常见CTF格式:")
    sequences_str = "".join([data for _, data in sequences])
    print(f"数据序列: {sequences_str}")
    
    # 从 050133000100 提取可能的信息
    # 05 01 33 00 01 00 可能表示: 3 和 1
    flag_candidates = []
    
    # 基于数据包顺序构建flag
    if sequences:
        flag_candidates.append("3-1_3")  # 从模式推测
        flag_candidates.append("313")    # 简单数字组合
        flag_candidates.append("flag{3_1_3}")  # 常见格式
    
    print("可能的flag:")
    for candidate in flag_candidates:
        print(f"  {candidate}")
    
    return result1, result2, flag_candidates

# 执行分析
print("开始分析ez_usb.pcapng...")
sequences = analyze_hid_patterns('ez_usb.pcapng')
results = decode_hid_data(sequences)

# 额外分析：查看数据包的时间顺序和模式
print("\n" + "="*50)
print("数据包时间序列分析:")
for i, (pkt_num, data) in enumerate(sequences):
    print(f"顺序 {i}: 包{pkt_num} = {data}")

# 基于序列构建flag
print("\n基于序列构建flag:")
flag_parts = []
for pkt_num, data in sequences:
    if data == "050133000100":
        flag_parts.append("3")
    elif data == "00ff0100":
        flag_parts.append("-")
    elif data == "00ffff00": 
        flag_parts.append("_")
    elif data == "0000fe00":
        flag_parts.append(".")

sequence_flag = "".join(flag_parts)
print(f"序列flag: {sequence_flag}")

# 尝试清理分隔符
clean_flag = sequence_flag.replace("-.", "").replace("_-", "").replace(".-", "")
print(f"清理后: {clean_flag}")

# 输出可能的CTF flag格式
print("\n最终可能的flag:")
print(f"flag{{{clean_flag}}}")
print(f"FLAG{{{clean_flag}}}") 
print(f"ctf{{{clean_flag}}}")