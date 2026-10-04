from collections import deque

V = ["A", "B", "C", "D", "E"]
E = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "E")]

PICTURE = r"""
    A --- B --- D
     \   /
      \ /
       C --- E
"""


def adjacency(vertices, edges):
    graph = {v: [] for v in vertices}
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    return graph


def is_walk(graph, route):
    return all(b in graph[a] for a, b in zip(route, route[1:]))


def is_simple_path(graph, route):
    return is_walk(graph, route) and len(set(route)) == len(route)


def is_cycle(graph, route):
    inner = route[:-1]
    return len(route) >= 4 and route[0] == route[-1] and is_walk(graph, route) and len(set(inner)) == len(inner)


def bfs_path(graph, start, goal):
    parent, queue = {start: None}, deque([start])
    while queue:
        vertex = queue.popleft()
        for neighbour in graph[vertex]:
            if neighbour not in parent:
                parent[neighbour] = vertex
                queue.append(neighbour)
    if goal not in parent:
        return None
    path = [goal]
    while parent[path[-1]]:
        path.append(parent[path[-1]])
    return path[::-1]


def is_connected(graph):
    start = next(iter(graph))
    return all(bfs_path(graph, start, v) for v in graph)


if __name__ == "__main__":
    graph = adjacency(V, E)
    print("1. Graph:", PICTURE)
    print("2. Order |V| =", len(V), " size |E| =", len(E))
    degrees = {v: len(graph[v]) for v in V}
    print("3. Degrees:", degrees, " sum =", sum(degrees.values()), "= 2|E|")
    walk, path, cycle = ["A", "B", "C", "A", "B", "D"], ["D", "B", "A", "C", "E"], ["A", "B", "C", "A"]
    print("4. Walk (vertices may repeat):", " - ".join(walk), is_walk(graph, walk))
    print("   Simple path (no repeated vertices):", " - ".join(path), is_simple_path(graph, path))
    print("   Cycle:", " - ".join(cycle), is_cycle(graph, cycle))
    print("5. Adjacency list:")
    for v in V:
        print(f"   {v}: {', '.join(graph[v])}")
    print("6. Connected:", is_connected(graph))
    shortest = bfs_path(graph, "A", "E")
    print("7. Shortest path A -> E:", " - ".join(shortest), "length", len(shortest) - 1)

    assert degrees == {"A": 2, "B": 3, "C": 3, "D": 1, "E": 1}
    assert is_walk(graph, walk) and not is_simple_path(graph, walk)
    assert is_simple_path(graph, path) and is_cycle(graph, cycle) and not is_cycle(graph, ["A", "B", "A"])
    assert is_connected(graph) and shortest == ["A", "C", "E"]
    print("checks passed")
