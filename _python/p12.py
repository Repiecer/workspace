
f = open('words.txt','r')

texts = f.readlines()
texts = [t[:-1] for t in texts]
old = set()
new = set()
leng = 1
for w in texts:
    if len(w)==1:
        old.add(w)
ans = set()
while True:
    leng+=1
    ans = old
    for w in texts:
        if len(w)==leng:
            for o in old:
                if ''.join(sorted(o)) in ''.join(sorted(w)):
                    new.add(w)
                    break
    if len(new)==0:
        print(old)
        break
    old = new
    new = set()
