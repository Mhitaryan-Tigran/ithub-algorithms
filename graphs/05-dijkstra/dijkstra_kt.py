import heapq
import random
from collections import deque
from itertools import permutations


def total_delay(routers, wires, entry_points):
    graph = {r: [] for r in routers}
    for u, v, w in wires:
        graph[u].append((v, w))
        graph[v].append((u, w))
    limit = sum(w for _, _, w in wires)
    distance = {r: None for r in routers}
    buckets = [[] for _ in range(limit + 1)]
    for e in entry_points:
        distance[e] = 0
        buckets[0].append(e)
    for d in range(limit + 1):
        for router in buckets[d]:
            if distance[router] != d:
                continue
            for neighbour, w in graph[router]:
                if distance[neighbour] is None or d + w < distance[neighbour]:
                    distance[neighbour] = d + w
                    buckets[d + w].append(neighbour)
    return sum(distance.values()), distance


def total_delay_heap(routers, wires, entry_points):
    graph = {r: [] for r in routers}
    for u, v, w in wires:
        graph[u].append((v, w))
        graph[v].append((u, w))
    distance = {r: float("inf") for r in routers}
    heap = [(0, e) for e in entry_points]
    for e in entry_points:
        distance[e] = 0
    while heap:
        d, router = heapq.heappop(heap)
        if d > distance[router]:
            continue
        for neighbour, w in graph[router]:
            if d + w < distance[neighbour]:
                distance[neighbour] = d + w
                heapq.heappush(heap, (d + w, neighbour))
    return sum(distance.values())


def bfs(flights, start):
    parent, queue = {start: None}, deque([start])
    while queue:
        city = queue.popleft()
        for nxt in flights.get(city, []):
            if nxt not in parent:
                parent[nxt] = city
                queue.append(nxt)
    return parent


def path_from(parent, goal):
    if goal not in parent:
        return None
    path = [goal]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    return path[::-1]


def honeymoon(cities, flights, home, wishes):
    graph = {c: [] for c in cities}
    for source, target in flights:
        graph[source].append(target)
    trees = {city: bfs(graph, city) for city in [home] + list(wishes)}
    best = None
    for order in permutations(wishes):
        stops = [home, *order, home]
        legs = [path_from(trees[a], b) for a, b in zip(stops, stops[1:])]
        if any(leg is None for leg in legs):
            continue
        flights_count = sum(len(leg) - 1 for leg in legs)
        if best is None or flights_count < best[0]:
            route = legs[0] + [city for leg in legs[1:] for city in leg[1:]]
            best = (flights_count, order, route)
    return best


if __name__ == "__main__":
    routers = list(range(1, 9))
    wires = [(1, 2, 4), (2, 3, 3), (3, 4, 2), (4, 5, 6), (5, 6, 1), (6, 7, 5), (7, 8, 2), (8, 1, 9), (2, 7, 1), (3, 6, 8)]
    total, distance = total_delay(routers, wires, entry_points=[1, 5])
    print("Network delays: routers 1..8, entry points 1 and 5")
    for router in routers:
        print(f"  router {router}: {distance[router]} m to the nearest entry point")
    print("  total delay:", total)

    cities = ["Ростов", "Москва", "Стамбул", "Дубай", "Пхукет", "Мале", "Ереван", "Тбилиси"]
    flights = [
        ("Ростов", "Москва"), ("Ростов", "Ереван"), ("Москва", "Дубай"), ("Москва", "Пхукет"),
        ("Ереван", "Дубай"), ("Дубай", "Мале"), ("Мале", "Дубай"), ("Дубай", "Пхукет"),
        ("Пхукет", "Стамбул"), ("Стамбул", "Тбилиси"), ("Тбилиси", "Ростов"), ("Стамбул", "Ростов"),
        ("Дубай", "Стамбул"), ("Москва", "Ростов"),
    ]
    count, order, route = honeymoon(cities, flights, "Ростов", ["Мале", "Пхукет", "Стамбул"])
    print("\nHoneymoon from Ростов to Мале, Пхукет, Стамбул")
    print("  visiting order:", ", ".join(order))
    print("  route:", " → ".join(route))
    print("  flights:", count)

    assert total == total_delay_heap(routers, wires, [1, 5]) == 30
    assert count == 7 and route[0] == route[-1] == "Ростов"
    assert all((a, b) in flights for a, b in zip(route, route[1:]))
    random.seed(9)
    for _ in range(200):
        r = random.randint(2, 30)
        nodes = list(range(r))
        edges = [(i, random.randrange(i), random.randint(1, 20)) for i in range(1, r)]
        edges += [(random.randrange(r), random.randrange(r), random.randint(1, 20)) for _ in range(r)]
        edges = [e for e in edges if e[0] != e[1]]
        entries = random.sample(nodes, random.randint(1, min(3, r)))
        assert total_delay(nodes, edges, entries)[0] == total_delay_heap(nodes, edges, entries)
    print("checks passed")
