n, m = list(map(int, input().split()))
mal = []
mal.append([0]*(m+2))
for _ in range(n):
    s = input().replace('?', '0').replace('*', '1')
    s = list(map(int, list(s)))
    mal.append([0]+s+[0])
    
    
mal.append([0]*(m+2))
for i in range(1, n):
    for j in range(1, m):
        if mal[i][j]==0:
            mal[i][j] = mal[i][j-1]+mal[i-1][j-1]+mal[i-1][j]+mal[i+1][j+1]+mal[i][j+1]+mal[i+1][j]+mal[i+1][j-1]+mal[i-1][j]
        

