from scapy.all import *

def comprehensive_analysis(pcap_file):
    packets = rdpcap(pcap_file)
    
    print("综合分析USB数据包...")
    print("=" * 60)
    
    # 统计不同长度的数据包
    length_stats = {}
    potential_data = []
    
    for i, pkt in enumerate(packets):
        raw_len = len(pkt)
        length_stats[raw_len] = length_stats.get(raw_len, 0) + 1
        
        # 查找可能包含键盘数据的包
        if 30 <= raw_len <= 40:
            raw_data = bytes(pkt)
            if raw_len > 28:
                usb_data = raw_data[28:]
                hex_str = usb_data.hex()
                
                # 检查是否包含非零数据
                if any(b != 0 for b in usb_data):
                    potential_data.append((i, raw_len, hex_str))
    
    print("数据包长度统计:")
    for length, count in sorted(length_stats.items()):
        if 30 <= length <= 40:
            print(f"  长度 {length}: {count} 个包")
    
    print(f"\n找到 {len(potential_data)} 个可能包含HID数据的包")
    print("\n前20个可能的数据包:")
    for i, (pkt_num, length, data) in enumerate(potential_data[:20]):
        data_len = length - 28
        print(f"{i:2d}. 包 {pkt_num:5d} (总长{length}, 数据{data_len}): {data}")
    
    return potential_data

# 运行分析
data_packets = comprehensive_analysis('ez_usb.pcapng')

# 保存结果
with open('potential_hid_data.txt', 'w') as f:
    for pkt_num, length, data in data_packets:
        f.write(f"{pkt_num} {length} {data}\n")

print(f"\n结果已保存到 potential_hid_data.txt")