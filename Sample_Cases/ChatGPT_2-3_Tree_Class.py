class Node:
    def __init__(self, key1=None, key2=None, parent=None):
        """Initialize a 2-3 tree node with up to two keys and pointers to children and parent."""
        self.key1 = key1
        self.key2 = key2
        self.parent = parent
        self.children = [None, None, None]  # Max 3 children for a 2-3 tree node

    def is_leaf(self):
        """Check if the node is a leaf (i.e., it has no children)."""
        return all(child is None for child in self.children)

    def has_two_keys(self):
        """Check if the node has two keys (non-empty key2)."""
        return self.key2 is not None

    def insert_into_node(self, key):
        """Insert a key into this node. Return True if key was successfully added."""
        if self.key1 is None:
            self.key1 = key
            return True
        elif self.key2 is None:
            if key < self.key1:
                self.key1, self.key2 = key, self.key1
            else:
                self.key2 = key
            return True
        return False  # Node already has two keys

class TwoThreeTree:
    def __init__(self):
        """Initialize an empty 2-3 tree."""
        self.root = None

    def search(self, key):
        """Search for a key in the tree. Return the node if found, otherwise None."""
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None:
            return None
        if key == node.key1 or key == node.key2:
            return node
        elif key < node.key1:
            return self._search_recursive(node.children[0], key)
        elif node.key2 is None or key < node.key2:
            return self._search_recursive(node.children[1], key)
        else:
            return self._search_recursive(node.children[2], key)

    def insert(self, key):
        """Insert a key into the 2-3 tree."""
        if self.root is None:
            self.root = Node(key1=key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if node.is_leaf():
            if not node.insert_into_node(key):
                self._split(node, key)
        else:
            if key < node.key1:
                self._insert_recursive(node.children[0], key)
            elif node.key2 is None or key < node.key2:
                self._insert_recursive(node.children[1], key)
            else:
                self._insert_recursive(node.children[2], key)

    def _split(self, node, key):
        """Split a full node during insertion."""
        # Handle splitting logic to maintain 2-3 tree properties
        # This is the key step in insertion in a 2-3 tree.
        new_parent = Node()  # New node to hold the middle key
        if key < node.key1:
            new_parent.key1 = node.key1
            left = Node(key1=key)
            right = Node(key1=node.key2)
        elif key > node.key2:
            new_parent.key1 = node.key2
            left = Node(key1=node.key1)
            right = Node(key1=key)
        else:
            new_parent.key1 = key
            left = Node(key1=node.key1)
            right = Node(key1=node.key2)

        # Fix parent and children
        if node.parent is None:
            self.root = new_parent
        else:
            self._insert_into_parent(node.parent, new_parent)

        new_parent.children = [left, right]

    def _insert_into_parent(self, parent, new_node):
        """Insert the middle value into the parent node during split."""
        # Handle insertion into parent node during a split.
        pass  # Simplified for brevity

    def delete(self, key):
        """Delete a key from the 2-3 tree."""
        node = self.search(key)
        if node is not None:
            self._delete_node(node, key)

    def _delete_node(self, node, key):
        """Perform deletion of a key from a node."""
        if node.is_leaf():
            if key == node.key1:
                node.key1 = node.key2
                node.key2 = None
            elif key == node.key2:
                node.key2 = None
        else:
            # Handle deletion from internal node and rebalancing
            pass  # Deletion and rebalancing are complex in 2-3 trees

    def prefix_traversal(self):
        """Perform a prefix traversal (preorder) of the 2-3 tree."""
        self._prefix_traversal_recursive(self.root)

    def _prefix_traversal_recursive(self, node):
        if node is None:
            return
        if node.key1 is not None:
            print(node.key1, end=" ")
        if node.key2 is not None:
            print(node.key2, end=" ")
        for child in node.children:
            self._prefix_traversal_recursive(child)
