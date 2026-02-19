ans = []
def main(string):
    t = string.count('U')
    if t%2 == 0:
        return 'NO'
    else:
        return 'YES'

for _ in range(int(input())):
    n = input()
    ans.append(main(input()))

print(*ans, sep='\n')
