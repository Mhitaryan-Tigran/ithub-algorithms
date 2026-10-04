from itertools import product


def count_strings(n):
    if n < 1:
        raise ValueError("n must be at least 1")
    k = [0, 2, 3]
    for i in range(3, n + 1):
        k.append(k[i - 1] + k[i - 2])
    return k[n], k[1:n + 1]


def brute_force(n):
    return sum("11" not in "".join(bits) for bits in product("01", repeat=n))


def examples(n):
    return ["".join(bits) for bits in product("01", repeat=n) if "11" not in "".join(bits)]


if __name__ == "__main__":
    print("K1 = 2 (0, 1), K2 = 3 (00, 01, 10), Kn = K(n-1) + K(n-2):")
    print("  ends with 0 -> any valid string of length n-1 before it")
    print("  ends with 1 -> the previous symbol must be 0, any valid string of length n-2 before them")
    for n in (1, 2, 3, 4, 5, 10):
        print(f"  n = {n:>2}: {count_strings(n)[0]}")
    print("  length 4:", ", ".join(examples(4)))
    print("  n = 64:", count_strings(64)[0], "- full search over 2^64 strings is impossible, DP takes 64 steps")

    for n in range(1, 18):
        assert count_strings(n)[0] == brute_force(n) == len(examples(n))
    assert count_strings(64)[0] == 27777890035288
    print("checks passed")
