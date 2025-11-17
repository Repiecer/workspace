results: list = []
for _ in range(int(input())):
    results.append(oct(int(input()))[2:])
print('\n'.join(results))