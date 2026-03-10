a = int(input('Enter a:'))
b = int(input('Enter b:'))
c = int(input('Enter c:'))

check = b**2-4*a*c
if check < 0:
    exit
x1 = (-b+check**0.5)/(2*a)
x2 = (-b-check**0.5)/(2*a)
print(f'x1 = {x1:.2f}, x2 = {x2:.2f}')

