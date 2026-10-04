import random


class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


def height(node):
    return node.height if node else 0


def update(node):
    node.height = 1 + max(height(node.left), height(node.right))


def balance(node):
    return height(node.left) - height(node.right)


def rotate_right(y):
    x = y.left
    y.left, x.right = x.right, y
    update(y)
    update(x)
    return x


def rotate_left(x):
    y = x.right
    x.right, y.left = y.left, x
    update(x)
    update(y)
    return y


def rebalance(node):
    update(node)
    if balance(node) > 1:
        if balance(node.left) < 0:
            node.left = rotate_left(node.left)
        return rotate_right(node)
    if balance(node) < -1:
        if balance(node.right) > 0:
            node.right = rotate_right(node.right)
        return rotate_left(node)
    return node


def insert(node, key):
    if node is None:
        return Node(key)
    if key < node.key:
        node.left = insert(node.left, key)
    elif key > node.key:
        node.right = insert(node.right, key)
    else:
        return node
    return rebalance(node)


def min_key(node):
    while node.left:
        node = node.left
    return node.key


def delete(node, key):
    if node is None:
        return None
    if key < node.key:
        node.left = delete(node.left, key)
    elif key > node.key:
        node.right = delete(node.right, key)
    else:
        if node.left is None or node.right is None:
            return node.left or node.right
        node.key = min_key(node.right)
        node.right = delete(node.right, node.key)
    return rebalance(node)


def plain_bst_insert(node, key):
    if node is None:
        return Node(key)
    if key < node.key:
        node.left = plain_bst_insert(node.left, key)
    else:
        node.right = plain_bst_insert(node.right, key)
    update(node)
    return node


def in_order(node):
    return in_order(node.left) + [node.key] + in_order(node.right) if node else []


def is_avl(node):
    if node is None:
        return True
    return abs(balance(node)) <= 1 and is_avl(node.left) and is_avl(node.right)


def draw(node, depth=0):
    if node is None:
        return []
    return draw(node.right, depth + 1) + ["    " * depth + str(node.key)] + draw(node.left, depth + 1)


if __name__ == "__main__":
    keys = list(range(1, 16))
    avl, plain = None, None
    for key in keys:
        avl = insert(avl, key)
        plain = plain_bst_insert(plain, key)
    print("keys inserted in sorted order 1..15")
    print("plain BST height:", height(plain), "- it degenerated into a list")
    print("AVL height:", height(avl))
    print("\n".join(draw(avl)))
    for key in [8, 1, 2, 3]:
        avl = delete(avl, key)
    print("after deleting 8, 1, 2, 3:", in_order(avl), "height", height(avl))
    print("\n".join(draw(avl)))

    assert height(plain) == 15 and height(avl) == 4
    assert in_order(avl) == [4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15]
    assert is_avl(avl)
    random.seed(1)
    tree, alive = None, set()
    for _ in range(2000):
        key = random.randint(1, 300)
        if random.random() < 0.6:
            tree = insert(tree, key)
            alive.add(key)
        else:
            tree = delete(tree, key)
            alive.discard(key)
        assert is_avl(tree)
    assert in_order(tree) == sorted(alive)
    print("checks passed")
