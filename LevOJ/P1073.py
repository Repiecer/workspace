def remove_zeros_simple(n):
    """简化的字符串方法"""
    s = str(n)
    # 去除末尾零，但如果全部是零则保留一个
    s_clean = s.rstrip('0')
    return int(s_clean) if s_clean else 0

num: int = remove_zeros_simple(int(input()))
if num >= 0:
    print(str(num)[::-1])
else:

    print('-' + str(num)[:0:-1])
