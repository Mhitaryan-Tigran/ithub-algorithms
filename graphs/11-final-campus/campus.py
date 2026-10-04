import heapq
from collections import deque
from numbers import Real

INF = float("inf")

OBJECTS = {
    "A": "Административный корпус",
    "B": "Библиотека",
    "C": "Учебный корпус",
    "D": "Лаборатория",
    "E": "Общежитие",
    "F": "Спортивный комплекс",
    "G": "Автостоянка",
}

EDGES = [
    ("A", "B", 3), ("A", "C", 8), ("A", "E", 15), ("B", "C", 2), ("B", "D", 5), ("C", "D", 1), ("C", "E", 7),
    ("D", "B", 4), ("D", "E", 2), ("D", "F", 6), ("E", "F", 1), ("F", "C", 3), ("G", "F", 2),
]


class DirectedWeightedGraph:
    def __init__(self, allow_negative=False):
        self.vertices = []
        self.adjacency = {}
        self.allow_negative = allow_negative

    def add_vertex(self, vertex):
        if vertex in self.adjacency:
            return False, f"vertex {vertex} already exists"
        self.vertices.append(vertex)
        self.adjacency[vertex] = {}
        return True, f"vertex {vertex} added"

    def add_edge(self, source, target, weight):
        if source not in self.adjacency or target not in self.adjacency:
            return False, f"edge {source}→{target} rejected: both vertices must exist"
        if source == target:
            return False, f"edge {source}→{target} rejected: loops are not allowed"
        if target in self.adjacency[source]:
            return False, f"edge {source}→{target} rejected: it already exists"
        if not isinstance(weight, Real) or isinstance(weight, bool):
            return False, f"edge {source}→{target} rejected: weight must be a number"
        if weight <= 0 and not self.allow_negative:
            return False, f"edge {source}→{target} rejected: weight must be positive"
        self.adjacency[source][target] = weight
        return True, f"edge {source}→{target} = {weight} added"

    def remove_edge(self, source, target):
        if target not in self.adjacency.get(source, {}):
            return False, f"edge {source}→{target} does not exist"
        del self.adjacency[source][target]
        return True, f"edge {source}→{target} removed"

    def remove_vertex(self, vertex):
        if vertex not in self.adjacency:
            return False, f"vertex {vertex} does not exist"
        del self.adjacency[vertex]
        self.vertices.remove(vertex)
        for targets in self.adjacency.values():
            targets.pop(vertex, None)
        return True, f"vertex {vertex} and its edges removed"

    def has_edge(self, source, target):
        return target in self.adjacency.get(source, {})

    def get_weight(self, source, target):
        return self.adjacency.get(source, {}).get(target)

    def neighbors(self, vertex):
        return sorted(self.adjacency[vertex])

    def predecessors(self, vertex):
        return sorted(v for v in self.vertices if vertex in self.adjacency[v])

    def in_degree(self, vertex):
        return len(self.predecessors(vertex))

    def out_degree(self, vertex):
        return len(self.adjacency[vertex])

    def vertex_count(self):
        return len(self.vertices)

    def edge_count(self):
        return sum(len(t) for t in self.adjacency.values())


def build():
    graph = DirectedWeightedGraph()
    for vertex in OBJECTS:
        graph.add_vertex(vertex)
    for edge in EDGES:
        graph.add_edge(*edge)
    return graph


def reachable(graph, start, undirected=False):
    seen, queue = {start}, deque([start])
    while queue:
        vertex = queue.popleft()
        nxt = graph.neighbors(vertex) + (graph.predecessors(vertex) if undirected else [])
        for n in nxt:
            if n not in seen:
                seen.add(n)
                queue.append(n)
    return seen


def has_cycle(graph):
    color = {v: 0 for v in graph.vertices}

    def visit(v):
        color[v] = 1
        for n in graph.neighbors(v):
            if color[n] == 1 or (color[n] == 0 and visit(n)):
                return True
        color[v] = 2
        return False

    return any(color[v] == 0 and visit(v) for v in graph.vertices)


def properties(graph):
    everyone = set(graph.vertices)
    return {
        "directed": any(not graph.has_edge(t, s) for s in graph.vertices for t in graph.neighbors(s)),
        "weighted": len({w for s in graph.vertices for w in graph.adjacency[s].values()}) > 1,
        "loops": any(graph.has_edge(v, v) for v in graph.vertices),
        "multiple edges": len(EDGES) != len({(s, t) for s, t, _ in EDGES}),
        "cycles": has_cycle(graph),
        "weakly connected": reachable(graph, graph.vertices[0], undirected=True) == everyone,
        "strongly connected": all(reachable(graph, v) == everyone for v in graph.vertices),
    }


def to_edge_list(graph):
    return [(s, t, w) for s in graph.vertices for t, w in sorted(graph.adjacency[s].items())]


def to_adjacency_list(graph):
    return {s: [(t, graph.get_weight(s, t)) for t in graph.neighbors(s)] for s in graph.vertices}


def to_adjacency_matrix(graph):
    return [[1 if graph.has_edge(s, t) else 0 for t in graph.vertices] for s in graph.vertices]


def to_weight_matrix(graph):
    return [[0 if s == t else graph.get_weight(s, t) if graph.has_edge(s, t) else INF for t in graph.vertices] for s in graph.vertices]


def is_valid_walk(graph, vertices):
    return len(vertices) >= 1 and all(graph.has_edge(a, b) for a, b in zip(vertices, vertices[1:]))


def walk_weight(graph, vertices):
    if not is_valid_walk(graph, vertices):
        return None
    return sum(graph.get_weight(a, b) for a, b in zip(vertices, vertices[1:]))


def is_simple_path(vertices):
    return len(set(vertices)) == len(vertices)


def is_cycle(graph, vertices):
    inner = vertices[:-1]
    return len(vertices) >= 3 and vertices[0] == vertices[-1] and is_valid_walk(graph, vertices) and is_simple_path(inner)


def bfs(graph, start):
    order, seen, queue = [], {start}, deque([start])
    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for n in graph.neighbors(vertex):
            if n not in seen:
                seen.add(n)
                queue.append(n)
    return order


def dfs(graph, start, order=None):
    order = order if order is not None else []
    order.append(start)
    for n in graph.neighbors(start):
        if n not in order:
            dfs(graph, n, order)
    return order


def dijkstra(graph, start):
    distance = {v: INF for v in graph.vertices}
    parent = {v: None for v in graph.vertices}
    distance[start] = 0
    heap = [(0, start)]
    while heap:
        d, vertex = heapq.heappop(heap)
        if d > distance[vertex]:
            continue
        for n in graph.neighbors(vertex):
            nd = d + graph.get_weight(vertex, n)
            if nd < distance[n]:
                distance[n], parent[n] = nd, vertex
                heapq.heappush(heap, (nd, n))
    return distance, parent


def path_to(parent, target):
    path = [target]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    return path[::-1]


def floyd_warshall(graph):
    n = graph.vertex_count()
    dist = to_weight_matrix(graph)
    nxt = [[j if dist[i][j] != INF and i != j else (i if i == j else None) for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]
    return dist, nxt


def fw_route(graph, nxt, source, target):
    i, j = graph.vertices.index(source), graph.vertices.index(target)
    if nxt[i][j] is None:
        return None
    path = [i]
    while i != j:
        i = nxt[i][j]
        path.append(i)
    return [graph.vertices[k] for k in path]


def matrix_text(graph, matrix):
    head = "     " + "".join(f"{v:>4}" for v in graph.vertices)
    rows = [f"  {v:>2} " + "".join(f"{'∞' if x == INF else x:>4}" for x in row) for v, row in zip(graph.vertices, matrix)]
    return "\n".join([head] + rows)


def main():
    print("Stage 1. Properties")
    props = properties(build())
    for name, value in props.items():
        print(f"  {name:<19} {'yes' if value else 'no'}")
    print("  B→D and D→B are two different directed edges, not a multiple edge.")
    print("  Not strongly connected: A and G have no incoming edges, nothing can reach them.")

    graph = DirectedWeightedGraph()
    print("\nStage 2. Class operations")
    log = [graph.add_vertex(v) for v in OBJECTS]
    log += [graph.add_edge(*e) for e in EDGES]
    print(f"  {graph.vertex_count()} vertices and {graph.edge_count()} edges added")
    checks = [
        graph.add_edge("A", "B", 3),
        graph.add_edge("A", "A", 1),
        graph.add_edge("X", "A", 1),
        graph.add_edge("G", "A", -1),
        graph.add_edge("G", "A", "five"),
        graph.add_vertex("A"),
        graph.remove_edge("A", "E"),
    ]
    for ok, message in checks:
        print(f"  {'ok  ' if ok else 'fail'} {message}")
    after_remove = graph.edge_count()
    print("  edges after removing A→E:", after_remove)
    print("  " + graph.add_edge("A", "E", 15)[1], "-> edges:", graph.edge_count())
    temp = build()
    temp.remove_vertex("G")
    print(f"  remove_vertex(G) on a copy: {temp.vertex_count()} vertices, {temp.edge_count()} edges; original keeps {graph.vertex_count()}")

    print("\nStage 3. Representations")
    edge_list = to_edge_list(graph)
    print("  edge list:", edge_list)
    adjacency = to_adjacency_list(graph)
    print("  adjacency list:")
    for s, targets in adjacency.items():
        print(f"    {s}: " + ", ".join(f"{t}({w})" for t, w in targets))
    print("  adjacency matrix:")
    print(matrix_text(graph, to_adjacency_matrix(graph)))
    print("  weight matrix D(0):")
    print(matrix_text(graph, to_weight_matrix(graph)))
    print("  A missing edge is ∞, not 0: a real edge may have weight 0.")

    print("\nStage 4. Degrees")
    degrees = {}
    for v in graph.vertices:
        degrees[v] = (graph.out_degree(v), graph.in_degree(v))
        print(f"  {v}: out {degrees[v][0]} in {degrees[v][1]}  out-neighbours {graph.neighbors(v)}  in-neighbours {graph.predecessors(v)}")
    total_out = sum(d[0] for d in degrees.values())
    total_in = sum(d[1] for d in degrees.values())
    sources = [v for v, d in degrees.items() if d[1] == 0]
    sinks = [v for v, d in degrees.items() if d[0] == 0]
    print(f"  sum of out-degrees {total_out}, sum of in-degrees {total_in}, |E| = {graph.edge_count()}")
    print("  sources:", ", ".join(sources), " sinks:", ", ".join(sinks) or "none")

    print("\nStage 5. Walks, paths and cycles")
    walks = [list("ABCDEF"), list("BCDB"), list("ADE"), list("ABCB")]
    walk_results = []
    for w in walks:
        result = (is_valid_walk(graph, w), walk_weight(graph, w), is_simple_path(w), is_cycle(graph, w))
        walk_results.append(result)
        valid, weight, simple, cycle = result
        details = f"weight {weight}" if valid else "no such route: " + ", ".join(f"{a}→{b}" for a, b in zip(w, w[1:]) if not graph.has_edge(a, b)) + " missing"
        print(f"  {' → '.join(w):<22} walk {str(valid):<5} simple path {str(simple):<5} cycle {str(cycle):<5} {details}")

    print("\nStage 6. Traversals from A, neighbours in alphabetical order")
    bfs_order, dfs_order = bfs(graph, "A"), dfs(graph, "A")
    print("  BFS:", " → ".join(bfs_order))
    print("  DFS:", " → ".join(dfs_order))
    print("  G is not reached from A: it has no incoming edges.")

    print("\nStage 7. Dijkstra from A")
    distance, parent = dijkstra(graph, "A")
    for v in graph.vertices:
        print(f"  {v}: " + (f"{distance[v]:>2} min  {' → '.join(path_to(parent, v))}" if distance[v] < INF else "unreachable"))

    print("\nStage 8. Floyd–Warshall, all pairs")
    dist, nxt = floyd_warshall(graph)
    print(matrix_text(graph, dist))
    examples = {}
    for s, t in [("A", "F"), ("G", "B"), ("E", "D"), ("F", "A")]:
        route = fw_route(graph, nxt, s, t)
        examples[(s, t)] = (route, dist[graph.vertices.index(s)][graph.vertices.index(t)])
        print(f"  {s}→{t}: " + (f"{' → '.join(route)}, {examples[(s, t)][1]} min" if route else "no path"))
    negative = [graph.vertices[i] for i in range(graph.vertex_count()) if dist[i][i] < 0]
    print("  negative cycles:", negative or "none, all weights are positive")

    return graph, after_remove, props, edge_list, adjacency, degrees, (total_out, total_in, sources, sinks), walk_results, (bfs_order, dfs_order), distance, dist, examples


if __name__ == "__main__":
    graph, after_remove, props, edge_list, adjacency, degrees, sums, walks, orders, distance, dist, examples = main()
    assert after_remove == 12 and graph.edge_count() == 13 and graph.vertex_count() == 7
    assert props == {"directed": True, "weighted": True, "loops": False, "multiple edges": False, "cycles": True, "weakly connected": True, "strongly connected": False}
    assert len(edge_list) == 13 and adjacency["D"] == [("B", 4), ("E", 2), ("F", 6)]
    assert to_adjacency_matrix(graph) == [
        [0, 1, 1, 0, 1, 0, 0], [0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0], [0, 1, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 0], [0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0],
    ]
    assert to_weight_matrix(graph)[0] == [0, 3, 8, INF, 15, INF, INF] and to_weight_matrix(graph)[6] == [INF] * 5 + [2, 0]
    assert degrees == {"A": (3, 0), "B": (2, 2), "C": (2, 3), "D": (3, 2), "E": (1, 3), "F": (1, 3), "G": (1, 0)}
    assert sums == (13, 13, ["A", "G"], [])
    assert walks[0] == (True, 9, True, False)
    assert walks[1] == (True, 7, False, True)
    assert walks[2][0] is False and walks[3][0] is False
    assert distance == {"A": 0, "B": 3, "C": 5, "D": 6, "E": 8, "F": 9, "G": INF}
    for i, s in enumerate(graph.vertices):
        d, _ = dijkstra(graph, s)
        assert [d[t] for t in graph.vertices] == dist[i]
    assert examples[("A", "F")] == (["A", "B", "C", "D", "E", "F"], 9)
    assert examples[("F", "A")] == (None, INF)
    print("\nchecks passed")
