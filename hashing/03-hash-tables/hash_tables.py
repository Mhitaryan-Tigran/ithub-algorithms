import random
from collections import Counter

CANDIDATES = {
    "i) random(0, 3000)": lambda x: random.randint(0, 3000),
    "ii) x mod 1301": lambda x: x % 1301,
    "iii) len(x)": lambda x: len(str(x)),
    "iv) digit sum": lambda x: sum(map(int, str(x))),
    "v) x0 + 5x1 + 25x2 + 125x3": lambda x: sum(int(d) * 5 ** i for i, d in enumerate(str(x))),
}


def quality(function):
    keys = range(1000, 10000)
    first = [function(x) for x in keys]
    deterministic = first == [function(x) for x in keys]
    counts = Counter(first)
    return deterministic, len(counts), max(counts.values()), len(keys) / len(counts)


def chaining(keys, m=9):
    table = [[] for _ in range(m)]
    for key in keys:
        table[key % m].append(key)
    return table


def linear_probing(keys, m=9):
    table = [None] * m
    for key in keys:
        i = 0
        while table[(key + i) % m] is not None:
            i += 1
        table[(key + i) % m] = key
    return table


def chain_costs(chain_lengths, sorted_chains):
    miss = []
    for length in chain_lengths:
        for gap in range(length + 1):
            miss.append(min(gap + 1, length) if sorted_chains else length)
    return sum(miss) / len(miss)


if __name__ == "__main__":
    random.seed(0)
    print("Task 1. Four-digit keys 1000..9999 (9000 keys)")
    print(f"  {'function':<28} {'same result twice':<18} {'distinct values':<16} {'largest bucket':<15} keys per value")
    report = {}
    for name, function in CANDIDATES.items():
        report[name] = quality(function)
        deterministic, distinct, largest, average = report[name]
        print(f"  {name:<28} {str(deterministic):<18} {distinct:<16} {largest:<15} {average:.1f}")

    keys = [5, 28, 19, 15, 20, 33, 12, 17, 10]
    print("\nTask 2. Keys", keys, "with h(k) = k mod 9")
    print("  addresses:", [(k, k % 9) for k in keys])
    print("  i) closed addressing, separate chaining:")
    for index, chain in enumerate(chaining(keys)):
        print(f"     {index}: {' -> '.join(map(str, chain)) or '-'}")
    print("  ii) open addressing, linear probing:")
    table = linear_probing(keys)
    for index, key in enumerate(table):
        print(f"     {index}: {key if key is not None else '-'}")

    lengths = [6] * 1000
    print("\nTask 3. Unsuccessful search in a chain of 6 keys, averaged over all positions of the missing key")
    print(f"  unsorted chain: {chain_costs(lengths, False):.2f} comparisons, sorted chain: {chain_costs(lengths, True):.2f}")

    assert report["ii) x mod 1301"][:3] == (True, 1301, 7)
    assert report["iii) len(x)"][1] == 1
    assert report["iv) digit sum"][1] == 36
    assert not report["i) random(0, 3000)"][0]
    assert chaining(keys)[1] == [28, 19, 10] and chaining(keys)[6] == [15, 33]
    assert table == [10, 28, 19, 20, 12, 5, 15, 33, 17]
    print("checks passed")
