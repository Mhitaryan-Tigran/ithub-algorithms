from itertools import product


def count_routes(n):
    if n < 1:
        raise ValueError("n must be at least 1")
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + (dp[i - 2] if i >= 3 else 0)
    return dp[n], dp


def count_routes_o1(n):
    previous, current = 0, 1
    for _ in range(n - 1):
        previous, current = current, current + previous
    return current


def brute_force(n):
    total = 0
    for steps in range(n):
        for jumps in product((1, 2), repeat=steps):
            total += sum(jumps) == n - 1
    return total


if __name__ == "__main__":
    answer, dp = count_routes(7)
    print("Points 1..n, a move goes to the next point or jumps over one.")
    print("dp[1] = 1 (already there), dp[2] = dp[1] = 1, dp[i] = dp[i-1] + dp[i-2] for i >= 3")
    print("dp:", {i: dp[i] for i in range(1, 8)})
    print(f"n = 7: {answer} routes")
    print("O(1) memory version:", count_routes_o1(7))
    print("n = 50:", count_routes_o1(50))

    assert answer == 13 and count_routes_o1(7) == 13
    for n in range(1, 16):
        assert count_routes(n)[0] == count_routes_o1(n) == brute_force(n)
    print("checks passed")
