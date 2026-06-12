import sys
sys.setrecursionlimit(10000000)
n, m = list(map(int, input().split()))
arr = []
for _ in range(n):
    arr.append(sys.stdin.readline())
for i in range(n):
    for j in range(m):
        if arr[i][j]=='S':
            po_s = (i, j)
        if arr[i][j]=='T':
            po_t = (i, j)

s = 1
visited = []
def dfs(length, pos):
    if 0 <= pos[0] <= n-1 and 0 <= pos[1] <= m-1:
        if pos in visited:
            return
        if arr[pos[0]][pos[1]] == 'T':
            s = max(s, length)
            return
        if arr[pos[0]][pos[1]] == '#':
            return
        if arr[pos[0]][pos[1]] == '.':
            length+=1
        elif arr[pos[0]][pos[1]] == 'W':
            length+=3
        for ds in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            
            dfs(length, pos+ds)
dfs(s, po_s)

print(arr)