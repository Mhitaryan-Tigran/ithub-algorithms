V = ["A", "B", "C", "D", "E"]
E = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "E")]


class AdjacencyListGraph:
    def __init__(self):
        self.adjacency = {}

    def add_vertex(self, vertex):
        if vertex in self.adjacency:
            return False
        self.adjacency[vertex] = []
        return True

    def add_edge(self, u, v):
        if u not in self.adjacency or v not in self.adjacency or u == v or self.has_edge(u, v):
            return False
        self.adjacency[u].append(v)
        self.adjacency[v].append(u)
        return True

    def has_edge(self, u, v):
        return u in self.adjacency and v in self.adjacency[u]

    def neighbors(self, vertex):
        return list(self.adjacency[vertex])

    def stored_items(self):
        return sum(len(n) for n in self.adjacency.values())

    def show(self):
        return [f"{v}: {', '.join(n)}" for v, n in self.adjacency.items()]


class AdjacencyMatrixGraph:
    def __init__(self):
        self.vertices = []
        self.index = {}
        self.matrix = []

    def add_vertex(self, vertex):
        if vertex in self.index:
            return False
        self.index[vertex] = len(self.vertices)
        self.vertices.append(vertex)
        for row in self.matrix:
            row.append(0)
        self.matrix.append([0] * len(self.vertices))
        return True

    def add_edge(self, u, v):
        if u not in self.index or v not in self.index or u == v or self.has_edge(u, v):
            return False
        i, j = self.index[u], self.index[v]
        self.matrix[i][j] = self.matrix[j][i] = 1
        return True

    def has_edge(self, u, v):
        return u in self.index and v in self.index and self.matrix[self.index[u]][self.index[v]] == 1

    def neighbors(self, vertex):
        row = self.matrix[self.index[vertex]]
        return [self.vertices[j] for j, bit in enumerate(row) if bit]

    def stored_items(self):
        return len(self.vertices) ** 2

    def show(self):
        lines = ["   " + "  ".join(self.vertices)]
        lines += [f"{v}  " + "  ".join(map(str, row)) for v, row in zip(self.vertices, self.matrix)]
        return lines


if __name__ == "__main__":
    graphs = [AdjacencyListGraph(), AdjacencyMatrixGraph()]
    for graph in graphs:
        for v in V:
            graph.add_vertex(v)
        for u, v in E:
            graph.add_edge(u, v)
    by_list, by_matrix = graphs
    print("1. Adjacency list (dict):")
    print("\n".join("   " + line for line in by_list.show()))
    print("2. Adjacency matrix (2D list):")
    print("\n".join("   " + line for line in by_matrix.show()))
    print("has_edge(B, D):", by_list.has_edge("B", "D"), by_matrix.has_edge("B", "D"))
    print("has_edge(A, E):", by_list.has_edge("A", "E"), by_matrix.has_edge("A", "E"))
    print("neighbors(C):", by_list.neighbors("C"), by_matrix.neighbors("C"))
    print("duplicate edge A-B accepted:", by_list.add_edge("A", "B"), by_matrix.add_edge("A", "B"))
    print(f"memory: list stores {by_list.stored_items()} neighbour entries (2|E|) plus {len(V)} keys, O(V + E);")
    print(f"        matrix stores {by_matrix.stored_items()} cells (|V|^2), O(V^2), of them only {2 * len(E)} are ones.")
    print("        For a sparse graph like this the list is smaller; the matrix answers has_edge in O(1).")

    for u in V:
        assert sorted(by_list.neighbors(u)) == by_matrix.neighbors(u)
        for v in V:
            assert by_list.has_edge(u, v) == by_matrix.has_edge(u, v)
    assert by_list.stored_items() == 10 and by_matrix.stored_items() == 25
    print("checks passed")
