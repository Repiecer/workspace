import sys
from collections import deque

input = sys.stdin.read
data = input().split()

T = int(data[0])
index = 1

def add_binary(str1, str2):
    if not str1:
        str1 = '0'
    if not str2:
        str2 = '0'
    s1 = str1[::-1]
    s2 = str2[::-1]
    carry = 0
    result = []
    i = 0
    max_len = max(len(s1), len(s2))
    while i < max_len or carry:
        bit1 = int(s1[i]) if i < len(s1) else 0
        bit2 = int(s2[i]) if i < len(s2) else 0
        total = bit1 + bit2 + carry
        result.append(str(total % 2))
        carry = total // 2
        i += 1
    res = ''.join(result)[::-1]
    res = res.lstrip('0')
    if not res:
        res = '0'
    return res

for _ in range(T):
    n = int(data[index])
    index += 1
    s = data[index]
    index += 1
    da = deque()
    db = deque()
    sa = 0
    sb = 0
    for char in reversed(s):
        if char == '1':
            if sa <= sb:
                da.appendleft(char)
                sa += 1
            else:
                db.appendleft(char)
                sb += 1
        else:
            if sa >= sb:
                da.appendleft(char)
                sa += 1
            else:
                db.appendleft(char)
                sb += 1
    a_str = ''.join(da)
    b_str = ''.join(db)
    print(add_binary(a_str, b_str))