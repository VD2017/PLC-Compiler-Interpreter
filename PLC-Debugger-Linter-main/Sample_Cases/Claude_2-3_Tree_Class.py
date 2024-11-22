class Node:
    def __init__(self, keys=None, children=None):
        self.keys = keys or []
        self.children = children or []

class TwoThreeTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if not self.root:
            self.root = Node([key])
        else:
            new_node = self._insert_recursive(self.root, key)
            if new_node:
                self.root = new_node

    def _insert_recursive(self, node, key):
        if not node.children:  # Leaf node
            node.keys.append(key)
            node.keys.sort()
            if len(node.keys) > 2:
                return self._split_node(node)
        else:  # Internal node
            child_index = self._find_child_index(node, key)
            new_child = self._insert_recursive(node.children[child_index], key)
            if new_child:
                node.keys.insert(child_index, new_child.keys[0])
                node.children[child_index] = new_child.children[0]
                node.children.insert(child_index + 1, new_child.children[1])
                if len(node.keys) > 2:
                    return self._split_node(node)
        return None

    def _split_node(self, node):
        mid = len(node.keys) // 2
        left = Node(node.keys[:mid], node.children[:mid+1])
        right = Node(node.keys[mid+1:], node.children[mid+1:])
        return Node([node.keys[mid]], [left, right])

    def _find_child_index(self, node, key):
        for i, k in enumerate(node.keys):
            if key < k:
                return i
        return len(node.keys)

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if not node:
            return False
        if key in node.keys:
            return True
        if not node.children:
            return False
        return self._search_recursive(node.children[self._find_child_index(node, key)], key)

    def delete(self, key):
        if not self.root:
            return
        self._delete_recursive(None, self.root, key)
        if self.root and not self.root.keys:
            self.root = self.root.children[0] if self.root.children else None

    def _delete_recursive(self, parent, node, key):
        if key in node.keys:
            if not node.children:  # Leaf node
                node.keys.remove(key)
            else:  # Internal node
                pred_node = self._get_predecessor(node, node.keys.index(key))
                node.keys[node.keys.index(key)] = pred_node.keys[-1]
                self._delete_recursive(node, pred_node, pred_node.keys[-1])
        else:
            if not node.children:
                return
            child_index = self._find_child_index(node, key)
            if len(node.children[child_index].keys) < 2:
                self._rebalance(node, child_index)
            self._delete_recursive(node, node.children[child_index], key)

    def _get_predecessor(self, node, index):
        current = node.children[index]
        while current.children:
            current = current.children[-1]
        return current

    def _rebalance(self, parent, index):
        child = parent.children[index]
        if index > 0 and len(parent.children[index - 1].keys) > 1:
            self._rotate_right(parent, index - 1, index)
        elif index < len(parent.children) - 1 and len(parent.children[index + 1].keys) > 1:
            self._rotate_left(parent, index, index + 1)
        else:
            if index > 0:
                self._merge(parent, index - 1, index)
            else:
                self._merge(parent, index, index + 1)

    def _rotate_right(self, parent, left_index, right_index):
        left_child = parent.children[left_index]
        right_child = parent.children[right_index]

        right_child.keys.insert(0, parent.keys[left_index])
        parent.keys[left_index] = left_child.keys.pop()

        if left_child.children:
            right_child.children.insert(0, left_child.children.pop())

    def _rotate_left(self, parent, left_index, right_index):
        left_child = parent.children[left_index]
        right_child = parent.children[right_index]

        left_child.keys.append(parent.keys[left_index])
        parent.keys[left_index] = right_child.keys.pop(0)

        if right_child.children:
            left_child.children.append(right_child.children.pop(0))

    def _merge(self, parent, left_index, right_index):
        left_child = parent.children[left_index]
        right_child = parent.children[right_index]

        left_child.keys.append(parent.keys.pop(left_index))
        left_child.keys.extend(right_child.keys)
        left_child.children.extend(right_child.children)

        parent.children.pop(right_index)

    def prefix_traversal(self):
        return self._prefix_traversal_recursive(self.root)

    def _prefix_traversal_recursive(self, node):
        if not node:
            return []
        result = node.keys.copy()
        for child in node.children:
            result.extend(self._prefix_traversal_recursive(child))
        return result

# Example usage
tree = TwoThreeTree()
for key in [3, 1, 5, 7, 2, 4, 6]:
    tree.insert(key)

print("Prefix traversal:", tree.prefix_traversal())
print("Search for 5:", tree.search(5))
print("Search for 8:", tree.search(8))

tree.delete(5)
print("After deleting 5:", tree.prefix_traversal())