from collections import deque

GRAPH = {
    "A": ["B", "C"],
    "B": ["A", "C", "D"],
    "C": ["A", "B", "E"],
    "D": ["B"],
    "E": ["C"],
}


def bfs(graph, start):
    order, visited, queue = [], {start}, deque([start])
    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for neighbour in graph[vertex]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    return order


def dfs(graph, start, visited=None):
    visited = visited if visited is not None else []
    visited.append(start)
    for neighbour in graph[start]:
        if neighbour not in visited:
            dfs(graph, neighbour, visited)
    return visited


def dfs_stack(graph, start):
    order, stack = [], [start]
    while stack:
        vertex = stack.pop()
        if vertex in order:
            continue
        order.append(vertex)
        stack.extend(reversed([n for n in graph[vertex] if n not in order]))
    return order


if __name__ == "__main__":
    print("BFS:", " → ".join(bfs(GRAPH, "A")))
    print("DFS:", " → ".join(dfs(GRAPH, "A")))
    print("DFS with an explicit stack:", " → ".join(dfs_stack(GRAPH, "A")))
    print()
    print("BFS takes vertices from a queue (FIFO): first all neighbours of A, then their neighbours,")
    print("so it moves in layers by distance and finds shortest paths in an unweighted graph.")
    print("DFS goes as deep as it can along one branch (recursion or a LIFO stack) and backtracks")
    print("only at a dead end: A → B → C → E, back to B, then D. It is used for cycles, components, topological sort.")
    print("Both visit every vertex and edge once: O(V + E).")

    assert bfs(GRAPH, "A") == ["A", "B", "C", "D", "E"]
    assert dfs(GRAPH, "A") == ["A", "B", "C", "E", "D"] == dfs_stack(GRAPH, "A")
    print("checks passed")
