import random
from collections import deque


class Node:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right


def to_array(root):
    result, queue = [], deque([root] if root else [])
    while queue:
        node = queue.popleft()
        result.append(node.key)
        queue.extend(child for child in (node.left, node.right) if child)
    return result


def heapify(arr, n, i):
    while True:
        largest = i
        for child in (2 * i + 1, 2 * i + 2):
            if child < n and arr[child] > arr[largest]:
                largest = child
        if largest == i:
            return
        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest


def build_max_heap(arr):
    for i in range(len(arr) // 2 - 1, -1, -1):
        heapify(arr, len(arr), i)
    return arr


def to_tree(arr, i=0):
    if i >= len(arr):
        return None
    return Node(arr[i], to_tree(arr, 2 * i + 1), to_tree(arr, 2 * i + 2))


def max_heap_from_tree(root):
    return to_tree(build_max_heap(to_array(root)))


def is_max_heap(root):
    arr = to_array(root)
    complete = to_array(to_tree(arr)) == arr
    return complete and all(arr[(i - 1) // 2] >= arr[i] for i in range(1, len(arr)))


def draw(node, depth=0):
    if node is None:
        return []
    return draw(node.right, depth + 1) + ["    " * depth + str(node.key)] + draw(node.left, depth + 1)


if __name__ == "__main__":
    lecture = Node(1, Node(12, Node(5), Node(6)), Node(9, Node(10)))
    print("tree from the lecture:", to_array(lecture))
    heap = max_heap_from_tree(lecture)
    print("descending heap:", to_array(heap))
    print("\n".join(draw(heap)))

    crooked = Node(3, Node(8, None, Node(1, Node(14))), Node(2, Node(7, None, Node(20))))
    print("\nany tree, not complete:")
    print("\n".join(draw(crooked)))
    heap = max_heap_from_tree(crooked)
    print("descending heap:", to_array(heap))
    print("\n".join(draw(heap)))

    assert to_array(max_heap_from_tree(lecture)) == [12, 6, 10, 5, 1, 9]
    assert is_max_heap(heap) and sorted(to_array(heap)) == sorted(to_array(crooked))
    assert not is_max_heap(crooked)
    random.seed(3)
    for _ in range(100):
        values = random.sample(range(100), random.randint(1, 30))
        root = None
        for value in values:
            root = Node(value, root, None) if random.random() < 0.5 else Node(value, None, root)
        assert is_max_heap(max_heap_from_tree(root))
    print("checks passed")
