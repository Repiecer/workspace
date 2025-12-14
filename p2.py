import sys

input = sys.stdin.read
data = input().split()
t = int(data[0])
idx = 1
out = []
for _ in range(t):
    n = int(data[idx]); m = int(data[idx+1]); idx += 2
    row_xor = [0]*n
    col_xor = [0]*m
    for i in range(n):
        s = data[idx]; idx += 1
        for j in range(m):
            val = ord(s[j]) - 48
            row_xor[i] ^= val
            col_xor[j] ^= val
    R = sum(row_xor)
    C = sum(col_xor)
    if R==0 and C==0:
        out.append("0")
    else:
        out.append(str(max(R, C)))
print("\n".join(out))