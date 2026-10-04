from math import comb


def king_routes(n, m, diagonal=False, forbidden=()):
    blocked = set(forbidden)
    w = [[0] * m for _ in range(n)]
    for a in range(n):
        for b in range(m):
            if (a, b) in blocked:
                continue
            if a == 0 and b == 0:
                w[a][b] = 1
                continue
            w[a][b] = (w[a][b - 1] if b else 0) + (w[a - 1][b] if a else 0)
            if diagonal and a and b:
                w[a][b] += w[a - 1][b - 1]
    return w[n - 1][m - 1], w


def brute_force(n, m, diagonal=False, forbidden=()):
    blocked = set(forbidden)
    moves = [(0, 1), (1, 0)] + ([(1, 1)] if diagonal else [])

    def go(a, b):
        if (a, b) in blocked or a >= n or b >= m:
            return 0
        if (a, b) == (n - 1, m - 1):
            return 1
        return sum(go(a + da, b + db) for da, db in moves)

    return go(0, 0)


def board(w, forbidden=()):
    return "\n".join("  " + " ".join("  X" if (a, b) in forbidden else f"{x:>3}" for b, x in enumerate(row)) for a, row in enumerate(w))


if __name__ == "__main__":
    forbidden = {(1, 1), (2, 3), (3, 0)}
    print("Variant 1. Down or right on 5x5: W(a, b) = W(a, b - 1) + W(a - 1, b)")
    total1, w1 = king_routes(5, 5)
    print(board(w1))
    print("  routes:", total1, "= C(8, 4)")
    print("\nVariant 2. Down, right or diagonally on 5x5: + W(a - 1, b - 1)")
    total2, w2 = king_routes(5, 5, diagonal=True)
    print(board(w2))
    print("  routes:", total2)
    print("\nVariant 3. Down or right on 5x5, X cells are forbidden, W = 0 there")
    total3, w3 = king_routes(5, 5, forbidden=forbidden)
    print(board(w3, forbidden))
    print("  routes:", total3)

    assert total1 == comb(8, 4) == 70 and total2 == 321
    for n in range(1, 6):
        for m in range(1, 6):
            assert king_routes(n, m)[0] == comb(n + m - 2, n - 1)
            for diagonal in (False, True):
                cells = {(a, b) for a in range(n) for b in range(m) if (a * 3 + b) % 4 == 1 and (a, b) not in {(0, 0), (n - 1, m - 1)}}
                assert king_routes(n, m, diagonal, cells)[0] == brute_force(n, m, diagonal, cells)
    print("checks passed")
