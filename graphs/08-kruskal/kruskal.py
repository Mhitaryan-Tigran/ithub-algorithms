EDGES = [("A", "B", 4), ("A", "C", 2), ("B", "C", 1), ("B", "D", 5), ("C", "D", 8), ("C", "E", 10), ("D", "E", 2), ("B", "E", 6)]


class UnionFind:
    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.rank = {x: 0 for x in items}

    def find(self, vertex):
        root = vertex
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[vertex] != root:
            self.parent[vertex], vertex = root, self.parent[vertex]
        return root

    def union(self, u, v):
        a, b = self.find(u), self.find(v)
        if a == b:
            return False
        if self.rank[a] < self.rank[b]:
            a, b = b, a
        self.parent[b] = a
        if self.rank[a] == self.rank[b]:
            self.rank[a] += 1
        return True


def kruskal(graph):
    vertices = sorted({v for u, w, _ in graph for v in (u, w)})
    sets = UnionFind(vertices)
    tree, skipped = [], []
    for u, v, w in sorted(graph, key=lambda e: e[2]):
        if len(tree) == len(vertices) - 1:
            break
        if sets.union(u, v):
            tree.append((u, v, w))
        else:
            skipped.append((u, v, w))
    connected = len(tree) == len(vertices) - 1
    return tree, sum(w for _, _, w in tree), connected, skipped


if __name__ == "__main__":
    tree, total, connected, skipped = kruskal(EDGES)
    print("Kruskal with Union-Find (path compression + union by rank)")
    print("MST:", ", ".join(f"{u}{v}={w}" for u, v, w in tree))
    print("skipped because of a cycle:", ", ".join(f"{u}{v}={w}" for u, v, w in skipped))
    print("total weight:", total, " edges:", len(tree), " connected:", connected)

    assert [(u + v, w) for u, v, w in tree] == [("BC", 1), ("AC", 2), ("DE", 2), ("BD", 5)]
    assert skipped == [("A", "B", 4)] and total == 10 and connected
    assert not kruskal(EDGES + [("X", "Y", 1)])[2]
    print("checks passed")
