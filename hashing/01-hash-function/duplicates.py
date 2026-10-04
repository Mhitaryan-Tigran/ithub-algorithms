import random


def duplicates_naive(a):
    return any(a[i] == a[j] for i in range(len(a)) for j in range(i + 1, len(a)))


def duplicates_sorted(a):
    b = sorted(a)
    return any(b[i] == b[i + 1] for i in range(len(b) - 1))


def duplicates_hashing(a):
    seen = set()
    for x in a:
        if x in seen:
            return True
        seen.add(x)
    return False


def duplicates_counting(a, k):
    seen = [False] * (k + 1)
    for x in a:
        if seen[x]:
            return True
        seen[x] = True
    return False


def h(k):
    return (11 * k + 4) % 9


def chaining(keys, m=9):
    table = [[] for _ in range(m)]
    for key in keys:
        table[h(key)].append(key)
    return table


def linear_probing(keys, m=9):
    table, steps = [None] * m, []
    for key in keys:
        home = h(key)
        for i in range(m):
            index = (home + i) % m
            if table[index] is None:
                table[index] = key
                steps.append((key, home, index, i))
                break
    return table, steps


if __name__ == "__main__":
    random.seed(5)
    for _ in range(300):
        k = random.randint(1, 60)
        a = [random.randint(1, k) for _ in range(random.randint(0, k))]
        answer = len(set(a)) != len(a)
        assert duplicates_naive(a) == duplicates_sorted(a) == duplicates_hashing(a) == duplicates_counting(a, k) == answer
    print("DUPLICATES: four algorithms agree on 300 random arrays")
    print("DUPLICATES([3, 1, 4, 1, 5]) =", duplicates_counting([3, 1, 4, 1, 5], 5))

    A = [67, 13, 49, 24, 40, 33, 58]
    print("\nh(k) = (11k + 4) mod 9")
    for key in A:
        print(f"  h({key}) = {11 * key + 4} mod 9 = {h(key)}")
    print("\nclosed addressing, separate chaining:")
    for index, chain in enumerate(chaining(A)):
        print(f"  {index}: {' -> '.join(map(str, chain)) or '-'}")
    table, steps = linear_probing(A)
    print("\nopen addressing, linear probing h(k, i) = (h(k) + i) mod 9:")
    for key, home, index, i in steps:
        print(f"  {key}: home {home}, placed at {index} after {i} collisions")
    for index, key in enumerate(table):
        print(f"  {index}: {key if key is not None else '-'}")

    assert chaining(A)[3] == [67, 13, 49, 40, 58] and chaining(A)[7] == [24, 33]
    assert table == [58, None, None, 67, 13, 49, 40, 24, 33]
    print("checks passed")
