temp = input()
if int(temp) == 6174:
    print(0)
    exit(0)

num: int = int("".join(sorted(list(temp), reverse=True)))
times: int = 0
while num != 6174:
    times += 1
    num = int("".join(sorted(list(str(num).zfill(4)), reverse=True))) - int("".join(sorted(list(str(num).zfill(4)))))

print(times)
