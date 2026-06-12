from collections import Counter

t = 0
while True:
    t +=1
    p = str(t**2)+str(t**3)
    ans = dict(Counter(p))
    if len(ans.items())!=10:
        continue
    for k, v in ans.items():
        if v!=1:
            continue
    print(t)
    break
    

