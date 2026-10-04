import random


class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.counter = 0

    def __len__(self):
        return len(self.heap)

    def _key(self, i):
        priority, order, _ = self.heap[i]
        return priority, -order

    def insert(self, item, priority):
        self.heap.append((priority, self.counter, item))
        self.counter += 1
        i = len(self.heap) - 1
        while i > 0 and self._key((i - 1) // 2) < self._key(i):
            parent = (i - 1) // 2
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            i = parent

    def peek(self):
        if not self.heap:
            raise IndexError("queue is empty")
        priority, _, item = self.heap[0]
        return item, priority

    def extract_max(self):
        if not self.heap:
            raise IndexError("queue is empty")
        priority, _, item = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0, len(self.heap))
        return item, priority

    def _sift_down(self, i, n):
        while True:
            largest = i
            for child in (2 * i + 1, 2 * i + 2):
                if child < n and self._key(child) > self._key(largest):
                    largest = child
            if largest == i:
                return
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            i = largest


def heap_sort(arr):
    def sift_down(i, n):
        while True:
            largest = i
            for child in (2 * i + 1, 2 * i + 2):
                if child < n and arr[child] > arr[largest]:
                    largest = child
            if largest == i:
                return
            arr[i], arr[largest] = arr[largest], arr[i]
            i = largest

    for i in range(len(arr) // 2 - 1, -1, -1):
        sift_down(i, len(arr))
    for end in range(len(arr) - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        sift_down(0, end)
    return arr


if __name__ == "__main__":
    queue = PriorityQueue()
    for task, priority in [("reply to email", 2), ("fix production bug", 10), ("code review", 5), ("lunch", 1), ("deploy hotfix", 10), ("standup", 5)]:
        queue.insert(task, priority)
        print(f"insert {task!r} with priority {priority}")
    print("next:", queue.peek())
    order = [queue.extract_max() for _ in range(len(queue))]
    for task, priority in order:
        print(f"  {priority:>2}  {task}")
    print("heap sort:", heap_sort([5, 2, 9, 1, 5, 6, 0, 3]))

    assert [task for task, _ in order] == ["fix production bug", "deploy hotfix", "code review", "standup", "reply to email", "lunch"]
    random.seed(11)
    for _ in range(200):
        values = [random.randint(-20, 20) for _ in range(random.randint(0, 50))]
        assert heap_sort(values[:]) == sorted(values)
        q = PriorityQueue()
        for v in values:
            q.insert(str(v), v)
        assert [q.extract_max()[1] for _ in range(len(q))] == sorted(values, reverse=True)
    print("checks passed")
