try: 
    num = int(input('Enter number:'))
except ValueError:
    print('ValueError')
    exit
root = [100, 50, 10, 5, 1]
for i in range(len(root)):
    print(f'{root[i]}yuan: {num//root[i]}sheet')
    num%=root[i]
