from collections import deque

GRAPH = {
    "A": ["C"],
    "B": ["C", "D"],
    "C": ["E"],
    "D": ["E"],
    "E": ["F"],
    "F": [],
}


def topological_sort(graph):
    in_degree = {v: 0 for v in graph}
    for targets in graph.values():
        for t in targets:
            in_degree[t] += 1
    queue = deque(sorted(v for v, d in in_degree.items() if d == 0))
    order = []
    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for t in graph[vertex]:
            in_degree[t] -= 1
            if in_degree[t] == 0:
                queue.append(t)
    if len(order) < len(graph):
        return order, sorted(v for v in graph if v not in order)
    return order, []


def find_cycle(graph, vertices):
    for start in vertices:
        path, stack = [start], [iter(graph[start])]
        while stack:
            nxt = next(stack[-1], None)
            if nxt is None:
                stack.pop()
                path.pop()
            elif nxt == start:
                return path + [start]
            elif nxt not in path and nxt in vertices:
                path.append(nxt)
                stack.append(iter(graph[nxt]))
    return None


if __name__ == "__main__":
    order, blocked = topological_sort(GRAPH)
    print("Topological order:", " → ".join(order))

    cyclic = {v: list(t) for v, t in GRAPH.items()}
    cyclic["F"].append("B")
    order2, blocked2 = topological_sort(cyclic)
    cycle = find_cycle(cyclic, blocked2)
    print("\nWith F → B added:")
    print("  processed:", " → ".join(order2))
    print("  never reached in-degree 0:", ", ".join(blocked2))
    print("  cycle:", " → ".join(cycle))
    print("  A topological order exists only for a DAG. After F → B the vertices B, C, E, F wait for each other")
    print("  in a loop, their in-degree never drops to 0, so Kahn's algorithm stops with fewer vertices than the graph")
    print("  has and reports the cycle. D is also stuck because it depends on B.")

    assert order == ["A", "B", "C", "D", "E", "F"] and not blocked
    assert order2 == ["A"] and blocked2 == ["B", "C", "D", "E", "F"]
    assert cycle == ["B", "C", "E", "F", "B"]
    print("checks passed")
