import sys

def solve():
    input = sys.stdin.readline
    n, m = map(int, input().split())
    
    bit = [0] * (n + 3)
    
    def update(idx, delta):
        while idx <= n + 1:
            bit[idx] += delta
            idx += idx & -idx
    
    def query(idx):
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & -idx
        return s
    
    for _ in range(m):
        op = list(map(int, input().split()))
        if op[0] == 1:
            L, R = op[1], op[2]
            update(L, 1)
            update(R + 1, -1)
        else:
            i = op[1]
            print(query(i) & 1)

if __name__ == "__main__":
    solve()