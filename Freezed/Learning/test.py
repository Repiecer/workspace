from functools import lru_cache
@lru_cache(maxsize=None)
def main():
    a=1
    while a<=9:
        b=1
        while b<=a:
            print(f"{a}**{b}={a**b}",end="\t")
            b+=1
        print()
        a+=1
main()