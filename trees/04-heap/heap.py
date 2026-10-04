import random


class MinHeap:
    def __init__(self, items=()):
        self.data = list(items)
        for i in range(len(self.data) // 2 - 1, -1, -1):
            self._sift_down(i)

    def __len__(self):
        return len(self.data)

    def peek(self):
        if not self.data:
            raise IndexError("heap is empty")
        return self.data[0]

    def push(self, item):
        self.data.append(item)
        self._sift_up(len(self.data) - 1)

    def pop(self):
        if not self.data:
            raise IndexError("heap is empty")
        top = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self._sift_down(0)
        return top

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.data[i] >= self.data[parent]:
                return
            self.data[i], self.data[parent] = self.data[parent], self.data[i]
            i = parent

    def _sift_down(self, i):
        n = len(self.data)
        while True:
            smallest = i
            for child in (2 * i + 1, 2 * i + 2):
                if child < n and self.data[child] < self.data[smallest]:
                    smallest = child
            if smallest == i:
                return
            self.data[i], self.data[smallest] = self.data[smallest], self.data[i]
            i = smallest

    def is_valid(self):
        return all(self.data[(i - 1) // 2] <= self.data[i] for i in range(1, len(self.data)))

    def levels(self):
        rows, start, width = [], 0, 1
        while start < len(self.data):
            rows.append(self.data[start:start + width])
            start, width = start + width, width * 2
        return rows


if __name__ == "__main__":
    heap = MinHeap()
    for value in [7, 3, 9, 1, 5, 8, 2]:
        heap.push(value)
        print(f"push {value}: {heap.data}")
    print("levels:", heap.levels())
    print("peek:", heap.peek())
    print("pop all:", [heap.pop() for _ in range(len(heap))])
    built = MinHeap([9, 4, 7, 1, 8, 2, 6])
    print("heapify [9, 4, 7, 1, 8, 2, 6]:", built.data)

    assert built.data == [1, 4, 2, 9, 8, 7, 6] and built.is_valid()
    random.seed(7)
    for _ in range(200):
        values = [random.randint(-50, 50) for _ in range(random.randint(0, 40))]
        h = MinHeap(values)
        extra = random.randint(-50, 50)
        h.push(extra)
        assert h.is_valid()
        assert [h.pop() for _ in range(len(h))] == sorted(values + [extra])
    print("checks passed")
