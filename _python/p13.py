import heapq

def dijkstra(n, graph, start):
    INF = 10e18
    dist = [INF]*n
    dist[start]=0
    pq = [(0, start)]
    while pq:
        d, u  = heapq.heappop(pq)
        if d>dist[u]:
            continue
        for v, w in graph[u]:
            nd = d+w
            if nd<dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))