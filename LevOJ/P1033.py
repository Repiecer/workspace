input()
raw = list(map(int, input().split()))
for i in range(len(raw)):
    for j in range(i + 1, len(raw)):
        if raw[i] > raw[j]:
            raw[i], raw[j] = raw[j], raw[i]
print(' '.join(map(str, raw)))