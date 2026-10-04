INF = float("inf")
EDGES = [("A", "B", 4), ("A", "C", 5), ("B", "C", -2), ("B", "D", 6), ("C", "D", 3), ("C", "E", 4), ("D", "E", 2)]


def floyd_warshall(graph):
    vertices = sorted({v for u, w, _ in graph for v in (u, w)})
    n = len(vertices)
    index = {v: i for i, v in enumerate(vertices)}
    dist = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    next_vertex = [[i if i == j else None for j in range(n)] for i in range(n)]
    for u, v, w in graph:
        dist[index[u]][index[v]] = w
        next_vertex[index[u]][index[v]] = index[v]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_vertex[i][j] = next_vertex[i][k]
    negative = [vertices[i] for i in range(n) if dist[i][i] < 0]
    return vertices, dist, next_vertex, negative


def route(vertices, next_vertex, source, target):
    i, j = vertices.index(source), vertices.index(target)
    if next_vertex[i][j] is None:
        return None
    path = [i]
    while i != j:
        i = next_vertex[i][j]
        path.append(i)
    return [vertices[k] for k in path]


def show(vertices, dist):
    lines = ["     " + "".join(f"{v:>5}" for v in vertices)]
    for v, row in zip(vertices, dist):
        lines.append(f"{v:>5}" + "".join(f"{'∞' if x == INF else x:>5}" for x in row))
    return "\n".join(lines)


if __name__ == "__main__":
    vertices, dist, next_vertex, negative = floyd_warshall(EDGES)
    print("Distance matrix:")
    print(show(vertices, dist))
    results = {}
    for source, target in [("A", "E"), ("B", "D"), ("E", "A")]:
        path = route(vertices, next_vertex, source, target)
        weight = dist[vertices.index(source)][vertices.index(target)]
        results[(source, target)] = (path, weight)
        print(f"{source}→{target}: " + (f"{'→'.join(path)}, weight {weight}" if path else "no path"))
    print("negative cycle:", negative or "none")

    _, dist2, _, negative2 = floyd_warshall(EDGES + [("E", "B", -7)])
    print("\nWith E→B = -7: diagonal", [dist2[i][i] for i in range(5)])
    print("negative values on the diagonal mean a vertex reaches itself with negative cost:", ", ".join(negative2))

    assert results[("A", "E")] == (["A", "B", "C", "E"], 6)
    assert results[("B", "D")] == (["B", "C", "D"], 1)
    assert results[("E", "A")] == (None, INF)
    assert not negative and negative2 == ["B", "C", "D", "E"]
    print("checks passed")
