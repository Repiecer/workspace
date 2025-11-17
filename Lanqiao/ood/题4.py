num_or: list = [ord(i)-96 for i in input()]
num_new: list = num_or[:]
while num_new<=num_or[::-1]:
    if num_new[-1] == 26:
        num_new.append(1)
        break
    num_new[-1]+=1
print(''.join(map(chr, [ch+96 for ch in num_new])), end='')
