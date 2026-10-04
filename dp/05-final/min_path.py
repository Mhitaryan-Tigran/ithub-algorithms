import random

FIELD = [
    [3, 7, 2, 9, 4],
    [8, 1, 6, 3, 5],
    [2, 9, 8, 1, 8],
    [6, 3, 7, 9, 6],
    [4, 8, 1, 5, 2],
]


def min_path(field):
    n, m = len(field), len(field[0])
    cost = [[0] * m for _ in range(n)]
    came = [[None] * m for _ in range(n)]
    for a in range(n):
        for b in range(m):
            options = [(cost[x][y], (x, y)) for x, y in ((a, b - 1), (a - 1, b), (a - 1, b - 1)) if x >= 0 and y >= 0]
            best, cell = min(options) if options else (0, None)
            cost[a][b] = best + field[a][b]
            came[a][b] = cell
    route, cell = [], (n - 1, m - 1)
    while cell:
        route.append(cell)
        cell = came[cell[0]][cell[1]]
    return cost[n - 1][m - 1], route[::-1], cost


def brute_force(field):
    n, m = len(field), len(field[0])

    def go(a, b):
        if (a, b) == (n - 1, m - 1):
            return field[a][b]
        steps = [(a + da, b + db) for da, db in ((0, 1), (1, 0), (1, 1)) if a + da < n and b + db < m]
        return field[a][b] + min(go(x, y) for x, y in steps)

    return go(0, 0)


def draw(field, route):
    on_route = set(route)
    return "\n".join("  " + " ".join(f"[{x}]" if (a, b) in on_route else f" {x} " for b, x in enumerate(row)) for a, row in enumerate(field))


if __name__ == "__main__":
    weight, route, cost = min_path(FIELD)
    print("Task 3. Minimum-weight route from the top-left to the bottom-right cell, moves right, down, diagonal")
    print("cost[a][b] = field[a][b] + min(cost[a][b-1], cost[a-1][b], cost[a-1][b-1]); came[a][b] stores the chosen neighbour")
    print("field, route in brackets:")
    print(draw(FIELD, route))
    print("cost table:")
    print("\n".join("  " + " ".join(f"{x:>3}" for x in row) for row in cost))
    print("route:", " → ".join(f"({a},{b})" for a, b in route))
    print("weight:", weight, "=", " + ".join(str(FIELD[a][b]) for a, b in route))
    print("time O(n·m), memory O(n·m) for the route; the weight alone needs only one row, O(m)")

    assert weight == brute_force(FIELD) == sum(FIELD[a][b] for a, b in route)
    assert route[0] == (0, 0) and route[-1] == (4, 4)
    assert all(0 <= x2 - x1 <= 1 and 0 <= y2 - y1 <= 1 and (x1, y1) != (x2, y2) for (x1, y1), (x2, y2) in zip(route, route[1:]))
    random.seed(15)
    for _ in range(200):
        n, m = random.randint(1, 6), random.randint(1, 6)
        field = [[random.randint(1, 9) for _ in range(m)] for _ in range(n)]
        w, r, _ = min_path(field)
        assert w == brute_force(field) == sum(field[a][b] for a, b in r)
    print("checks passed")
