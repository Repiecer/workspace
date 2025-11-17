move: int = int(input())
road: list = [1]
if move == 1:
    print(-1)
else:
    road.append(2)
    for _ in range((move-2)//3):
        road.extend([3,4,2])
    road.extend([3,4,2][:(move-2)%3])
    road.append(1)
    print(' '.join(map(str, road)))