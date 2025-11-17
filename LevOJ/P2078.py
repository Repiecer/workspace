num: int = int(input())
weapon: list = list(map(int, input().split()))
steal: list = list(map(int, input().split()))
harm_sum: int = 0
for _ in range(1, len(steal)+1):
    be_steal = steal.index(_)
    harm_sum+=max(weapon)
    weapon[be_steal] = 0
print(harm_sum, end='')