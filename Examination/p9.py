import sys

input = lambda: sys.stdin.buffer.readline().rstrip()
mi = lambda: map(int, input().split())
li = lambda: list(mi())


def get(l, r):
    return sum[r] - sum[l - 1]


if __name__ == '__main__':
    INF = 40000000000
    n = int(input())
    a = []
    suf = [0 for _ in range(n + 2)]
    vec = []
    sum = [0 for _ in range(n + 2)]
    tot = 0
    a.append(0)
    b = li()
    a += b
    i = 1
    while i <= n:
        if a[i] > 1:
            vec.append(i)
            tot += 1
        sum[i] = sum[i - 1] + a[i]
        i += 1
    res = 0
    cnt = 0
    for i in range(n, 0, -1):
        if a[i] > 1:
            suf[i] = cnt
            cnt = 0
        else:
            cnt += 1
    i = 1
    while i <= n:
        res += 1
        now = a[i]
        L = 0
        R = tot - 1
        pos = n
        while L <= R:
            mid = L + R >> 1
            if vec[mid] > i:
                R = mid - 1
                pos = mid
            else:
                L = mid + 1
        j = pos
        while j < tot:
            now *= a[vec[j]]
            if now > INF:
                break
            if get(i, vec[j]) <= now <= get(i, vec[j]) + suf[vec[j]]:
                res += 1
            j += 1
        i += 1
    print(res)