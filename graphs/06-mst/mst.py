GRAPH = [("A", "B", 4), ("A", "C", 2), ("B", "C", 1), ("B", "D", 5), ("C", "D", 8), ("C", "E", 10), ("D", "E", 2), ("B", "E", 6)]


def minimum_spanning_tree(graph):
    vertices = sorted({v for u, w, _ in graph for v in (u, w)})
    component = {v: v for v in vertices}
    chosen, log = [], []
    for u, v, weight in sorted(graph, key=lambda edge: edge[2]):
        if component[u] == component[v]:
            log.append(f"skip {u}{v}={weight}: {u} and {v} are already in one component, the edge would close a cycle")
            continue
        old, new = component[v], component[u]
        for vertex in vertices:
            if component[vertex] == old:
                component[vertex] = new
        chosen.append((u, v, weight))
        log.append(f"take {u}{v}={weight}")
        if len(chosen) == len(vertices) - 1:
            break
    connected = len(set(component.values())) == 1
    return chosen, sum(w for _, _, w in chosen), connected, log


if __name__ == "__main__":
    edges, total, connected, log = minimum_spanning_tree(GRAPH)
    print("Kruskal: edges sorted by weight, each vertex keeps the label of its component")
    for line in log:
        print("  " + line)
    print("MST edges:", ", ".join(f"{u}{v}={w}" for u, v, w in edges))
    print("total weight:", total, " number of edges:", len(edges), "= |V| - 1")
    print("graph connected:", connected)
    print("Cycles are prevented by component labels: an edge is taken only if its ends have different labels,")
    print("after that the two components are merged under one label.")

    assert [(u + v, w) for u, v, w in edges] == [("BC", 1), ("AC", 2), ("DE", 2), ("BD", 5)]
    assert total == 10 and len(edges) == 4 and connected
    assert not minimum_spanning_tree(GRAPH + [("X", "Y", 1)])[2]
    print("checks passed")
