import random
from dataclasses import dataclass, fields

EMPTY = object()
DELETED = object()
MAX_LOAD = 0.70

SOURCE = [
    (26, "Проектор", "A-201", "Свободно"),
    (39, "3D-принтер", "A-305", "Обслуживание"),
    (52, "Осциллограф", "B-214", "Свободно"),
    (14, "Ноутбук", "A-108", "Выдано"),
    (27, "Маршрутизатор", "B-214", "Свободно"),
    (40, "Набор микроконтроллеров", "A-305", "Выдано"),
    (16, "Веб-камера", "A-108", "Свободно"),
    (29, "Графический планшет", "A-201", "Обслуживание"),
    (42, "Лазерный принтер", "A-108", "Свободно"),
]


@dataclass(eq=False)
class Equipment:
    id: int
    name: str
    room: str
    status: str

    def __post_init__(self):
        if not isinstance(self.id, int) or isinstance(self.id, bool) or self.id <= 0:
            raise ValueError(f"inventory number must be a positive integer, got {self.id!r}")

    def __eq__(self, other):
        return isinstance(other, Equipment) and self.id == other.id


def division_hash(key, capacity):
    return key % capacity


def mixed_hash(key, capacity):
    return ((7 * key + 3) % 101) % capacity


def analyze_distribution(keys, capacity, hash_function):
    counts = [0] * capacity
    addresses, collisions = [], 0
    for key in keys:
        address = hash_function(key, capacity)
        collisions += counts[address] > 0
        counts[address] += 1
        addresses.append((key, address))
    occupied = sum(1 for c in counts if c)
    return {
        "addresses": addresses,
        "occupied": occupied,
        "empty": capacity - occupied,
        "collisions": collisions,
        "max_in_bucket": max(counts),
        "load_factor": len(keys) / capacity,
    }


def is_prime(number):
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def next_prime(number):
    while not is_prime(number):
        number += 1
    return number


def change(record, room, status):
    if room is not None:
        record.room = room
    if status is not None:
        record.status = status
    return record


class ChainNode:
    def __init__(self, equipment):
        self.data = equipment
        self.next = None


class ChainedHashTable:
    def __init__(self, capacity=13, hash_function=division_hash):
        self.capacity = capacity
        self.hash_function = hash_function
        self.buckets = [None] * capacity
        self.size = 0

    def _index(self, key):
        return self.hash_function(key, self.capacity)

    def insert(self, equipment):
        index = self._index(equipment.id)
        node = self.buckets[index]
        if node is None:
            self.buckets[index] = ChainNode(equipment)
            self.size += 1
            return True
        while True:
            if node.data.id == equipment.id:
                return False
            if node.next is None:
                break
            node = node.next
        node.next = ChainNode(equipment)
        self.size += 1
        return True

    def search(self, equipment_id):
        node, comparisons = self.buckets[self._index(equipment_id)], 0
        while node:
            comparisons += 1
            if node.data.id == equipment_id:
                return node.data, comparisons
            node = node.next
        return None, comparisons

    def update(self, equipment_id, room=None, status=None):
        record, _ = self.search(equipment_id)
        return change(record, room, status) if record else None

    def delete(self, equipment_id):
        index = self._index(equipment_id)
        previous, node = None, self.buckets[index]
        while node:
            if node.data.id == equipment_id:
                if previous is None:
                    self.buckets[index] = node.next
                else:
                    previous.next = node.next
                self.size -= 1
                return True
            previous, node = node, node.next
        return False

    def contains(self, equipment_id):
        return self.search(equipment_id)[0] is not None

    def load_factor(self):
        return self.size / self.capacity

    def chain(self, index):
        keys, node = [], self.buckets[index]
        while node:
            keys.append(node.data.id)
            node = node.next
        return keys

    def records(self):
        return [record for index in range(self.capacity) for record in self._chain_records(index)]

    def _chain_records(self, index):
        node = self.buckets[index]
        while node:
            yield node.data
            node = node.next

    def display(self):
        return [f"{index}: {' → '.join(map(str, self.chain(index))) or '—'}" for index in range(self.capacity)]

    def rehash(self, new_capacity):
        old = self.records()
        self.capacity, self.buckets, self.size = new_capacity, [None] * new_capacity, 0
        for record in old:
            self.insert(record)


class OpenAddressHashTable:
    STRATEGIES = ("linear", "quadratic", "double")

    def __init__(self, capacity=13, strategy="linear", auto_resize=False):
        if strategy not in self.STRATEGIES:
            raise ValueError(f"unknown strategy {strategy}")
        self.capacity = capacity
        self.size = 0
        self.deleted_count = 0
        self.data = [EMPTY] * capacity
        self.strategy = strategy
        self.auto_resize = auto_resize
        self.last_insert = None

    def _probe(self, key):
        home = division_hash(key, self.capacity)
        step = 1 + key % (self.capacity - 1)
        for i in range(self.capacity):
            if self.strategy == "linear":
                yield (home + i) % self.capacity
            elif self.strategy == "quadratic":
                yield (home + i * i) % self.capacity
            else:
                yield (home + i * step) % self.capacity

    def insert(self, equipment):
        if self.auto_resize and (self.size + 1) / self.capacity > MAX_LOAD:
            self.rehash(next_prime(2 * self.capacity))
        probes, occupied, first_deleted, target = 0, 0, None, None
        for index in self._probe(equipment.id):
            probes += 1
            cell = self.data[index]
            if cell is EMPTY:
                target = index
                break
            if cell is DELETED:
                if first_deleted is None:
                    first_deleted = index
                continue
            if cell.id == equipment.id:
                self.last_insert = {"probes": probes, "occupied": occupied, "index": None}
                return False
            occupied += 1
        if first_deleted is not None:
            target = first_deleted
            self.deleted_count -= 1
        self.last_insert = {"probes": probes, "occupied": occupied, "index": target}
        if target is None:
            return False
        self.data[target] = equipment
        self.size += 1
        return True

    def search(self, equipment_id):
        visited = []
        for index in self._probe(equipment_id):
            cell = self.data[index]
            visited.append(index)
            if cell is EMPTY:
                return None, visited, len(visited)
            if cell is not DELETED and cell.id == equipment_id:
                return cell, visited, len(visited)
        return None, visited, len(visited)

    def path(self, visited):
        return " → ".join(f"{i}(DELETED)" if self.data[i] is DELETED else str(i) for i in visited)

    def update(self, equipment_id, room=None, status=None):
        record = self.search(equipment_id)[0]
        return change(record, room, status) if record else None

    def delete(self, equipment_id):
        record, visited, _ = self.search(equipment_id)
        if record is None:
            return False
        self.data[visited[-1]] = DELETED
        self.size -= 1
        self.deleted_count += 1
        return True

    def contains(self, equipment_id):
        return self.search(equipment_id)[0] is not None

    def load_factor(self):
        return self.size / self.capacity

    def used_factor(self):
        return (self.size + self.deleted_count) / self.capacity

    def rehash(self, new_capacity):
        active = [cell for cell in self.data if cell is not EMPTY and cell is not DELETED]
        self.capacity, self.size, self.deleted_count = new_capacity, 0, 0
        self.data = [EMPTY] * new_capacity
        auto, self.auto_resize = self.auto_resize, False
        for record in active:
            self.insert(record)
        self.auto_resize = auto

    def cell(self, index):
        value = self.data[index]
        return "—" if value is EMPTY else "DEL" if value is DELETED else str(value.id)

    def display(self):
        return [f"{index}: {self.cell(index)}" for index in range(self.capacity)]


def records():
    return [Equipment(*row) for row in SOURCE]


def print_columns(title, tables):
    print(title)
    print("  index | " + " | ".join(f"{t.strategy:<9}" for t in tables))
    for index in range(tables[0].capacity):
        print(f"  {index:>5} | " + " | ".join(f"{t.cell(index):<9}" for t in tables))


def stage_1():
    print("Stage 1. Record model")
    for bad in (0, -5):
        try:
            Equipment(bad, "Test", "A-100", "Свободно")
        except ValueError as error:
            print(f"  id {bad}: rejected, {error}")
    same = Equipment(26, "Другое имя", "X-1", "Выдано") == records()[0]
    print("  records with id 26 and different names are equal by key:", same)
    return same


def stage_2():
    print("\nStage 2. Hash functions, m = 13")
    keys = [row[0] for row in SOURCE]
    division = analyze_distribution(keys, 13, division_hash)
    mixed = analyze_distribution(keys, 13, mixed_hash)
    print("  key | division_hash | mixed_hash")
    for (key, d), (_, m) in zip(division["addresses"], mixed["addresses"]):
        print(f"  {key:>3} | {d:>13} | {m:>10}")
    for name, title in [("occupied", "occupied buckets"), ("empty", "empty buckets"), ("collisions", "inserts with collision"), ("max_in_bucket", "max keys in one bucket"), ("load_factor", "load factor")]:
        print(f"  {title:<24} {division[name]:>8.3f} {mixed[name]:>8.3f}" if name == "load_factor" else f"  {title:<24} {division[name]:>8} {mixed[name]:>8}")
    print("  division_hash puts the keys into 3 buckets: 26, 39, 52 differ by 13 and so do 14, 27, 40 and 16, 29, 42.")
    return division, mixed


def stage_3():
    print("\nStage 3. Separate chaining")
    table = ChainedHashTable(13)
    for record in records():
        table.insert(record)
    print("\n".join("  " + line for line in table.display()))
    print(f"  load factor {table.size}/{table.capacity} = {table.load_factor():.3f}")
    results = {}
    for key in (42, 91):
        record, comparisons = table.search(key)
        bucket = division_hash(key, 13)
        viewed = table.chain(bucket)[:comparisons]
        results[key] = (bucket, viewed, comparisons, record)
        print(f"  search {key}: bucket {bucket}, viewed {' → '.join(map(str, viewed))}, comparisons {comparisons}, {'found ' + record.name if record else 'not found'}")
    print("  insert 27 again:", "added" if table.insert(Equipment(27, "Маршрутизатор", "B-214", "Свободно")) else "rejected, duplicate id")
    updated = table.update(27, room="B-310", status="Выдано")
    print("  update 27:", updated)
    table.insert(Equipment(195, "Документ-камера", "B-210", "Свободно"))
    print("  insert 195, bucket 0:", " → ".join(map(str, table.chain(0))))
    table.delete(39)
    print("  delete 39 (middle of the chain), bucket 0:", " → ".join(map(str, table.chain(0))))
    print("  52 found:", table.contains(52), "195 found:", table.contains(195))
    table.insert(Equipment(351, "VR-шлем", "B-212", "Свободно"))
    print("  insert 351, bucket 0:", " → ".join(map(str, table.chain(0))))
    edge = ChainedHashTable(13)
    for record in records():
        edge.insert(record)
    edge.delete(26)
    edge.delete(52)
    print("  extra check: deleting the head 26 and the tail 52 leaves bucket 0 as", " → ".join(map(str, edge.chain(0))))
    return table, results, edge


def stage_5():
    print("\nStage 5. Open addressing, m = 13, no resizing")
    tables, stats = [], {}
    for strategy in OpenAddressHashTable.STRATEGIES:
        table = OpenAddressHashTable(13, strategy)
        probes = occupied = 0
        for record in records():
            table.insert(record)
            probes += table.last_insert["probes"]
            occupied += table.last_insert["occupied"]
        tables.append(table)
        stats[strategy] = (occupied, probes)
    print_columns("  table after nine inserts", tables)
    print("  strategy  | occupied cells met | total probes")
    for strategy, (occupied, probes) in stats.items():
        print(f"  {strategy:<9} | {occupied:>18} | {probes:>12}")
    print("  Primary clustering: linear probing fills neighbouring cells, so keys with different home addresses")
    print("  (14, 27, 40 start at 1, 16, 29, 42 at 3) run into the same block 0..8 and every new key walks the whole block.")
    print("  Quadratic probing jumps by 1, 4, 9 and double hashing by a key-dependent step, so the block does not grow as one piece.")
    return tables, stats


def stage_7(tables):
    print("\nStage 7. Search")
    paths = {}
    for key in (42, 91):
        for table in tables:
            record, visited, probes = table.search(key)
            paths[(table.strategy, key)] = (visited, probes)
            print(f"  {key} {table.strategy:<9}: {' → '.join(map(str, visited))}, probes {probes}, {'found' if record else 'not found, stopped at EMPTY'}")
    return paths


def stage_8(tables):
    print("\nStage 8. Deletion with DELETED")
    paths = {}
    for table in tables:
        table.insert(Equipment(195, "Документ-камера", "B-210", "Свободно"))
        table.delete(39)
        record, visited, _ = table.search(195)
        paths[table.strategy] = table.path(visited)
        print(f"  {table.strategy:<9}: search 195 after deleting 39: {paths[table.strategy]} -> {'found' if record else 'missing'}")
        tomb = next(i for i in visited if table.data[i] is DELETED)
        table.data[tomb] = EMPTY
        wrong = table.search(195)[0]
        table.data[tomb] = DELETED
        print(f"  {'':<9}  experiment: DELETED replaced by EMPTY -> 195 {'found' if wrong else 'reported missing'}, marker restored")
        table.insert(Equipment(351, "VR-шлем", "B-212", "Свободно"))
        print(f"  {'':<9}  insert 351 -> cell {table.last_insert['index']} (the cell left by 39 is reused)")
    print("  Without DELETED the search for 195 stops at the cell of the removed 39 as if it were never used,")
    print("  although 195 was placed further along the same probe sequence, so an existing record looks missing.")
    print_columns("  state after all operations", tables)
    print(f"  active records {tables[0].size}, load factor {tables[0].size}/13 = {tables[0].load_factor():.3f}")
    return paths


def stage_9(tables):
    print("\nStage 9. Resizing and rehashing")
    print(f"  is_prime(29) {is_prime(29)}, next_prime(26) {next_prime(26)}")
    for table in tables:
        table.auto_resize = True
        before = table.capacity
        table.insert(Equipment(54, "Набор датчиков", "A-305", "Свободно"))
        cells = [(i, table.cell(i)) for i in range(table.capacity) if table.cell(i) != "—"]
        print(f"  {table.strategy:<9}: {before} -> {table.capacity}, size {table.size}, deleted {table.deleted_count}, load {table.load_factor():.3f}")
        print("             " + ", ".join(f"{i}:{k}" for i, k in cells))
    return tables


def experiment(seed=2026, capacity=101, unsuccessful=1000):
    rng = random.Random(seed)
    pool = rng.sample(range(1, 1_000_000), capacity + unsuccessful)
    absent = pool[capacity:]
    rows = {}
    for fill in (0.25, 0.50, 0.70, 0.85):
        n = round(fill * capacity)
        keys = pool[:n]
        chained = ChainedHashTable(capacity)
        collisions = insert_cost = worst = 0
        for key in keys:
            bucket = chained.chain(division_hash(key, capacity))
            collisions += bool(bucket)
            insert_cost += len(bucket) + 1
            worst = max(worst, len(bucket) + 1)
            chained.insert(Equipment(key, "", "", ""))
        lengths = [len(chained.chain(i)) for i in range(capacity)]
        rows[(fill, "chaining")] = {
            "collisions": collisions,
            "avg insert": insert_cost / n,
            "max insert": worst,
            "avg hit": sum(chained.search(k)[1] for k in keys) / n,
            "avg miss": sum(chained.search(k)[1] for k in absent) / len(absent),
            "longest chain": max(lengths),
            "empty": lengths.count(0),
            "failed": 0,
        }
        for strategy in OpenAddressHashTable.STRATEGIES:
            table = OpenAddressHashTable(capacity, strategy)
            collisions = probes = worst = failed = 0
            for key in keys:
                ok = table.insert(Equipment(key, "", "", ""))
                failed += not ok
                collisions += table.last_insert["occupied"] > 0
                probes += table.last_insert["probes"]
                worst = max(worst, table.last_insert["probes"])
            stored = [k for k in keys if table.contains(k)]
            run = longest = 0
            for cell in table.data + table.data:
                run = run + 1 if cell is not EMPTY else 0
                longest = max(longest, min(run, capacity))
            rows[(fill, strategy)] = {
                "collisions": collisions,
                "avg insert": probes / n,
                "max insert": worst,
                "avg hit": sum(table.search(k)[2] for k in stored) / len(stored),
                "avg miss": sum(table.search(k)[2] for k in absent) / len(absent),
                "longest chain": longest,
                "empty": table.data.count(EMPTY),
                "failed": failed,
            }
    return rows


def stage_10():
    print("\nStage 10. Experiment, m = 101, random keys, no resizing")
    print("  chaining counts key comparisons, open addressing counts inspected cells;")
    print("  'longest chain' for open addressing is the longest run of occupied cells (cluster)")
    rows = experiment()
    methods = ("chaining",) + OpenAddressHashTable.STRATEGIES
    for metric in ("collisions", "avg insert", "max insert", "avg hit", "avg miss", "longest chain", "empty", "failed"):
        print(f"\n  {metric}")
        print("  fill | " + " | ".join(f"{m:<9}" for m in methods))
        for fill in (0.25, 0.50, 0.70, 0.85):
            values = [rows[(fill, m)][metric] for m in methods]
            print(f"  {fill:.2f} | " + " | ".join(f"{v:<9.2f}" if isinstance(v, float) else f"{v:<9}" for v in values))
    return rows


def main():
    same = stage_1()
    division, mixed = stage_2()
    chained, chain_results, edge = stage_3()
    tables, stats = stage_5()
    search_paths = stage_7(tables)
    deleted_paths = stage_8(tables)
    snapshot = {t.strategy: [t.cell(i) for i in range(13)] for t in tables}
    stage_9(tables)
    rows = stage_10()
    return same, division, mixed, chained, chain_results, edge, stats, search_paths, deleted_paths, snapshot, tables, rows


if __name__ == "__main__":
    same, division, mixed, chained, chain_results, edge, stats, search_paths, deleted_paths, snapshot, tables, rows = main()
    assert same and [f.name for f in fields(Equipment)] == ["id", "name", "room", "status"]
    assert [a for _, a in division["addresses"]] == [0, 0, 0, 1, 1, 1, 3, 3, 3]
    assert [a for _, a in mixed["addresses"]] == [6, 9, 12, 0, 0, 3, 1, 4, 4]
    assert (division["occupied"], division["empty"], division["collisions"], division["max_in_bucket"]) == (3, 10, 6, 3)
    assert (mixed["occupied"], mixed["empty"], mixed["collisions"], mixed["max_in_bucket"]) == (7, 6, 2, 2)
    assert chain_results[42][1:3] == ([16, 29, 42], 3) and chain_results[91][1:3] == ([26, 39, 52], 3)
    assert chained.chain(0) == [26, 52, 195, 351] and chained.search(27)[0].room == "B-310"
    assert edge.chain(0) == [39] and edge.chain(1) == [14, 27, 40]
    assert stats == {"linear": (24, 33), "quadratic": (14, 23), "double": (8, 17)}
    assert search_paths[("linear", 42)] == ([3, 4, 5, 6, 7, 8], 6)
    assert search_paths[("quadratic", 42)] == ([3, 4, 7, 12], 4)
    assert search_paths[("double", 42)] == ([3, 10], 2)
    assert search_paths[("linear", 91)] == (list(range(10)), 10)
    assert search_paths[("quadratic", 91)] == ([0, 1, 4, 9], 4)
    assert search_paths[("double", 91)] == ([0, 8], 2)
    assert deleted_paths == {"linear": "0 → 1(DELETED) → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9", "quadratic": "0 → 1(DELETED) → 4 → 9", "double": "0 → 4(DELETED) → 8"}
    assert snapshot["linear"] == ["26", "351", "52", "14", "27", "40", "16", "29", "42", "195", "—", "—", "—"]
    assert snapshot["quadratic"] == ["26", "351", "14", "16", "52", "27", "—", "29", "—", "195", "40", "—", "42"]
    assert snapshot["double"] == ["26", "14", "29", "16", "351", "52", "40", "—", "195", "27", "42", "—", "—"]
    expected = {0: "29", 3: "351", 11: "40", 13: "42", 14: "14", 16: "16", 21: "195", 23: "52", 25: "54", 26: "26", 27: "27"}
    for table in tables:
        assert table.capacity == 29 and table.size == 11 and table.deleted_count == 0
        assert {i: table.cell(i) for i in range(29) if table.cell(i) != "—"} == expected
    assert all(rows[(f, "chaining")]["failed"] == 0 for f in (0.25, 0.5, 0.7, 0.85))
    assert rows[(0.85, "linear")]["avg miss"] > rows[(0.85, "double")]["avg miss"]
    print("\nchecks passed")
