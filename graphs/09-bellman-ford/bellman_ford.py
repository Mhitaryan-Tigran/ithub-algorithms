INF = float("inf")
EDGES = [("A", "B", 4), ("A", "C", 5), ("B", "C", -2), ("B", "D", 6), ("C", "D", 3), ("C", "E", 4), ("D", "E", 2)]


def bellman_ford(graph, start):
    vertices = sorted({v for u, w, _ in graph for v in (u, w)})
    distance = {v: INF for v in vertices}
    parent = {v: None for v in vertices}
    distance[start] = 0
    rounds = 0
    for _ in range(len(vertices) - 1):
        rounds += 1
        changed = False
        for u, v, w in graph:
            if distance[u] + w < distance[v]:
                distance[v], parent[v] = distance[u] + w, u
                changed = True
        if not changed:
            break
    for u, v, w in graph:
        if distance[u] + w < distance[v]:
            parent[v] = u
            vertex = v
            for _ in range(len(vertices)):
                vertex = parent[vertex]
            cycle, current = [vertex], parent[vertex]
            while current != vertex:
                cycle.append(current)
                current = parent[current]
            cycle.reverse()
            return distance, parent, cycle + [cycle[0]], rounds
    return distance, parent, None, rounds


def path(parent, target):
    result = [target]
    while parent[result[-1]] is not None:
        result.append(parent[result[-1]])
    return result[::-1]


if __name__ == "__main__":
    distance, parent, cycle, rounds = bellman_ford(EDGES, "A")
    print(f"Bellman-Ford from A, stopped after {rounds} relaxation rounds of at most |V| - 1 = 4")
    for v in distance:
        print(f"  {v} = {distance[v]:>2}  parent {parent[v]}  path {' → '.join(path(parent, v))}")
    print("negative cycle:", cycle)

    with_cycle = EDGES + [("E", "B", -7)]
    _, _, cycle2, _ = bellman_ford(with_cycle, "A")
    weight = sum(w for a, b in zip(cycle2, cycle2[1:]) for u, v, w in with_cycle if (u, v) == (a, b))
    print("\nWith E→B = -7:")
    print("  after |V| - 1 rounds an edge still relaxes, so a negative cycle is reachable from A")
    print("  cycle:", " → ".join(cycle2), "weight", weight, "- distances on it can be decreased forever")

    assert distance == {"A": 0, "B": 4, "C": 2, "D": 5, "E": 6} and cycle is None
    assert path(parent, "E") == ["A", "B", "C", "E"]
    assert sorted(cycle2[:-1]) == ["B", "C", "E"] and weight == -5
    print("checks passed")
