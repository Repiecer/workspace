from scapy.all import *
import struct

def extract_8byte_usb_data(pcap_file):
    packets = rdpcap(pcap_file)
    eight_byte_data = []
    
    print("提取8字节USB数据...")
    
    for i, pkt in enumerate(packets):
        raw = bytes(pkt)
        
        # 检查数据包总长度
        if len(raw) == 36:  # 28字节USBPcap头部 + 8字节数据
            # 提取USB数据部分（跳过28字节头部）
            usb_data = raw[28:36]
            hex_str = usb_data.hex()
            eight_byte_data.append(hex_str)
            print(f"包 {i}: {hex_str}")
    
    print(f"\n总共找到 {len(eight_byte_data)} 个8字节数据包")
    return eight_byte_data

# 提取数据
keyboard_data = extract_8byte_usb_data('ez_usb.pcapng')

# 保存到文件
with open('keyboard_data.txt', 'w') as f:
    for item in keyboard_data:
        f.write(item + '\n')