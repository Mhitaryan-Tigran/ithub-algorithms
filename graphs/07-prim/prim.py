import heapq

EDGES = [("A", "B", 4), ("A", "C", 2), ("B", "C", 1), ("B", "D", 5), ("C", "D", 8), ("C", "E", 10), ("D", "E", 2), ("B", "E", 6)]


def to_graph(edges):
    graph = {}
    for u, v, w in edges:
        graph.setdefault(u, []).append((v, w))
        graph.setdefault(v, []).append((u, w))
    return graph


def prim(graph, start):
    visited = {start}
    heap = [(w, start, v) for v, w in graph[start]]
    heapq.heapify(heap)
    tree = []
    while heap and len(visited) < len(graph):
        weight, u, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        tree.append((u, v, weight))
        for nxt, w in graph[v]:
            if nxt not in visited:
                heapq.heappush(heap, (w, v, nxt))
    connected = len(visited) == len(graph)
    return tree, sum(w for _, _, w in tree), connected


if __name__ == "__main__":
    tree, total, connected = prim(to_graph(EDGES), "A")
    print("Prim from A, edges in the order they were added:")
    for u, v, w in tree:
        print(f"  {u}{v}={w}")
    print("total weight:", total, " edges:", len(tree), " connected:", connected)
    print("The heap always gives the lightest edge leaving the tree; an edge to an already visited vertex is skipped,")
    print("so a cycle can never appear.")

    assert [(u + v, w) for u, v, w in tree] == [("AC", 2), ("CB", 1), ("BD", 5), ("DE", 2)]
    assert total == 10 and len(tree) == 4 and connected
    split = to_graph(EDGES + [("X", "Y", 3)])
    assert not prim(split, "A")[2]
    print("checks passed")
