class Node:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

    def is_leaf(self):
        return self.left is None and self.right is None

    def children(self):
        return [child for child in (self.left, self.right) if child is not None]

    def __repr__(self):
        return f"Node({self.key})"


def insert(root, key, value=None):
    node = Node(key, value)
    if root is None:
        return node
    current = root
    while True:
        if key == current.key:
            current.value = value
            return root
        side = "left" if key < current.key else "right"
        child = getattr(current, side)
        if child is None:
            setattr(current, side, node)
            node.parent = current
            return root
        current = child


def in_order(node):
    if node is None:
        return []
    return in_order(node.left) + [node.key] + in_order(node.right)


def draw(node, depth=0):
    if node is None:
        return []
    return draw(node.right, depth + 1) + ["    " * depth + str(node.key)] + draw(node.left, depth + 1)


if __name__ == "__main__":
    root = None
    for key in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
        root = insert(root, key)
    print("\n".join(draw(root)))
    print("in-order:", in_order(root))
    print("root:", root, "children:", root.children(), "leaf 1:", root.left.left.is_leaf())
    print("parent of 6:", root.left.right.parent)
    assert in_order(root) == sorted([8, 3, 10, 1, 6, 14, 4, 7, 13])
    assert root.left.right.parent is root.left
    assert root.left.left.is_leaf() and not root.is_leaf()
    print("checks passed")
