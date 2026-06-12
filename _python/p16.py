data = ['99,81,75',
        '30,42,90,87',
        '69,50,96,77,89,93',
        '82,99,78,100']

ans = []
for i in data:
    ans+=i.split(',')
ans = list(map(int, ans))
print(f'{sum(ans)/len(ans):.2f}')

