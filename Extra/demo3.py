is_prime = lambda n: n > 1 and all(n % i for i in range(2, int(n**0.5)+1))
ans =  0
for i in range(1, 1000):
    if is_prime(i):
        ans+=1
    if ans == 80:
        print(i)
        break
