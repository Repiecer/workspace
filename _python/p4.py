t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    freq = {}
    for num in arr:
        freq[num] = freq.get(num, 0) + 1
    score = 0
    for count in freq.values():
        score += count // 2
    
    print(score)