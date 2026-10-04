import random


class CuckooHashTable:
    def __init__(self, capacity=11, max_kicks=32):
        self.capacity = capacity
        self.max_kicks = max_kicks
        self.tables = [[None] * capacity, [None] * capacity]
        self.size = 0
        self.rehashes = 0

    def _index(self, which, key):
        return key % self.capacity if which == 0 else (key // self.capacity) % self.capacity

    def search(self, key):
        for which in (0, 1):
            if self.tables[which][self._index(which, key)] == key:
                return which, self._index(which, key)
        return None

    def insert(self, key, log=None):
        if self.search(key):
            return False
        which = 0
        for _ in range(self.max_kicks):
            index = self._index(which, key)
            key, self.tables[which][index] = self.tables[which][index], key
            if log is not None:
                log.append((which, index))
            if key is None:
                self.size += 1
                return True
            which = 1 - which
        self._grow(key)
        return True

    def _grow(self, pending):
        keys = [k for table in self.tables for k in table if k is not None] + [pending]
        self.capacity = self.capacity * 2 + 1
        self.tables = [[None] * self.capacity, [None] * self.capacity]
        self.size = 0
        self.rehashes += 1
        for key in keys:
            self.insert(key)

    def delete(self, key):
        found = self.search(key)
        if not found:
            return False
        which, index = found
        self.tables[which][index] = None
        self.size -= 1
        return True


class RobinHoodHashTable:
    def __init__(self, capacity=11):
        self.capacity = capacity
        self.keys = [None] * capacity
        self.distances = [0] * capacity
        self.size = 0

    def insert(self, key):
        if self.search(key)[0]:
            return False
        if self.size == self.capacity:
            raise OverflowError("table is full")
        index, distance = key % self.capacity, 0
        while True:
            if self.keys[index] is None:
                self.keys[index], self.distances[index] = key, distance
                self.size += 1
                return True
            if self.distances[index] < distance:
                key, self.keys[index] = self.keys[index], key
                distance, self.distances[index] = self.distances[index], distance
            index, distance = (index + 1) % self.capacity, distance + 1

    def search(self, key):
        index, distance = key % self.capacity, 0
        while self.keys[index] is not None and distance <= self.distances[index]:
            if self.keys[index] == key:
                return True, distance + 1
            index, distance = (index + 1) % self.capacity, distance + 1
        return False, distance + 1

    def delete(self, key):
        index = key % self.capacity
        for _ in range(self.capacity):
            if self.keys[index] is None:
                return False
            if self.keys[index] == key:
                break
            index = (index + 1) % self.capacity
        else:
            return False
        nxt = (index + 1) % self.capacity
        while self.keys[nxt] is not None and self.distances[nxt] > 0:
            self.keys[index], self.distances[index] = self.keys[nxt], self.distances[nxt] - 1
            index, nxt = nxt, (nxt + 1) % self.capacity
        self.keys[index], self.distances[index] = None, 0
        self.size -= 1
        return True


class LinearProbing:
    def __init__(self, capacity):
        self.capacity = capacity
        self.keys = [None] * capacity

    def insert(self, key):
        index = key % self.capacity
        while self.keys[index] is not None:
            index = (index + 1) % self.capacity
        self.keys[index] = key

    def probes(self, key):
        index, count = key % self.capacity, 1
        while self.keys[index] is not None and self.keys[index] != key:
            index, count = (index + 1) % self.capacity, count + 1
        return count


if __name__ == "__main__":
    print("1. Cuckoo hashing: two tables, h1(k) = k mod 11, h2(k) = (k div 11) mod 11")
    cuckoo = CuckooHashTable()
    for key in [20, 50, 53, 75, 100, 67, 105, 3, 36, 39]:
        log = []
        cuckoo.insert(key, log)
        moves = " -> ".join(f"T{w + 1}[{i}]" for w, i in log)
        print(f"   insert {key:>3}: {moves}")
    for which in (0, 1):
        print(f"   T{which + 1}:", ["-" if k is None else k for k in cuckoo.tables[which]])
    print("   search 105 ->", cuckoo.search(105), "(at most two cells are checked)")

    print("\n2. Robin Hood hashing: a key far from home takes the cell of a key closer to its home")
    robin = RobinHoodHashTable()
    for key in [22, 33, 44, 1, 2, 12, 23, 5]:
        robin.insert(key)
    print("   keys:     ", ["-" if k is None else k for k in robin.keys])
    print("   distances:", robin.distances)
    print("   search 23:", robin.search(23), "search 34 (absent):", robin.search(34))
    robin.delete(33)
    print("   after deleting 33 with backward shift:", ["-" if k is None else k for k in robin.keys])

    random.seed(4)
    capacity = 101
    keys = random.sample(range(1, 100000), 85)
    linear, rh = LinearProbing(capacity), RobinHoodHashTable(capacity)
    for key in keys:
        linear.insert(key)
        rh.insert(key)
    linear_costs = [linear.probes(k) for k in keys]
    rh_costs = [rh.search(k)[1] for k in keys]
    print("\n3. 85 random keys in 101 cells, successful search:")
    print(f"   linear probing: average {sum(linear_costs) / 85:.2f}, worst {max(linear_costs)}")
    print(f"   Robin Hood:     average {sum(rh_costs) / 85:.2f}, worst {max(rh_costs)}")

    assert all(cuckoo.search(k) for k in [20, 50, 53, 75, 100, 67, 105, 3, 36, 39])
    assert robin.search(23)[0] and not robin.search(33)[0] and all(robin.search(k)[0] for k in [22, 44, 1, 2, 12, 23, 5])
    assert max(rh_costs) <= max(linear_costs)
    for _ in range(50):
        c, r, alive = CuckooHashTable(7), RobinHoodHashTable(211), set()
        for _ in range(150):
            key = random.randint(1, 500)
            if random.random() < 0.7:
                c.insert(key)
                r.insert(key)
                alive.add(key)
            else:
                assert c.delete(key) == r.delete(key) == (key in alive)
                alive.discard(key)
        assert all(c.search(k) and r.search(k)[0] for k in alive)
        assert c.size == r.size == len(alive)
    print("checks passed")
