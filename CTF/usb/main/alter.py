from scapy.all import *

def extract_real_hid_data(pcap_file):
    packets = rdpcap(pcap_file)
    hid_packets = []
    
    print("提取真正的HID数据包...")
    
    for i, pkt in enumerate(packets):
        raw = bytes(pkt)
        raw_len = len(raw)
        
        # 查找长度32和34的数据包（包含HID数据）
        if raw_len in [32, 34]:
            usb_data = raw[28:]  # 跳过28字节USBPcap头部
            hex_str = usb_data.hex()
            
            # 只保存非描述符数据
            if not hex_str.startswith('8006') and hex_str != '0000000000000000':
                hid_packets.append((i, raw_len, hex_str))
    
    return hid_packets

# 提取数据
hid_data = extract_real_hid_data('ez_usb.pcapng')

print("找到的HID数据包:")
for i, (pkt_num, length, data) in enumerate(hid_data):
    print(f"{i:2d}. 包 {pkt_num:5d} (长度{length}): {data}")

print(f"\n总共找到 {len(hid_data)} 个HID数据包")

# USB HID键盘键码映射
keymap = {
    0x00: "",
    0x04: "a", 0x05: "b", 0x06: "c", 0x07: "d", 0x08: "e",
    0x09: "f", 0x0a: "g", 0x0b: "h", 0x0c: "i", 0x0d: "j",
    0x0e: "k", 0x0f: "l", 0x10: "m", 0x11: "n", 0x12: "o",
    0x13: "p", 0x14: "q", 0x15: "r", 0x16: "s", 0x17: "t",
    0x18: "u", 0x19: "v", 0x1a: "w", 0x1b: "x", 0x1c: "y",
    0x1d: "z",
    0x1e: "1", 0x1f: "2", 0x20: "3", 0x21: "4", 0x22: "5",
    0x23: "6", 0x24: "7", 0x25: "8", 0x26: "9", 0x27: "0",
    0x28: "\n",  # 回车
    0x2c: " ",   # 空格
    0x2d: "-", 0x2e: "=", 0x2f: "[", 0x30: "]", 0x31: "\\",
    0x33: ";", 0x34: "'", 0x35: "`", 0x36: ",", 0x37: ".",
    0x38: "/",
    0x2a: "[BACKSPACE]",
    0x39: "[CAPS]",
    0x2b: "[TAB]",
    0x4f: "[RIGHT]",
    0x50: "[LEFT]",
    0x51: "[DOWN]", 
    0x52: "[UP]"
}

# Shift键映射
shift_keymap = {
    0x04: "A", 0x05: "B", 0x06: "C", 0x07: "D", 0x08: "E",
    0x09: "F", 0x0a: "G", 0x0b: "H", 0x0c: "I", 0x0d: "J",
    0x0e: "K", 0x0f: "L", 0x10: "M", 0x11: "N", 0x12: "O",
    0x13: "P", 0x14: "Q", 0x15: "R", 0x16: "S", 0x17: "T",
    0x18: "U", 0x19: "V", 0x1a: "W", 0x1b: "X", 0x1c: "Y",
    0x1d: "Z",
    0x1e: "!", 0x1f: "@", 0x20: "#", 0x21: "$", 0x22: "%",
    0x23: "^", 0x24: "&", 0x25: "*", 0x26: "(", 0x27: ")",
    0x2d: "_", 0x2e: "+", 0x2f: "{", 0x30: "}", 0x31: "|",
    0x33: ":", 0x34: '"', 0x35: "~", 0x36: "<", 0x37: ">",
    0x38: "?"
}

def parse_hid_keyboard_data(hid_packets):
    """解析HID键盘数据"""
    result = ""
    
    for pkt_num, length, hex_data in hid_packets:
        if not hex_data:
            continue
            
        data_bytes = bytes.fromhex(hex_data)
        
        print(f"分析包 {pkt_num}: {hex_data}")
        
        # 根据数据长度解析不同格式
        if length == 34:  # 6字节数据包
            # 格式可能是: [report_id, modifier, keycode, ...]
            if len(data_bytes) >= 3:
                if data_bytes[0] == 0x05:  # 可能是报告ID
                    modifier = data_bytes[1]
                    keycode = data_bytes[2]
                    
                    if keycode != 0:
                        char = convert_keycode(keycode, modifier)
                        result += char
                        print(f"  -> 按键: {char} (键码: 0x{keycode:02x}, 修饰键: 0x{modifier:02x})")
        
        elif length == 32:  # 4字节数据包
            # 可能是鼠标数据或特殊按键
            if hex_data == "00ff0100":
                print("  -> 可能是鼠标移动或特殊功能")
            elif hex_data == "00ffff00":
                print("  -> 可能是鼠标移动")
            elif hex_data == "0000fe00":
                print("  -> 可能是鼠标移动")
    
    return result

def convert_keycode(keycode, modifier):
    """转换键码为字符"""
    if modifier in [0x02, 0x20]:  # Shift键
        if keycode in shift_keymap:
            return shift_keymap[keycode]
        elif keycode in keymap:
            char = keymap[keycode]
            return char.upper() if char.isalpha() else char
    else:
        if keycode in keymap:
            return keymap[keycode]
    
    return f"[{keycode:02x}]"

# 解析数据
print("解析HID键盘数据...")
print("=" * 50)
flag = parse_hid_keyboard_data(hid_data)
print("=" * 50)
print(f"解析结果: {flag}")
