n, sub = list(map(int, input().split()))
weights: list = list(map(int, input().split()))
trick = -1
def dfs(depth, last: list, odd: int):
    if trick != -1:
        return
    if odd > sub:
        return
    elif odd == sub:
        return True
    for i in range(len(last)):
        dfs(depth+1, )

def main():
    for i in range(1, n+1):
        for j in 
