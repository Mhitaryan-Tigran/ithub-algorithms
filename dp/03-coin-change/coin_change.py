from itertools import combinations_with_replacement

INF = float("inf")


def min_banknotes(notes, amount):
    best = [0] + [INF] * amount
    last = [None] * (amount + 1)
    for s in range(1, amount + 1):
        for note in notes:
            if note <= s and best[s - note] + 1 < best[s]:
                best[s], last[s] = best[s - note] + 1, note
    if best[amount] == INF:
        return None
    result = []
    while amount:
        result.append(last[amount])
        amount -= last[amount]
    return sorted(result, reverse=True)


def greedy(notes, amount):
    result = []
    for note in sorted(notes, reverse=True):
        while amount >= note:
            result.append(note)
            amount -= note
    return result if amount == 0 else None


def brute_force(notes, amount):
    for count in range(0, amount // min(notes) + 1):
        for combo in combinations_with_replacement(notes, count):
            if sum(combo) == amount:
                return count
    return None


def show(result):
    return " + ".join(map(str, result)) + f" ({len(result)} notes)" if result else "impossible"


if __name__ == "__main__":
    print("best[s] = min over notes b <= s of best[s - b] + 1, best[0] = 0; last[s] remembers the note to restore the answer")
    cases = [([10, 60, 100], 120), ([60, 100], 120), ([60, 100], 160), ([60, 100], 110), ([50, 100, 200, 500, 1000, 2000, 5000], 3850)]
    for notes, amount in cases:
        print(f"  notes {notes}, N = {amount}:")
        print(f"    DP:     {show(min_banknotes(notes, amount))}")
        print(f"    greedy: {show(greedy(notes, amount))}")

    assert min_banknotes([10, 60, 100], 120) == [60, 60] and greedy([10, 60, 100], 120) == [100, 10, 10]
    assert min_banknotes([60, 100], 120) == [60, 60] and greedy([60, 100], 120) is None
    assert min_banknotes([60, 100], 110) is None
    for notes in ([3, 7], [1, 5, 6, 9], [4, 10, 25]):
        for amount in range(1, 60):
            dp = min_banknotes(notes, amount)
            assert (len(dp) if dp else None) == brute_force(notes, amount)
            assert dp is None or sum(dp) == amount
    print("checks passed")
