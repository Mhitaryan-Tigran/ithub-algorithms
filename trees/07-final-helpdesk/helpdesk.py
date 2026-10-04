from collections import deque
from dataclasses import dataclass

DELETE_METHOD = "a node with two children is replaced by its in-order successor (the minimum of the right subtree); the whole request is moved"

REQUESTS = [
    (50, "Ошибка оплаты", 9),
    (30, "Сброс пароля", 4),
    (70, "Интеграция API", 13),
    (20, "Изменение профиля", 2),
    (40, "Ошибка отчёта", 7),
    (60, "Настройка уведомлений", 11),
    (80, "Сбой сервера", 15),
    (10, "Удаление аккаунта", 1),
    (25, "Проблема входа", 3),
    (35, "Экспорт данных", 5),
    (45, "Возврат платежа", 8),
    (55, "Подключение тарифа", 10),
    (65, "Ошибка синхронизации", 12),
    (75, "Недоступна база данных", 14),
    (90, "Обновление реквизитов", 6),
]


@dataclass
class Request:
    id: int
    title: str
    priority: int

    def __str__(self):
        return f"{self.id}({self.priority})"


class TreeNode:
    def __init__(self, request):
        self.request = request
        self.left = None
        self.right = None


def insert(root, request):
    if root is None:
        return TreeNode(request), True
    if request.id == root.request.id:
        return root, False
    if request.id < root.request.id:
        root.left, added = insert(root.left, request)
    else:
        root.right, added = insert(root.right, request)
    return root, added


def pre_order(node):
    return [node.request] + pre_order(node.left) + pre_order(node.right) if node else []


def in_order(node):
    return in_order(node.left) + [node.request] + in_order(node.right) if node else []


def post_order(node):
    return post_order(node.left) + post_order(node.right) + [node.request] if node else []


def level_order(root):
    result, queue = [], deque([root] if root else [])
    while queue:
        node = queue.popleft()
        result.append(node.request)
        queue.extend(child for child in (node.left, node.right) if child)
    return result


def levels(root):
    rows, queue = [], deque([root] if root else [])
    while queue:
        rows.append([str(node.request) for node in queue])
        queue = deque(child for node in queue for child in (node.left, node.right) if child)
    return rows


def search(root, request_id):
    path, node = [], root
    while node:
        path.append(node.request.id)
        if request_id == node.request.id:
            return node.request, path
        node = node.left if request_id < node.request.id else node.right
    return None, path


def find_min(root):
    while root.left:
        root = root.left
    return root.request


def find_max(root):
    while root.right:
        root = root.right
    return root.request


def count_nodes(root):
    return 1 + count_nodes(root.left) + count_nodes(root.right) if root else 0


def count_leaves(root):
    if root is None:
        return 0
    if root.left is None and root.right is None:
        return 1
    return count_leaves(root.left) + count_leaves(root.right)


def height(root):
    return 1 + max(height(root.left), height(root.right)) if root else 0


def get_depth(root, request_id):
    found, path = search(root, request_id)
    return len(path) - 1 if found else None


def validate_bst(root, low=None, high=None):
    if root is None:
        return True
    key = root.request.id
    if (low is not None and key <= low) or (high is not None and key >= high):
        return False
    return validate_bst(root.left, low, key) and validate_bst(root.right, key, high)


def delete(root, request_id):
    if root is None:
        return None, False
    if request_id < root.request.id:
        root.left, removed = delete(root.left, request_id)
        return root, removed
    if request_id > root.request.id:
        root.right, removed = delete(root.right, request_id)
        return root, removed
    if root.left is None:
        return root.right, True
    if root.right is None:
        return root.left, True
    successor = find_min(root.right)
    root.request = successor
    root.right, _ = delete(root.right, successor.id)
    return root, True


def ids(requests):
    return [r.id for r in requests]


def show(requests):
    return ", ".join(str(r) for r in requests)


def key(request):
    return request.priority, request.id


def sift_down(data, heap_size, index):
    while True:
        largest = index
        for child in (2 * index + 1, 2 * index + 2):
            if child < heap_size and key(data[child]) > key(data[largest]):
                largest = child
        if largest == index:
            return
        data[index], data[largest] = data[largest], data[index]
        index = largest


def build_max_heap(data):
    for i in range(len(data) // 2 - 1, -1, -1):
        sift_down(data, len(data), i)
    return data


def is_max_heap(data):
    return all(key(data[(i - 1) // 2]) >= key(data[i]) for i in range(1, len(data)))


def heap_levels(data):
    rows, start, width = [], 0, 1
    while start < len(data):
        rows.append(show(data[start:start + width]))
        start, width = start + width, width * 2
    return rows


def heap_sort(data):
    build_max_heap(data)
    for end in range(len(data) - 1, 0, -1):
        data[0], data[end] = data[end], data[0]
        sift_down(data, end, 0)
    return data


def state(root, operation):
    print(f"\n{operation}")
    print("  in-order:", ", ".join(map(str, ids(in_order(root)))))
    print("  nodes:", count_nodes(root), "height:", height(root), "validate_bst:", validate_bst(root))


def main():
    root = None
    for record in REQUESTS:
        root, _ = insert(root, Request(*record))

    print("Stage 1. BST by levels, ID(priority):")
    for depth, row in enumerate(levels(root), 1):
        print(f"  level {depth}: {'  '.join(row)}")

    print("\nStage 2. Traversals")
    traversals = {"pre-order": pre_order(root), "in-order": in_order(root), "post-order": post_order(root), "level-order": level_order(root)}
    for name, result in traversals.items():
        print(f"  {name:<12}", ", ".join(map(str, ids(result))))
    print("  In-order gives ascending ids: for every node the whole left subtree holds smaller keys and the right one larger,")
    print("  so visiting left subtree, node, right subtree lists the smaller keys first, then the node, then the larger ones.")

    print("\nStage 3. Search and characteristics")
    found, path = search(root, 65)
    print("  search 65:", found, "path:", " → ".join(map(str, path)))
    missing, path99 = search(root, 99)
    print("  search 99:", missing, "path:", " → ".join(map(str, path99)))
    characteristics = {
        "nodes": count_nodes(root),
        "leaves": count_leaves(root),
        "height": height(root),
        "min id": find_min(root).id,
        "max id": find_max(root).id,
        "depth of 65": get_depth(root, 65),
        "validate_bst": validate_bst(root),
    }
    for name, value in characteristics.items():
        print(f"  {name:<13} {value}")

    print("\nStage 4. Changing the tree")
    print("  deletion method:", DELETE_METHOD)
    root, added = insert(root, Request(37, "Утечка данных", 16))
    state(root, f"1. insert 37 -> {'added' if added else 'rejected'}")
    root, added = insert(root, Request(50, "Дубликат", 1))
    state(root, f"2. insert 50 again -> {'added' if added else 'rejected as duplicate'}")
    for step, request_id, kind in [(3, 10, "leaf"), (4, 35, "one child"), (5, 70, "two children"), (6, 999, "missing")]:
        root, removed = delete(root, request_id)
        state(root, f"{step}. delete {request_id} ({kind}) -> {'removed' if removed else 'not found, tree unchanged'}")

    print("\nStage 5. Max heap by (priority, id)")
    data = in_order(root)
    print("  source array:", show(data))
    build_max_heap(data)
    print("  heap array:  ", show(data))
    for depth, row in enumerate(heap_levels(data), 1):
        print(f"  level {depth}: {row}")
    print("  is_max_heap:", is_max_heap(data))

    print("\nStage 6. Heap sort for the report, most urgent first")
    report = heap_sort(in_order(root))[::-1]
    for r in report:
        print(f"  {r.priority:>2}  {r.id:>3}  {r.title}")

    print("\nComplexity, n nodes, h height")
    for row in [
        ("insert, search, delete in BST", "O(h): O(log n) balanced, O(n) degenerate", "O(h) recursion"),
        ("traversals", "O(n)", "O(h) recursion, O(n) queue for level-order"),
        ("count, height, validate_bst", "O(n)", "O(h)"),
        ("sift_down", "O(log n)", "O(1)"),
        ("build_max_heap", "O(n)", "O(1)"),
        ("heap_sort", "O(n log n) always", "O(1), in place, not stable"),
    ]:
        print("  {:<30} {:<42} {}".format(*row))

    return root, traversals, characteristics, (path, path99), data, report


if __name__ == "__main__":
    root, traversals, characteristics, (path, path99), data, report = main()
    assert ids(traversals["pre-order"]) == [50, 30, 20, 10, 25, 40, 35, 45, 70, 60, 55, 65, 80, 75, 90]
    assert ids(traversals["in-order"]) == sorted(r[0] for r in REQUESTS)
    assert ids(traversals["post-order"]) == [10, 25, 20, 35, 45, 40, 30, 55, 65, 60, 75, 90, 80, 70, 50]
    assert ids(traversals["level-order"]) == [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 90]
    assert characteristics == {"nodes": 15, "leaves": 8, "height": 4, "min id": 10, "max id": 90, "depth of 65": 3, "validate_bst": True}
    assert path == [50, 70, 60, 65] and path99 == [50, 70, 80, 90]
    assert ids(in_order(root)) == [20, 25, 30, 37, 40, 45, 50, 55, 60, 65, 75, 80, 90]
    assert count_nodes(root) == 13 and height(root) == 4 and validate_bst(root)
    assert show(data) == "37(16), 75(14), 80(15), 60(11), 65(12), 45(8), 50(9), 55(10), 25(3), 20(2), 40(7), 30(4), 90(6)"
    assert [key(r) for r in report] == sorted((key(r) for r in report), reverse=True)
    broken = TreeNode(Request(50, "", 1))
    broken.left = TreeNode(Request(30, "", 1))
    broken.left.right = TreeNode(Request(60, "", 1))
    assert not validate_bst(broken)
    print("\nchecks passed")
