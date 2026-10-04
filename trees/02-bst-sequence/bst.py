class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.size = 1


def size(node):
    return node.size if node else 0


class BinarySearchTree:
    def __init__(self, keys=()):
        self.root = None
        for key in keys:
            self.insert(key)

    def __len__(self):
        return size(self.root)

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return Node(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        node.size = 1 + size(node.left) + size(node.right)
        return node

    def search(self, key):
        node, path = self.root, []
        while node is not None:
            path.append(node.key)
            if key == node.key:
                return node, path
            node = node.left if key < node.key else node.right
        return None, path

    def minimum(self, node=None):
        node = node or self.root
        while node.left:
            node = node.left
        return node.key

    def maximum(self, node=None):
        node = node or self.root
        while node.right:
            node = node.right
        return node.key

    def successor(self, key):
        node, best = self.root, None
        while node:
            if key < node.key:
                best, node = node.key, node.left
            else:
                node = node.right
        return best

    def predecessor(self, key):
        node, best = self.root, None
        while node:
            if key > node.key:
                best, node = node.key, node.right
            else:
                node = node.left
        return best

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            node.key = self.minimum(node.right)
            node.right = self._delete(node.right, node.key)
        node.size = 1 + size(node.left) + size(node.right)
        return node

    def in_order(self):
        result = []

        def walk(node):
            if node:
                walk(node.left)
                result.append(node.key)
                walk(node.right)

        walk(self.root)
        return result

    def kth(self, i):
        if not 1 <= i <= len(self):
            raise IndexError(f"no node number {i} in a tree of {len(self)}")
        node = self.root
        while True:
            left = size(node.left)
            if i == left + 1:
                return node.key
            if i <= left:
                node = node.left
            else:
                i -= left + 1
                node = node.right

    def height(self, node="root"):
        node = self.root if node == "root" else node
        return 0 if node is None else 1 + max(self.height(node.left), self.height(node.right))

    def draw(self):
        lines = []

        def walk(node, depth):
            if node:
                walk(node.right, depth + 1)
                lines.append("      " * depth + str(node.key))
                walk(node.left, depth + 1)

        walk(self.root, 0)
        return "\n".join(lines)


if __name__ == "__main__":
    keys = [17, 6, 5, 20, 19, 18, 11, 14, 12, 13, 2, 4, 10]
    tree = BinarySearchTree(keys)
    print("tree turned 90 degrees left, root on the left:")
    print(tree.draw())
    print("in-order:", tree.in_order())
    print("i-th node:", [(i, tree.kth(i)) for i in range(1, len(tree) + 1)])
    node, path = tree.search(13)
    print("search 13, path:", " -> ".join(map(str, path)))
    print("min", tree.minimum(), "max", tree.maximum(), "height", tree.height())
    print("successor of 14:", tree.successor(14), "predecessor of 17:", tree.predecessor(17))
    tree.insert(15)
    print("after insert 15:", tree.in_order())
    tree.delete(6)
    print("after delete 6 (two children, replaced by in-order successor 10):", tree.in_order())
    print("5th node now:", tree.kth(5))

    assert BinarySearchTree(keys).in_order() == sorted(keys)
    fresh = BinarySearchTree(keys)
    assert [fresh.kth(i) for i in range(1, 14)] == sorted(keys)
    assert path == [17, 6, 11, 14, 12, 13]
    assert fresh.height() == 6
    assert tree.in_order() == sorted(set(keys + [15]) - {6})
    assert tree.kth(5) == 11 and len(tree) == 13
    assert fresh.successor(14) == 17 and fresh.predecessor(17) == 14
    print("checks passed")
